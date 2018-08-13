import sys
import argparse


version = 'v0.0.3'

def createParser():
    parser = argparse.ArgumentParser(
                    prog = 'reimaging',
                    description = '''Simple photo downloader from vk.com''',
                    add_help = False)

    parent_group = parser.add_argument_group(title='Params')
    parent_group.add_argument('--help', '-h', action='help', help='Help')
    parent_group.add_argument('--version',
                    action='version',
                    help = 'reimaging version',
                    version='%(prog)s {}'.format(version))

    subparsers = parser.add_subparsers(dest='command',
                    title='Commands',)

    create_download_parser(subparsers)

    return parser


def create_download_parser(subparsers):
    download_parser = subparsers.add_parser('download', add_help = False,
                    description=
                    '''Download photos to local drive.''')

    download_group = download_parser.add_argument_group(title='Params')

    download_group.add_argument('-a', '--auth', action='store_const',
                                                const=True,
                    help='''Enable authorization for downloading
                    private albums''')

    download_group.add_argument('-o', '--owner', type=int, required=True,
                    help='''Takes an owner ID for download all owner
                    albums. By default download all albums
                    at working directory. Type "-" in front of
                    owner ID to download group photos''')

    download_group.add_argument('-p', '--path',
                    help='Changes download folder')

    download_group.add_argument('--album_id', type=int,
                    help='Download only owner album by album id')

    download_group.add_argument('--system', action='store_const', const=True,
                    help='''Download system albums. If album ID is not set,
                    download all system albums.
                    Album ID for profile photos = -6.
                    Album ID for wall photos = -7.
                    Album ID for saved photos = -15.''')

    download_group.add_argument('--help', '-h', action='help', help='Help')


if __name__ == '__main__':
    parser = createParser()
    namespace = parser.parse_args(sys.argv[1:])
    if not namespace.command:
        parser.print_help()
    else:
        print(namespace)