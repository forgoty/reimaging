import os
from unittest import TestCase

from ..src.download import DownloadService
from ..src import auth


class DownloadTest(TestCase):

    def test_album_download_with_service_api(self):
        profile = DownloadService(api=auth.get_service_api(), user=1)
        asdf = [i['id'] for i in profile.albums]
        self.assetTrue(136592355 in asdf)
        # profile.download_album(136592355)
        # os.path.relpath()

