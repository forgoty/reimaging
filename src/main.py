import sys
from pyvk.exceptions import APIError

from .argparser import createParser
from .download import DownloadService
from .upload import UploadService
from .auth import get_user_api, get_service_api


def command_line_runner():
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


def main():
    try:
        command_line_runner()
    except KeyboardInterrupt:
        print('Keyboard Interrupt')
        sys.exit(1)

    except APIError as exc:
        print('Connection Error %d: %s' % (exc.error_code, exc.error_msg))
        sys.exit(1)

    except OSError as e:
        print('System Error %d: %s' % (e.error_code, e.error_msg))
        sys.exit(1)


if __name__ == '__main__':
    main()