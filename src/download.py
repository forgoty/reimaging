import os
from tqdm import tqdm
import asyncio
import aiohttp
import aiofiles

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
                os.path.join(path_to_album, photo.url.split('/')[-1]),
                photo.url
            ) for photo in album.get_photos()
        )

        self._download_async(album.title, path_url_pairs)

    @staticmethod
    def _download_async(title, path_url_pairs):
        loop = asyncio.new_event_loop()
        loop.run_until_complete(_download_many(title, path_url_pairs))
        loop.close()


async def _download_many(title, path_url_pairs):
    async with aiohttp.ClientSession() as client:
        to_do = tuple(
            _download_one(client, path, url) for path, url in path_url_pairs
        )
        to_do_iter = tqdm(
            asyncio.as_completed(to_do),
            total=len(path_url_pairs),
            desc=title,
            ascii=True,
            unit=' photos'
        )

        for coroutine in to_do_iter:
            await coroutine


async def _download_one(client, path, url):
    async with client.get(url) as response:
        if response.status == 200:
            file = await aiofiles.open(path, 'wb')
            await file.write(await response.read())
            await file.close()
