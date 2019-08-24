import os
from shutil import rmtree
import filecmp
from unittest import TestCase

from src.download import DownloadSession
from src import auth


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ALBUM_ID = 136592355
FILENAME = 'w_62aef149.jpg'
ALBUM_TITLE = 'Здесь будут новые фотографии для прессы-службы'
JPG_FILE_PATH = BASE_DIR + '/tests/test_data/' + FILENAME


class DownloadTest(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        rmtree(BASE_DIR + '/' + ALBUM_TITLE, ignore_errors=True)

    def test_albums_download_with_service_api(self):
        args = {'api': auth.get_service_api(), 'user': 1}
        session = DownloadSession(**args)
        album = session.get_album_by_id(ALBUM_ID)
        session.download_album(album)
        dirs = os.listdir(BASE_DIR)

        self.assertTrue(ALBUM_TITLE in dirs, 'Failed dir creattion')
        self.assertTrue(filecmp.cmp(
                BASE_DIR + '/' + album.title + '/' + FILENAME,
                JPG_FILE_PATH)
        )

    def test_album_download_with_user_api(self):
        session = DownloadSession(api=auth.get_user_api(), user=1)
        album = session.get_album_by_id(ALBUM_ID)
        session.download_album(album)
        dirs = os.listdir(BASE_DIR)

        self.assertTrue(ALBUM_TITLE in dirs, 'Failed dir creattion')
        self.assertTrue(filecmp.cmp(
                BASE_DIR + '/' + album.title + '/' + FILENAME,
                JPG_FILE_PATH)
        )

    def test_album_download_with_service_api(self):
        album_id = -6
        args = {'api': auth.get_service_api(), 'user': 1, "system": 1}
        session = DownloadSession(**args)
        album = session.get_album_by_id(album_id)
        session.download_album(album)
        dirs = os.listdir(BASE_DIR)

        self.assertTrue(album.title in dirs, 'Failed dir creattion')
        self.assertTrue(filecmp.cmp(
                BASE_DIR + '/' + album.title + '/' + FILENAME,
                JPG_FILE_PATH)
        )
        rmtree(BASE_DIR + '/' + album.title + '/', ignore_errors=True)
