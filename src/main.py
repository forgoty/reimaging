import sys
from aiovk import exceptions

from .argparser import createParser
from .download import DownloadSession
from .upload import UploadSession
from .list import get_list


def main():
    sys.tracebacklimit = 0

    try:
        command_line_runner()
    except (EOFError, KeyboardInterrupt):
        print('\nKeyboard Interrupt')
        sys.exit(1)

    except OSError as e:
        print('OSError Error: {} '.format(str(e)))
        sys.exit(1)

    except exceptions.VkAuthError as e:
        print(f'Authentication Error: {e}')
        sys.exit(1)

    except exceptions.VkAPIError as e:
        print(f'Request Error: {e}')
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
    with DownloadSession(**vars(namespace)) as session:
        session.connect()
        if namespace.album_id:
            album = session.get_album_by_id(session.album_id)
            session.download_album(album)
        else:
            for album in session.albums:
                session.download_album(album)


def upload_command(namespace):
    with UploadSession(**vars(namespace)) as session:
        session.connect()
        session.upload_photos()


def list_command(namespace):
    get_list(**vars(namespace))


if __name__ == '__main__':
    main()
