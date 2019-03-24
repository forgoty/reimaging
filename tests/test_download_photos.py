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
        album = profile.get_album(self.ALBUM_ID)
        profile.download_album(album)
        dirs = os.listdir(self.BASE_DIR)

        self.assertTrue(self.ALBUM_TITLE in dirs, 'Failed dir creattion')
        self.assertTrue(filecmp.cmp(
                self.BASE_DIR + '/' + album.title + '/' + '16ccc1.jpg',
                self.JPG_FILE_PATH)
        )

    def test_album_download_with_user_api(self):
        profile = DownloadService(api=auth.get_user_api(), user=1)
        album = profile.get_album(self.ALBUM_ID)
        profile.download_album(album)
        dirs = os.listdir(self.BASE_DIR)

        self.assertTrue(self.ALBUM_TITLE in dirs, 'Failed dir creattion')
        self.assertTrue(filecmp.cmp(
                self.BASE_DIR + '/' + album.title + '/' + '16ccc1.jpg',
                self.JPG_FILE_PATH)
        )

    def test_service_album_download(self):
        album_id = -6
        testing_file = self.BASE_DIR + '/tests/test_data/fafe4c.jpg'
        profile = DownloadService(api=auth.get_service_api(), user=1, system=1)
        album = profile.get_album(album_id)
        profile.download_album(album)
        dirs = os.listdir(self.BASE_DIR)

        self.assertTrue(album.title in dirs, 'Failed dir creattion')
        self.assertTrue(filecmp.cmp(
                self.BASE_DIR + '/' + album.title + '/' + 'fafe4c.jpg',
                testing_file)
        )
        rmtree(self.BASE_DIR + '/'+ album.title, ignore_errors=True)
