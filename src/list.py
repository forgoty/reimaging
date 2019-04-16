from .download import DownloadSession


def get_list(**kwargs):
    session = DownloadSession(**kwargs)
    for album in session.get_all_albums():
        print('{}({}) - id:{}'.format(album.title, album.size, album.id))
