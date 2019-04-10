from .download import DownloadSession


def get_list(api, user, system=None):
    session = DownloadSession(api, user, system=system)
    for album in session.get_all_albums():
        print('id:{} - {}({})'.format(album.id, album.title, album.size))
