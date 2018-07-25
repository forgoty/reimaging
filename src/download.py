import os
from tqdm import tqdm
from auth import auth
import requests
from multiprocessing import Pool, cpu_count


class DownloadService():

    def __init__(self, user, path=None):
        if path:
            self.path = path
        else:
            self.path = os.getcwd()

        self.user = user
        self.api = auth()

        try:
            albums = self.api.photos.getAlbums(owner_id=user)
        except:
            print('Something went wrong. Check input parameters.')
            exit(1)

        self.albums = []
        for item in albums.get('items'):
            dict_buffer = dict.fromkeys(['id', 'title', 'size'])
            dict_buffer.update([('id', item.get('id')),
                                    ('title', item.get('title')),
                                    ('size', item.get('size'))])

            self.albums.append(dict_buffer)

    def download_album(self, album_id):
        links = self.get_photo_links(album_id)
        title = self.get_album_title(album_id)
        os.makedirs(os.path.join(self.path, title), exist_ok=True)
        args = tuple((link, self.path, title) for link in links)

        with Pool(processes=cpu_count()) as pool:
            for _ in tqdm(pool.imap_unordered(self.download_routine, args),
                                            total=len(links), ascii=True,
                                            desc=title, unit='photo'):
                pass

    def get_photo_links(self, album_id):
        try:
            response = self.api.photos.get(owner_id=self.user,
                                        album_id=album_id,
                                        photo_sizes=1)
        except:
            print('Something went wrong. Check input parameters.')
            exit(1)

        sizes = [item.get('sizes') for item in response.get('items')]
        links = []

        for i in range(len(sizes)):
            for item in sizes[i]:
                if item.get('type') == 'w':
                    links.append(item.get('src'))
                    break
                elif item.get('type') == 'z':
                    links.append(item.get('src'))
                    break
                elif item.get('type') == 'y':
                    links.append(item.get('src'))
                    break
                elif item.get('type') == 'x':
                    links.append(item.get('src'))
                    break

        return links

    def get_album_title(self, album_id):
        for item in self.albums:
            if item.get('id') == album_id:
                title = item.get('title')
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
    profile = DownloadService(user=1)
    for item in profile.albums:
        profile.download_album(item.get('id'))
