import sys
from pyvk.exceptions import *

from .argparser import createParser
from .download import DownloadSession
from .upload import UploadSession
from .auth import get_user_api, get_service_api
from .list import get_list


def download_command(namespace):
    if namespace.auth:
        api = get_user_api()
    else:
        api = get_service_api()

    if namespace.album_id:
        session = DownloadSession(
            api=api,
            user=namespace.user,
            path=namespace.path,
            system=namespace.system
        )

        album = session.get_album_by_id(namespace.album_id)
        session.download_album(album)

    else:
        session = DownloadSession(
            api=api,
            user=namespace.user,
            path=namespace.path,
            system=namespace.system
        )

        for item in session.albums:
            session.download_album(item)


def upload_command(namespace):
    api = get_user_api()

    if namespace.album_id and not namespace.title:
        session = UploadSession(
            api,
            album_id=namespace.album_id,
            path=namespace.path
        )
        session.upload_photos()

    if namespace.title and not namespace.album_id:
        session = UploadSession(
            api,
            title=namespace.title,
            path=namespace.path
        )
        session.upload_photos()


def list_command(namespace):
    if namespace.auth:
        api = get_user_api()
    else:
        api = get_service_api()

    get_list(api, namespace.id, namespace.system)


def command_line_runner():
    parser = createParser()
    namespace = parser.parse_args(sys.argv[1:])

    if not namespace.command:
        parser.print_help()

    if namespace.command == 'download':
        download_command(namespace)

    if namespace.command == 'upload':
        upload_command(namespace)

    if namespace.command == 'list':
        list_command(namespace)


def main():
    sys.tracebacklimit = 0

    try:
        command_line_runner()

    except KeyboardInterrupt:
        print('Keyboard Interrupt')
        sys.exit(1)

    except OSError as e:
        print(e)
        sys.exit(1)

    except AuthError as e:
        print('Authentication Error %d: %s' % (e.error_code, e.error_msg))
        sys.exit(1)

    except InvalidToken as e:
        print('Invalid Token Error %d: %s' % (e.error_code, e.error_msg))
        sys.exit(1)

    except ReqError as e:
        print('Request Error %d: %s' % (e.error_code, e.error_msg))
        print('Seems VK is denying all our requests')
        print('Just Try again later')
        sys.exit(1)

    except APIError as e:
        print('API Error %d: %s' % (e.error_code, e.error_msg))
        if e.error_msg == 'Unknown error occurred':
            print('Try again later')
        sys.exit(1)


if __name__ == '__main__':
    main()
