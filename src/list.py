from .download import DownloadService


def get_list(api, user, system=None):
    service = DownloadService(api, user, system=system)
    for album in service.get_all_albums:
        print('id:{} - {}({})'.format(album.id, album.title, album.size))
