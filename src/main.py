from argparser import createParser
from download import DownloadService
import auth
import sys


def main():
    parser = createParser()
    namespace = parser.parse_args(sys.argv[1:])

    if not namespace.command:
        parser.print_help()

    if namespace.command == 'download':

        if namespace.auth:
            api = auth.get_user_api()
        else:
            api = auth.get_service_api()
            
        if namespace.album_id:
            service = DownloadService(api=api,
                                        owner=namespace.owner,
                                        path=namespace.path,
                                        system=namespace.system)

            service.download_album(namespace.album_id)
        else:
            service = DownloadService(api=api,
                                        owner=namespace.owner,
                                        path=namespace.path,
                                        system=namespace.system)

            for item in service.albums:
                service.download_album(item['id'])


if __name__ == '__main__':
    main()