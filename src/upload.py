from os import listdir, getcwd
from os.path import isfile, join
import requests
from tqdm import tqdm
from multiprocessing import dummy, cpu_count
from pyvk.exceptions import APIError


class UploadService():
    def __init__(self, api, title=None, path=None, album_id=None):

        self.api = api
        self.title = title

        if path:
            self.path = path
        else:
            self.path = getcwd()

        if album_id:
            self.album_id = album_id
        else:
            self.album_id = self.create_album()

        self.upload_server = self.get_upload_server()


    def create_album(self):
        try:
            album = self.api.photos.createAlbum(title=self.title, privacy=3,
                                                            comment_privacy=3)
        except APIError as exc:
            print('Error %d: %s' % (exc.error_code, exc.error_msg))
            exit(1)

        return album['id']

    def get_upload_server(self):
        try:
            response = self.api.photos.getUploadServer(album_id=self.album_id)
        except APIError as exc:
            print('Error %d: %s' % (exc.error_code, exc.error_msg))
            exit(1)

        return response['upload_url']


    def upload_photos(self):
        #"step" is actually number of files to post in one request
        step = 4
        extensions = ['JPG', 'PNG', 'GIF', 'BMP']
        try:
            file_path = [join(self.path, file) for file in listdir(self.path)
                                if isfile(join(self.path, file))
                                if file[-3:].upper() in extensions]
        except OSError as e:
            print('Error %d: %s' % (e.error_code, e.error_msg))
            exit(1)

        if not file_path:
            print('No images found')
            exit(1)

        file_path_len = len(file_path)
        fields = list(self.get_items_gen(file_path, step=step))

        with dummy.Pool(processes=cpu_count()) as pool:
            with tqdm(total=file_path_len, ascii=True, desc=self.title,
                        leave=False, unit=' photos') as pbar:
                for _ in pool.imap_unordered(self.send_request, fields):
                    pbar.update(step)

                pbar.close()
                print('Successfully uploaded {} photos'.format(file_path_len))

    def send_request(self, paths):
        data = []

        for i, path in enumerate(paths):
            file = open(path, 'rb')
            data.append(('file{}'.format(i+1),
                            ('photo{}.{}'.format(i, path[-3:]), file)))

        try:
            request = requests.post(self.upload_server, files=data).json()
            self.api.photos.save(album_id=self.album_id, **request)
        except APIError as exc:
            print('Error %d: %s' % (exc.error_code, exc.error_msg))
            exit(1)
        finally:
            self.close_files(data)

    @staticmethod
    def get_items_gen(data, step=1):
        while data:
            yield list(data[:step])
            del data[:step]

    @staticmethod
    def close_files(field):
        for f in field:
            f[1][1].close()

