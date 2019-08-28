import os
import asyncio
import aiohttp
import aiofiles
from tqdm import tqdm

from .core import BaseSession, Album


class DownloadSession(BaseSession):

    def connect(self):
        self.loop.run_until_complete(self.get_all_albums())

    async def get_all_albums(self):
        response = await self.api.photos.getAlbums(
            owner_id=self.user,
            need_system=self.system or 0
        )

        self.albums = [Album(self.api, **item) for item in response['items']]

    def get_album_by_id(self, id):
        return next((album for album in self.albums if album.id == id), None)

    def download_album(self, album):
        self.loop.run_until_complete(album.get_photos())
        os.makedirs(os.path.join(self.path, album.title), exist_ok=True)
        path_to_album = os.path.join(self.path, album.title)
        path_url_pairs = tuple(
            (
                os.path.join(
                    path_to_album,
                    photo.url.split('/')[-1].replace('-', '')
                ),
                photo.url
            ) for photo in album.photos
        )

        self.loop.run_until_complete(
            _download_many(album.title, path_url_pairs)
        )


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
    if os.path.exists(path):
        return

    async with client.get(url) as response:
        if response.status == 200:
            file = await aiofiles.open(path, 'wb')
            await file.write(await response.read())
            await file.close()
