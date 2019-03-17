import os
from shutil import rmtree
import filecmp
from unittest import TestCase

from src.download import DownloadService
from src import auth


class DownloadTest(TestCase):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ALBUM_ID = 136592355
    ALBUM_TITLE = 'Здесь будут новые фотографии для прессы-службы'
    JPG_FILE_PATH = BASE_DIR + '/tests/test_data/16ccc1.jpg'

    def setUp(self):
        pass

    def tearDown(self):
        rmtree(self.BASE_DIR + '/'+ self.ALBUM_TITLE, ignore_errors=True)

    def test_album_download_with_service_api(self):
        profile = DownloadService(api=auth.get_service_api(), user=1)
        profile.download_album(self.ALBUM_ID)
        title = profile.get_album_title(self.ALBUM_ID)
        album_ids = [i['id'] for i in profile.albums]
        dirs = os.listdir(self.BASE_DIR)

        self.assertTrue(self.ALBUM_ID in album_ids, 'ALBUM_ID not in albums')
        self.assertTrue(self.ALBUM_TITLE in dirs, 'Failed dir creattion')
        self.assertTrue(filecmp.cmp(
                self.BASE_DIR + '/' + title + '/' + '16ccc1.jpg',
                self.JPG_FILE_PATH)
        )

    def test_album_download_with_user_api(self):
        profile = DownloadService(api=auth.get_user_api(), user=1)
        profile.download_album(self.ALBUM_ID)
        title = profile.get_album_title(self.ALBUM_ID)
        album_ids = [i['id'] for i in profile.albums]
        dirs = os.listdir(self.BASE_DIR)

        self.assertTrue(self.ALBUM_ID in album_ids, 'ALBUM_ID not in albums')
        self.assertTrue(self.ALBUM_TITLE in dirs, 'Failed dir creattion')
        self.assertTrue(filecmp.cmp(
                self.BASE_DIR + '/' + title + '/' + '16ccc1.jpg',
                self.JPG_FILE_PATH)
        )

