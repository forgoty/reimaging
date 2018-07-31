# reimaging
reimaging is simple photo downloader for vk.com using CLI.
### Requirements
- Tested only in python 3.6
- vk-requests
- tqdm
```sh
$ pip install vk-requests
$ pip install tqdm
```
### Using
First of all, view help
```sh
$ python main.py --help
```
You will need an owner ID and album ID. Album ID is optional.

![N|Solid](https://image.ibb.co/fRpaDo/image.png)

First number - owner ID (1).
Second number - album ID (136592355).

If you want to download group photo:

![N|Solid](https://image.ibb.co/gGoJve/image.png)

Album ID will be with "-" in front of owner ID

### Launch Examples
```sh
$ python main.py download -o 53083705 -p ~/download-folder --album_id 255217256 #download single album of owner by ID`s
$ python main.py download -o 1 #download all albums
$ python main.py download -o -17566514 # for group albums
```

### Todos

 - More testing
 - Add upload mode
 - Add installation script
 - Test on Windows machine
 - Improve README.md


