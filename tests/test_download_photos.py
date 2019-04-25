import os
from shutil import rmtree
import filecmp
from unittest import TestCase

from src.download import DownloadSession
from src.core import CPU_COUNT
from src import auth


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ALBUM_ID = 136592355
ALBUM_TITLE = 'Здесь будут новые фотографии для прессы-службы'
JPG_FILE_PATH = BASE_DIR + '/tests/test_data/aef149.jpg'


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
                BASE_DIR + '/' + album.title + '/' + 'aef149.jpg',
                JPG_FILE_PATH)
        )

    def test_album_download_with_user_api(self):
        session = DownloadSession(api=auth.get_user_api(), user=1)
        album = session.get_album_by_id(ALBUM_ID)
        session.download_album(album)
        dirs = os.listdir(BASE_DIR)

        self.assertTrue(ALBUM_TITLE in dirs, 'Failed dir creattion')
        self.assertTrue(filecmp.cmp(
                BASE_DIR + '/' + album.title + '/' + 'aef149.jpg',
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
                BASE_DIR + '/' + album.title + '/' + 'aef149.jpg',
                JPG_FILE_PATH)
        )
        rmtree(BASE_DIR + '/' + album.title + '/', ignore_errors=True)

    def test_init_session_with_double_workers_count(self):
        workers_amount = CPU_COUNT * 2
        args = {'api': auth.get_service_api(), 'user': 1, 'workers': workers_amount}
        session = DownloadSession(**args)
        self.assertEqual(session.workers, workers_amount)

    def test_init_session_with_unvalid_count_of_workers(self):
        workers_amount = CPU_COUNT * 20
        args = {'api': auth.get_service_api(), 'user': 1, 'workers': workers_amount}
        session = DownloadSession(**args)
        self.assertNotEqual(session.workers, workers_amount)


