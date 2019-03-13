import os
import requests
from tqdm import tqdm
from multiprocessing import dummy, cpu_count
import time


class UploadService():
    def __init__(self, api, title=None, path=None, album_id=None):
        self.api = api
        self.title = title

        if path is not None:
            self.path = path
        else:
            self.path = os.getcwd()

        if album_id:
            self.album_id = album_id
        else:
            self.album_id = self.create_album()

        self.upload_server = self._get_upload_server()


    def create_album(self):
        album = self.api.photos.createAlbum(title=self.title, privacy=3,
                                            comment_privacy=3)
        return album['id']

    def _get_upload_server(self):
        response = self.api.photos.getUploadServer(album_id=self.album_id)
        return response['upload_url']

    def upload_photos(self):
        FILES_IN_ONE_POST_REQUEST = 4
        extensions = ('jpg', 'png', 'gif', 'bmp')

        file_path = [
            os.path.join(self.path, file) for file in os.listdir(self.path)
                if os.path.isfile(os.path.join(self.path, file))
                if file.endwith(extensions)
        ]

        if not file_path:
            print('No images found')
            exit(1)

        file_path_len = len(file_path)
        fields = list(self._get_items_gen(file_path,
                                            step=FILES_IN_ONE_POST_REQUEST))

        with dummy.Pool(processes=cpu_count()) as pool:
            with tqdm(total=file_path_len, ascii=True, desc=self.title,
                        leave=False, unit=' photos') as pbar:

                for _ in pool.imap_unordered(self.send_request, fields):
                    pbar.update(FILES_IN_ONE_POST_REQUEST)

                pbar.close()
                print('Successfully uploaded {} photos'.format(file_path_len))

    def send_request(self, paths):
        data = []

        for i, path in enumerate(paths):
            file = open(path, 'rb')
            data.append(
                ('file{}'.format(i+1),
                ('photo{}.{}'.format(i, path[-3:]), file))
            )

        try:
            request = requests.post(self.upload_server, files=data)
            self.api.photos.save(album_id=self.album_id, **request.json())
            time.sleep(.2)
        finally:
            self._close_files(data)

    @staticmethod
    def _get_items_gen(data, step=1):
        while data:
            yield tuple(data[:step])
            del data[:step]

    @staticmethod
    def _close_files(field):
        for f in field:
            f[1][1].close()

