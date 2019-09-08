from .download import DownloadSession


def get_list(**kwargs):
    with DownloadSession(**kwargs) as session:
        session.connect()
        for album in session.albums:
            print('{}({}) - id:{}'.format(album.title, album.size, album.id))
