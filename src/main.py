import sys
from pyvk.exceptions import *

from .argparser import createParser
from .download import DownloadSession
from .upload import UploadSession
from .auth import get_user_api, get_service_api
from .list import get_list


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
        print('Try again later')
        sys.exit(1)

    except APIError as e:
        print('API Error %d: %s' % (e.error_code, e.error_msg))
        print('Check photos')
        sys.exit(1)


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


def download_command(namespace):
    if namespace.auth:
        api = get_user_api()
    else:
        api = get_service_api()

    if namespace.album_id:
        session = DownloadSession(api=api, **vars(namespace))
        album = session.get_album_by_id(namespace.album_id)
        session.download_album(album)
    else:
        session = DownloadSession(api=api, **vars(namespace))
        for album in session.albums:
            session.download_album(album)


def upload_command(namespace):
    api = get_user_api()
    session = UploadSession(api=api, **vars(namespace))
    session.upload_photos()


def list_command(namespace):
    if namespace.auth:
        api = get_user_api()
    else:
        api = get_service_api()

    get_list(api=api, **vars(namespace))


if __name__ == '__main__':
    main()
