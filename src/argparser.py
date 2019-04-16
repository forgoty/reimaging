import sys
import argparse
from . import __version__


def createParser():
    parser = argparse.ArgumentParser(
        prog='reimaging',
        description='''Simple photo downloader/uploader for vk.com''',
        add_help=False
    )

    parent_group = parser.add_argument_group(title='Params')
    parent_group.add_argument('--help', '-h', action='help', help='Help')
    parent_group.add_argument(
        '--version',
        action='version',
        help='reimaging version',
        version='%(prog)s {}'.format(__version__)
    )

    subparsers = parser.add_subparsers(dest='command', title='Commands')

    create_download_parser(subparsers)
    create_upload_parser(subparsers)
    create_list_parser(subparsers)

    return parser


def create_download_parser(subparsers):
    download_parser = subparsers.add_parser(
        'download',
        add_help=False,
        description='''Download photos to local drive'''
    )

    download_group = download_parser.add_argument_group(title='Params')

    download_group.add_argument(
        '-a',
        '--auth',
        action='store_const',
        const=True,
        help='''Enable authorization for downloading private albums'''
    )

    download_group.add_argument(
        '-u',
        '--user',
        type=int,
        required=True,
        help='''Takes an user ID for download all user albums.
            By default download all albums at working directory.
            Type "-" in front of user ID to download group photos'''
    )

    download_group.add_argument(
        '-p',
        '--path',
        help='Changes download folder'
    )

    download_group.add_argument(
        '--album_id',
        type=int,
        help='Download only user album by album id'
    )

    download_group.add_argument(
        '-w',
        '--workers',
        type=int,
        help='Number of workers'
    )

    download_group.add_argument(
        '--system',
        action='store_const',
        const=True,
        help='''Download system albums. If album ID is not set,
                download all system albums
                Album ID for profile photos = -6.
                Album ID for wall photos = -7.
                Album ID for saved photos = -15.'''
        )


    download_group.add_argument('--help', '-h', action='help', help='Help')


def create_upload_parser(subparsers):
    upload_parser = subparsers.add_parser(
        'upload',
        add_help=False,
        description='Upload photos to VK album'
    )

    upload_group = upload_parser.add_argument_group(title='Params')

    upload_group.add_argument(
        '-p',
        '--path',
        help='Choose photo path for upload'
    )

    upload_group.add_argument(
        '-w',
        '--workers',
        type=int,
        help='Number of workers'
    )

    upload_subgroup = upload_group.add_mutually_exclusive_group()

    upload_subgroup.add_argument(
        '-t',
        '--title',
        action='store',
        help='Create Album with "title" name'
    )

    upload_subgroup.add_argument(
        '--album_id',
        action='store',
        help='Update album by ID'
    )

    upload_group.add_argument('--help', '-h', action='help', help='Help')


def create_list_parser(subparsers):
    list_parser = subparsers.add_parser(
        'list',
        description='Get list of user photo albums'
    )

    list_parser.add_argument(
        'user',
        type=int,
        help='User ID'
    )

    list_group = list_parser.add_argument_group(title='Params')
    list_group.add_argument(
        '-a',
        '--auth',
        action='store_const',
        const=True,
        help='Enable authorization'
    )

    list_group.add_argument(
        '--system',
        action='store_const',
        const=True,
        help='List system albums'
    )


if __name__ == '__main__':
    parser = createParser()
    namespace = parser.parse_args(sys.argv[1:])
    if not namespace.command:
        parser.print_help()
    else:
        print(namespace)
