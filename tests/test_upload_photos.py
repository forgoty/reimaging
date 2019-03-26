import os
from shutil import rmtree
import filecmp
from unittest import TestCase

from src.download import DownloadService
from src.upload import UploadService
from src import auth


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/'
PATH_TO_PHOTOS = BASE_DIR + 'tests/test_data/'
asdf = 'Здесь будут новые фотографии для прессы-службы'
TEST_ALBUM_TITLE = "Test"
ALBUM_ID_TO_DOWNLOAD = 136592355


class UploadTest(TestCase):

    def setUp(self):
        self.api = auth.get_user_api()
        self.user_id = self.api.users.get()[0]['id']
        self._download_album(ALBUM_ID_TO_DOWNLOAD, path=PATH_TO_PHOTOS)

    def tearDown(self):
        pass
        # rmtree(BASE_DIR + '/'+ ALBUM_TITLE, ignore_errors=True)

    # def test_one_one_equal_two(self):
    #     self.assertEqual(1+1, 2, 'WTF')

    def test_upload_photos_to_new_album(self):
        upload = UploadService(api=self.api, path=PATH_TO_PHOTOS + asdf,
                                title=TEST_ALBUM_TITLE, album_id=None)
        upload.upload_photos()
        self._download_album(upload.album.id, user=self.user_id, path=BASE_DIR + upload.album.title)
        title = upload.album.title

        self.assertEqual(
            sum(os.path.getsize(f) for f in os.listdir(BASE_DIR + title + '/') if os.path.isfile(f)),
            sum(os.path.getsize(f) for f in os.listdir(PATH_TO_PHOTOS + asdf + '/') if os.path.isfile(f))
        )
        self.api.photos.deleteAlbum(album_id=upload.album.id)

    # private methods

    def _download_album(self, album_id, path=None, user=1):
        download = DownloadService(api=self.api, user=user,
                                    path=path)
        album = download.get_album_by_id(album_id)
        download.download_album(album)
