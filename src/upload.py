import os
import json
from tqdm import tqdm
import asyncio
import aiohttp

from .core import BaseSession, Album


FILES_IN_ONE_POST_REQUEST = 5
EXTENSIONS = ('jpg', 'png', 'gif', 'bmp')


class UploadSession(BaseSession):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = kwargs.get('title')

        if kwargs.get('album_id'):
            self.loop.run_until_complete(
                self.get_album_by_id(kwargs['album_id'])
            )
        else:
            self.loop.run_until_complete(self.create_album())

        self.loop.run_until_complete(self._get_upload_server())

    async def get_album_by_id(self, id):
        response = await self.api.photos.getAlbums(
            albums_ids=[id],
        )
        self.album = Album(self.api, **response['items'][0])

    async def create_album(self):
        album = await self.api.photos.createAlbum(
            title=self.title,
            privacy_view='only_me',
        )
        self.album = Album(self.api, **album)

    async def _get_upload_server(self):
        response = await self.api.photos.getUploadServer(
            album_id=self.album.id
        )
        self.upload_server = response['upload_url']

    def upload_photos(self):
        file_paths = self._get_file_paths()
        files_count = len(file_paths)
        path_groups = list(
            self._get_path_group(file_paths, step=FILES_IN_ONE_POST_REQUEST)
        )

        self._upload_async(files_count, path_groups)

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

    def _upload_async(self, files_count, path_groups):
        self.loop.run_until_complete(
            self._upload_many(files_count, path_groups)
        )

    async def _upload_many(self, files_count, path_groups):
        async with aiohttp.ClientSession() as session:
            to_do = tuple(
                self._upload_file(session, group) for group in path_groups
            )
            pbar = tqdm(
                total=files_count,
                desc=self.title,
                ascii=True,
                unit=' photos',
                unit_scale=1,
            )

            for coroutine in asyncio.as_completed(to_do):
                await coroutine
                pbar.update(files_count/len(to_do))
            pbar.close()

    async def _upload_file(self, session, group):
        data = self._get_uploading_data(group)
        async with session.post(self.upload_server, data=data) as response:
            if response.status == 200:
                json_result = json.loads(await response.text())
                await asyncio.sleep(0.6)
                await self.api.photos.save(
                    album_id=self.album.id,
                    **json_result
                )

    @staticmethod
    def _get_uploading_data(group):
        data = aiohttp.FormData()
        for index, path in enumerate(group):
            data.add_field(
                'file{}'.format(index+1),
                open(path, 'rb'),
                filename='photo{}.{}'.format(index+1, path.split('.')[-1]),
            )
        return data
