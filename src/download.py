import os
from tqdm import tqdm
import requests
from multiprocessing import Pool, cpu_count
from pyvk.exceptions import APIError


class DownloadService():

    def __init__(self, api, owner, path=None, system=0):
        if path:
            self.path = path
        else:
            self.path = os.getcwd()

        self.owner = owner
        self.api = api

        try:
            albums_response = api.photos.getAlbums(owner_id=owner,
                                                    need_system=system)
        except APIError as exc:
            print('Error %d: %s' % (exc.error_code, exc.error_msg))
            exit(1)

        self.albums = []
        for item in albums_response['items']:

            dict_buffer = dict.fromkeys(['id', 'title', 'size'])
            dict_buffer.update([('id', item['id']),
                                    ('title', item['title']),
                                    ('size', item['size'])])

            self.albums.append(dict_buffer)

    def download_album(self, album_id):
        links = self.get_photo_links(album_id)
        title = self.get_album_title(album_id)
        os.makedirs(os.path.join(self.path, title), exist_ok=True)
        args = tuple((link, self.path, title) for link in links)

        with Pool(processes=cpu_count()) as pool:
            for _ in tqdm(pool.imap_unordered(self.download_routine, args),
                                            total=len(links), ascii=True,
                                            desc=title, unit=' photos'):
                pass

    def get_photo_links(self, album_id):

        try:
            response = self.api.photos.get(owner_id=self.owner,
                                        album_id=album_id,
                                        photo_sizes=1)
        except APIError as exc:
            print('Error %d: %s' % (exc.error_code, exc.error_msg))
            exit(1)

        sizes = [item['sizes'] for item in response['items']]
        links = []

        for i in range(len(sizes)):
            for item in sizes[i]:
                if item['type'] == 'w':
                    links.append(item['src'])
                    break
                elif item['type'] == 'z':
                    links.append(item['src'])
                    break
                elif item['type'] == 'y':
                    links.append(item['src'])
                    break
                elif item['type'] == 'x':
                    links.append(item['src'])
                    break

        return links

    def get_album_title(self, album_id):
        for item in self.albums:
            if item['id']== album_id:
                title = item['title']
                return title
        else:
            print('Something went wrong. Check input parameters.')
            exit(1)

    @staticmethod
    def download_routine(data):
        link = data[0]
        path = data[1]
        title = data[2]
        path_to_file = os.path.join(path, title, link[len(link)-10:])

        if os.path.exists(path_to_file):
            return

        response = requests.get(link)
        if response.status_code == 200:
            with open(path_to_file, 'wb') as f:
                f.write(response.content)


if __name__ == '__main__':
    import auth
    profile = DownloadService(api=auth.get_user_api(), owner=1, system=1)
    for item in profile.albums:
        profile.download_album(item['id'])
