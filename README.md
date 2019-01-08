# reimaging
reimaging is simple photo downloader/uploader for vk.com using CLI for UNIX.
### Requirements
- Python 3.7
- pyvk (https://github.com/mkuznets/pyvk)
- tqdm

```sh
$ pip install git+https://github.com/mkuznets/pyvk.git
$ pip install tqdm
```

### Installation
Just cd to source folder and type:
```sh
$ python setup.py install
```

### Using
First of all, view help:
```sh
$ reimaging --help
$ reimaging download --help #for download help
$ reimaging upload --help #for upload help
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
$ reimaging download -o 53083705 -p ~/download-folder --album_id 255217256 #download single album of owner by ID`s
$ reimaging download -o 1 #download all albums
$ reimaging download -o -17566514 # for group albums
$ reimaging download -a -o "owner id" #Downloading with login
$ reimaging download -a -o "owner id" --system #for download all albums including system albums too.
$ reimaging download -a -o "owner id" --system --album_id -15 # for downloading saved photos album
$ reimaging upload -p "path" -t "title" #Upload photos from "path" to Album with "title"
$ reimaging upload -p "path" --album_id "album_id" # Update Album with "album_id" with photos form "path"
$ reimaging list -a --system 1 # View album list with system albums
```

### Todos

 - More testing
 - Make it for Windows
 - Rewrite using AsyncIO

For any problems and bugs please report to Issues.
