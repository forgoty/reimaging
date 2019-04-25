import os
from tqdm import tqdm
import requests
from multiprocessing import Pool

from .core import BaseSession, Album


class DownloadSession(BaseSession):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user = kwargs.get('user')
        self.system = kwargs.get('system', False)
        self.albums = self.get_all_albums()

    def get_all_albums(self):
        response = self.api.photos.getAlbums(
            owner_id=self.user,
            need_system=self.system
        )

        return [Album(self.api, **item) for item in response['items']]

    def get_album_by_id(self, id):
        return next((album for album in self.albums if album.id == id), None)

    def download_album(self, album):
        os.makedirs(os.path.join(self.path, album.title), exist_ok=True)
        path_to_album = os.path.join(self.path, album.title)
        path_url_pairs = tuple(
            (
                os.path.join(path_to_album, photo.url[len(photo.url)-10:]),
                photo.url
            ) for photo in album.get_photos()
        )

        with Pool(processes=self.workers) as pool:
            progressbar = tqdm(
                pool.imap_unordered(self._download_routine, path_url_pairs),
                total=album.size,
                ascii=True,
                desc=album.title,
                unit=' photos'
            )
            for _ in progressbar:
                pass

    @staticmethod
    def _download_routine(path_url_pairs):
        path, url = path_url_pairs

        if os.path.exists(path):
            print('{} already exists'.format(path))
            return

        response = requests.get(url)
        if response.status_code == 200:
            with open(path, 'wb') as file:
                file.write(response.content)
