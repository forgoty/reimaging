import os
from tqdm import tqdm
from auth import auth
import pickle
import requests
from sys import exit


class DownloadService():

    def __init__(self, user, path):
        if path:
            self.path = os.getcwd()
        else:
            self.path = path


        self.api = auth()

        try:
            albums = self.api.photos.getAlbums(owner_id=user)
        except:
            print('Something went wrong. Check input parameters.')
            exit(1)

        albums_items = albums.get('items')

        self.user = user
        self.album_count = albums.get('count')

        self.albums = []
        for item in albums_items:
            d = dict.fromkeys(['id', 'title', 'size'])
            d.update([('id', item.get('id')),
                                    ('title', item.get('title')),
                                    ('size', item.get('size'))])

            self.albums.append(d)

    def download_album(self, album_id):
        links = self.get_links(album_id)
        self.create_folder(album_id)
        title = self.get_album_title(album_id)
        linkStorage = links.copy()

        for link in tqdm(links, desc=title, unit='photo'):
            try:
                response = requests.get(link)
                if response.status_code == 200:
                    with open(os.path.join(self.path, title,
                                        link[len(link)-10:]), 'wb') as f:

                        f.write(response.content)
                linkStorage.remove(link)
            except (Exception, requests.exceptions.RequestException) as err:
                print('Something went wrong. ' +
                'Check connection or download folder and try again')
                self.create_dump(album_id, linkStorage)
                exit(1)

    def get_links(self, album_id):
        title = self.get_album_title(album_id)

        if os.path.exists(os.path.join(self.path, title, 'links.bin')):
            with open(os.path.join(self.path, title, 'links.bin'), 'rb') as f:
                links = pickle.load(f)
                os.remove(os.path.join(self.path, title, 'links.bin'))
        else:
            links = self.get_photo_links(album_id)

        return links

    def create_dump(self, album_id, data):
        title = self.get_album_title(album_id)
        with open(os.path.join(self.path, title,
                                        'links.bin'), 'wb') as file:

            pickle.dump(data, file)

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

    def get_album_size(self, album_id):
            for item in self.albums:
                if item.get('id') == album_id:
                    size = item.get('size')
                    return size
            else:
                print('Something went wrong. Check input parameters.')
                exit(1)

    def create_folder(self, album_id):
        title = self.get_album_title(album_id)
        os.makedirs(os.path.join(self.path, title), exist_ok=True)


if __name__ == '__main__':
    a = DownloadService(user=1)
    for item in a.albums:
        a.download_album(item.get('id'))
