import os
import asyncio
import aiovk

from aiovk.mixins import LimitRateDriverMixin
from .auth import get_user_api, get_service_api


class SoftHttpDriver(LimitRateDriverMixin, aiovk.drivers.HttpDriver):
    request_per_period = 3
    period = 1.3


class BaseSession():
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

        self.path = kwargs.get('path') or os.getcwd()
        self.loop = asyncio.get_event_loop()
        self.api = self._get_api()

    def _get_api(self):
        if self.command in ('upload', 'download'):
            return get_user_api(driver=SoftHttpDriver)
        if self.auth and self.command == 'list':
            return get_user_api()
        else:
            return get_service_api()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.loop.run_until_complete(self.api._session.close())


class Album():
    MAX_COUNT = 1000

    def __init__(self, api, **kwargs):
        self.api = api
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __repr__(self):
        return 'Album ({})'.format(self.title)

    @property
    def vk_link(self):
        return 'https://vk.com/{}_{}'.format(self.owner_id, self.id)

    def get_photos(self):
        loop = asyncio.get_event_loop()
        self.photos = loop.run_until_complete(self._delegate())
        return self.photos

    async def _delegate(self):
        from math import ceil
        from itertools import accumulate

        count = ceil(self.size/self.MAX_COUNT)
        offsets = [0]
        offsets.extend(accumulate(self.MAX_COUNT for i in range(count)))

        coros = [self._send(offset) for offset in offsets]

        photos = []
        for coro in asyncio.as_completed(coros):
            photos += await coro

        return photos

    async def _send(self, offset):
        response = await self.api.photos.get(
            owner_id=self.owner_id,
            album_id=self.id,
            photo_sizes=1,
            count=self.MAX_COUNT,
            offset=offset,
        )
        return [Photo(**item) for item in response['items']]


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
