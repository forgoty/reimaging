from .download2 import DownloadService


def get_list(api, user, system=None):
    service = DownloadService(api, user, system=system)
    for album in service.albums:
        print('id:{} - {}({})'.format(album.id, album.title, album.size))
