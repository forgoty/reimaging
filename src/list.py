from .download import DownloadSession


def get_list(**kwargs):
    session = DownloadSession(**kwargs)
    for album in session.albums:
        print('{}({}) - id:{}'.format(album.title, album.size, album.id))
    session.close()
