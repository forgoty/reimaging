from argparser import createParser
from download import DownloadService
import sys


def main():
    parser = createParser()
    namespace = parser.parse_args(sys.argv[1:])
    if namespace.command == 'download':
        if namespace.album_id == None:
            service = DownloadService(namespace.owner, namespace.path)
            for item in service.albums:
                service.download_album(item.get('id'))
        else:
            service = DownloadService(namespace.owner, namespace.path)
            service.download_album(namespace.album_id)
    if not namespace.command:
        parser.print_help()


if __name__ == '__main__':
    main()