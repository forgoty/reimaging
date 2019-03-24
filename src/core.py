import os


class Album():
    def __init__(self, api, **kwargs):
        self.api = api
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __str__(self):
        return 'Album({}) of {} id'.format(self.id, self.owner_id)

    @property
    def link(self):
        return 'https://vk.com/{}_{}/'.format(self.owner_id, self.id)

    def get_photo_links(self):
        response = self.api.photos.get(
            owner_id=self.owner_id,
            album_id=self.id,
            photo_sizes=1,
            count=1000
        )

        photo_sizes = [item['sizes'] for item in response['items']]
        links = []

        for i in range(len(photo_sizes)):
            for item in photo_sizes[i]:
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
