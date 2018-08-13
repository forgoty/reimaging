# reimaging
reimaging is simple photo downloader for vk.com using CLI.
### Requirements
- Tested only in python 3.7
- pyvk
- tqdm
```sh
$ pip install pyvk
$ pip install tqdm
```
### Using
First of all, view help:
```sh
$ python main.py --help
$ python main.py download --help #for download help
```
You will need an owner ID and album ID. Album ID is optional.

![N|Solid](https://image.ibb.co/fRpaDo/image.png)

First number - owner ID (1).
Second number - album ID (136592355).

If you want to download group photo:

![N|Solid](https://image.ibb.co/gGoJve/image.png)

Owner ID will be with "-".

If you want to download system albums, but not them all, you can use **--system** and **--album_id** with next album_id`s:
* **-6** - for profile`s photos
* **-7** - for wall photos
* **-15** - for saved photos

Unfortunately, VK API do not allow to download more than 1000 photos.

### Launch Examples
```sh
$ python main.py download -o 53083705 -p ~/download-folder --album_id 255217256 #download single album of owner by ID`s
$ python main.py download -o 1 #download all albums
$ python main.py download -o -17566514 # for group albums
$ python main.py download -a -o "owner id" #Downloading with login
$ python main.py download -a -o "owner id" --system #for download all albums including system albums too.
$ python main.py download -a -o "owner id" --system --album_id -15 # for donwloading saved photos album
```

### Todos

 - More testing
 - Add upload mode
 - Add installation script
 - Test on Windows machine

For any problems and bugs please report to Issues.
