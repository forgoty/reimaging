import os
import requests
import time
from tqdm import tqdm
from multiprocessing import dummy

from .core import BaseSession, Album


FILES_IN_ONE_POST_REQUEST = 4
EXTENSIONS = ('jpg', 'png', 'gif', 'bmp')


class UploadSession(BaseSession):
    def __init__(self, **kwargs):
        super().__init__( **kwargs)
        self.title = kwargs.get('title')

        if kwargs.get('album_id'):
            self.album = self.get_album_by_id(kwargs['album_id'])
        else:
            self.album = self.create_album()

        self.upload_server = self._get_upload_server()

    def get_album_by_id(self, id):
        response = self.api.photos.getAlbums(
            albums_ids=[id],
        )
        return Album(self.api, **response['items'][0])

    def create_album(self):
        album = self.api.photos.createAlbum(title=self.title, privacy=3,
                                            comment_privacy=3)
        return Album(self.api, **album)

    def _get_upload_server(self):
        response = self.api.photos.getUploadServer(album_id=self.album.id)
        return response['upload_url']

    def upload_photos(self):
        file_paths = self._get_file_paths()
        files_count = len(file_paths)
        path_groups = list(
            self._get_path_group(file_paths, step=FILES_IN_ONE_POST_REQUEST)
        )

        pbar = tqdm(total=files_count, ascii=True, desc=self.title,
                    leave=False, unit=' photos')

        with dummy.Pool(processes=self.workers) as pool:
            with pbar:
                for _ in pool.imap_unordered(self._send_request, path_groups):
                    pbar.update(FILES_IN_ONE_POST_REQUEST)

                pbar.close()
                print('Successfully uploaded {} photos'.format(files_count))

    def _get_file_paths(self):
        file_paths = [
            os.path.join(self.path, file) for file in os.listdir(self.path)
            if os.path.isfile(os.path.join(self.path, file))
            if file.endswith(EXTENSIONS)
        ]

        if not file_paths:
            print('No images found')
            exit(1)
        else:
            return file_paths

    @staticmethod
    def _get_path_group(paths, step=1):
        while paths:
            yield tuple(paths[:step])
            del paths[:step]

    def _send_request(self, paths):
        name_key_pair = self._get_uploading_pair(paths)
        try:
            request = requests.post(self.upload_server, files=name_key_pair)
            self.api.photos.save(album_id=self.album.id, **request.json())
            time.sleep(0.34)
        finally:
            self._close_files(name_key_pair)

    @staticmethod
    def _get_uploading_pair(paths):
        name_key_pair = []
        for i, path in enumerate(paths):
            file = open(path, 'rb')
            name_key_pair.append(
                (
                    'file{}'.format(i+1),
                    ('photo{}.{}'.format(i, path[-3:]), file)
                )
            )

        return name_key_pair

    @staticmethod
    def _close_files(group):
        for i in group:
            i[1][1].close()
