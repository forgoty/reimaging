from .argparser import createParser
from .download import DownloadService
from .upload import UploadService
from .auth import get_user_api, get_service_api
import sys


def main():
    sys.tracebacklimit = 0
    parser = createParser()
    namespace = parser.parse_args(sys.argv[1:])

    if not namespace.command:
        parser.print_help()

    if namespace.command == 'download':

        if namespace.auth:
            api = get_user_api()
        else:
            api = get_service_api()

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

    if namespace.command == 'upload':

        api = get_user_api()

        if namespace.album_id and not namespace.title:
            service = UploadService(api,
                                        album_id=namespace.album_id,
                                        path=namespace.path)

            service.upload_photos()

        if namespace.title and not namespace.album_id:
            service = UploadService(api,
                                        title=namespace.title,
                                        path=namespace.path)

            service.upload_photos()

if __name__ == '__main__':
    main()