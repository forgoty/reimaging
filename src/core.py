import os
import asyncio
import aiovk

from .mixins import LimitRateDriverMixin
from .auth import get_user_api, get_service_api


class UploadDriver(LimitRateDriverMixin, aiovk.drivers.HttpDriver):
    request_per_period = 5
    period = 2


class BaseSession():
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

        self.path = kwargs.get('path') or os.getcwd()
        self.loop = asyncio.get_event_loop()
        self.api = self._get_api()

    def _get_api(self):
        if self.command == 'upload':
            return get_user_api(driver=UploadDriver)
        if self.auth and self.command in ('download', 'list'):
            return get_user_api()
        else:
            return get_service_api()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.loop.run_until_complete(self.api._session.close())


class Album():
    def __init__(self, api, **kwargs):
        self.api = api
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __repr__(self):
        return 'Album ({})'.format(self.title)

    @property
    def vk_link(self):
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
