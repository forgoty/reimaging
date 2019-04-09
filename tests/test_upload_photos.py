import os
from shutil import rmtree
from unittest import TestCase

from src.download import DownloadSession
from src.upload import UploadSession
from src import auth


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/'
PATH_TO_TEST_ALBUM = BASE_DIR + 'tests/test_data/'
TEST_ALBUM_TITLE = 'Здесь будут новые фотографии для прессы-службы'
TEST_ALBUM_ID_TO_DOWNLOAD = 136592355
TITLE = "Test"


class UploadTest(TestCase):

    def setUp(self):
        self.api = auth.get_user_api()
        self.user_id = self.api.users.get()[0]['id']

    def tearDown(self):
        rmtree(BASE_DIR + TITLE, ignore_errors=True)
        rmtree(PATH_TO_TEST_ALBUM + TEST_ALBUM_TITLE, ignore_errors=True)

    def test_upload_photos_to_new_album(self):
        self._download_album(TEST_ALBUM_ID_TO_DOWNLOAD,
                             path=PATH_TO_TEST_ALBUM)
        upload = UploadSession(api=self.api,
                               path=PATH_TO_TEST_ALBUM + TEST_ALBUM_TITLE,
                               title=TITLE, album_id=None)
        upload.upload_photos()
        self._download_album(upload.album.id, user=self.user_id,
                             path=BASE_DIR + TITLE)

        self.assertEqual(
            self._get_dir_size(BASE_DIR + TITLE),
            self._get_dir_size(PATH_TO_TEST_ALBUM + TEST_ALBUM_TITLE)
        )
        self.api.photos.deleteAlbum(album_id=upload.album.id)

    def test_upload_to_existing_album(self):
        self._download_album(TEST_ALBUM_ID_TO_DOWNLOAD,
                             path=PATH_TO_TEST_ALBUM)
        upload = UploadSession(api=self.api,
                               path=PATH_TO_TEST_ALBUM + TEST_ALBUM_TITLE,
                               title=TITLE, album_id=None)
        upload.upload_photos()
        upload = UploadSession(api=self.api,
                               path=PATH_TO_TEST_ALBUM + TEST_ALBUM_TITLE,
                               album_id=upload.album.id)
        upload.upload_photos()
        self._download_album(upload.album.id, user=self.user_id,
                             path=BASE_DIR)

        import ipdb; ipdb.set_trace()
        self.assertEqual(
            self._get_dir_size(BASE_DIR + TITLE) / 2,
            self._get_dir_size(PATH_TO_TEST_ALBUM + TEST_ALBUM_TITLE)
        )
        self.api.photos.deleteAlbum(album_id=upload.album.id)


    # private methods

    def _download_album(self, album_id, path=None, user=1):
        download = DownloadSession(api=self.api, user=user,
                                   path=path)
        album = download.get_album_by_id(album_id)
        download.download_album(album)

    @staticmethod
    def _get_dir_size(path):
        return sum(
            os.path.getsize(path+'/'+f) for f in os.listdir(path)
            if os.path.isfile(path+'/'+f)
        )

