from .download import DownloadService
get_albums = DownloadService.get_albums


def get_list(api, user_id, system=None):
    albums = get_albums(api, user_id, system)
    for album in albums:
        id = album.get('id')
        title = album.get('title')
        size = album.get('size')
        print('id:{} - {}({})'.format(id, title, size))
