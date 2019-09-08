import os
from shutil import rmtree
from unittest import TestCase

from src.download import DownloadSession
from src.upload import UploadSession


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/'
PATH_TO_TEST_ALBUM = BASE_DIR + 'tests/test_data/'
TEST_ALBUM_TITLE = 'Здесь будут новые фотографии для прессы-службы'
TEST_ALBUM_ID_TO_DOWNLOAD = 136592355
TITLE = "Test"


class UploadTest(TestCase):

    def tearDown(self):
        rmtree(BASE_DIR + TITLE, ignore_errors=True)
        rmtree(PATH_TO_TEST_ALBUM + TEST_ALBUM_TITLE, ignore_errors=True)

    def test_upload_photos_to_new_album(self):
        downloaded = self._download_album(TEST_ALBUM_ID_TO_DOWNLOAD,
                                          path=PATH_TO_TEST_ALBUM)
        with UploadSession(**self._get_kwargs()) as session:
            session.connect()
            session.upload_photos()
            self.assertEqual(len(session.album.get_photos()), downloaded, 'Photos count should be equal!')

    # private methods
    def _download_album(self, album_id, path=None, user=1):
        args = {'user': user, 'command': 'download', 'auth': False, 'system': 0, 'path': path}
        with DownloadSession(**args) as download:
            download.connect()
            album = download.get_album_by_id(album_id)
            download.download_album(album)
            return len(album.get_photos())

    def _get_kwargs(self):
        return {
            'command': 'upload',
            'path': PATH_TO_TEST_ALBUM + TEST_ALBUM_TITLE,
            'title': TITLE,
            'album_id': None,
        }
