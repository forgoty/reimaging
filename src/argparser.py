import sys
import argparse


version = '0.0.1'

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
                    '''Takes an user ID for download all user
                    albums. By default download all open albums
                    at working directory. After connection lost or
                    folder problems, downloading proccess will resume
                    after second command call''')

    download_group = download_parser.add_argument_group(title='Params')
    download_group.add_argument('-u', '--user', type=int, required=True,
                    help='Takes ID. Required parameter',)

    download_group.add_argument('-p', '--path',
                    help='Changes download folder')

    download_group.add_argument('--album_id', type=int,
                    help='Download only user album by album id')

    download_group.add_argument('--help', '-h', action='help', help='Help')


if __name__ == '__main__':
    parser = createParser()
    namespace = parser.parse_args(sys.argv[1:])
    if not namespace.command:
        parser.print_help()
    else:
        print(namespace.album_id)