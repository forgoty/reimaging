import os
import asyncio
import aiovk

from .mixins import LimitRateDriverMixin


class UploadDriver(LimitRateDriverMixin, aiovk.drivers.HttpDriver):
    request_per_period = 5
    period = 2


class BaseSession():
    def __init__(self, **kwargs):
        self.path = kwargs.get('path') or os.getcwd()
        self.api = kwargs.get('api')
        self.loop = asyncio.get_event_loop()

    def close(self):
        self.loop.run_until_complete(self.api._session.close())


class Album():
    def __init__(self, api, **kwargs):
        self.api = api
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __repr__(self):
        return 'Album {}_{}'.format(self.owner_id, self.id)

    @property
    def link(self):
        return 'https://vk.com/{}_{}'.format(self.owner_id, self.id)

    async def get_photos(self):
        response = await self.api.photos.get(
            owner_id=self.owner_id,
            album_id=self.id,
            photo_sizes=1,
            count=1000
        )

        self.photos = [Photo(**item) for item in response['items']]
        return self.photos


class Photo():
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __repr__(self):
        return 'Photo {}_{}'.format(self.owner_id, self.id)

    @property
    def vk_link(self):
        return 'https://vk.com/photo{}_{}'.format(self.owner_id, self.id)

    @property
    def url(self):
        resolution = ('w', 'z', 'y', 'x', 'r', 'q', 'p', 'o', 'm', 's')
        self.sizes.sort(key=lambda i: resolution.index(i['type']))
        return self.sizes[0]['src']
