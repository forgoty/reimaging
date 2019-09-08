import os
from unittest import TestCase

from src.list import get_list


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ALBUM_ID = 136592355
ALBUM_TITLE = 'Здесь будут новые фотографии для прессы-службы'
JPG_FILE_PATH = BASE_DIR + '/tests/test_data/aef149.jpg'


class ListTest(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_list(self):
        kwargs = {'user': 1, 'command': 'list', 'auth': False, 'system': 0}
        try:
            get_list(**kwargs)
        except:
            self.fail('Unexpected exception occured')
