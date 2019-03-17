import os
from tqdm import tqdm
import requests
from multiprocessing import Pool, cpu_count

from .core import Album


class DownloadService():
    def __init__(self, api, user, path=None, system=0):
        if path is not None:
            self.path = path
        else:
            self.path = os.getcwd()

        self.user = user
        self.system = system
        self.api = api
        self.albums = self.get_all_albums()

    def get_all_albums(self):
        response = self.api.photos.getAlbums(
            owner_id=self.user,
            need_system=self.system
        )

        return [Album(self.api,**item) for item in response['items']]

    def get_album(self, id):
        for album in self.albums:
            if album.id == id:
                return album

    def download(self, album):
        os.makedirs(os.path.join(self.path, album.title), exist_ok=True)
        args = tuple(
            (link, self.path, album.title) for link in album.get_photo_links()
        )

        with Pool(processes=cpu_count()) as pool:
            for _ in tqdm(
                pool.imap_unordered(self._download_routine, args),
                total=album.size,
                ascii=True,
                desc=album.title,
                unit=' photos'
            ):
                pass

    @staticmethod
    def _download_routine(data):
        link, path, title = data
        path_to_file = os.path.join(path, title, link[len(link)-10:])

        if os.path.exists(path_to_file):
            return

        response = requests.get(link)
        if response.status_code == 200:
            with open(path_to_file, 'wb') as f:
                f.write(response.content)
