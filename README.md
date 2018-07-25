# reimaging
reimaging is simple photo downloader for vk.com using CLI.
### Requirements
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
You will need an user ID and album ID. Album ID is optional.
![N|Solid](https://image.ibb.co/fRpaDo/image.png)
First number - user ID (1).
Second number - album ID (136592355)
### Launch Examples
```sh
$ python main.py download -u 53083705 -p ~/download-folder --album_id 255217256
# download single album of user by ID`s
$ python main.py download -u 1 #download all albums of user
```

### Todos

 - Fix some bugs
 - Add upload mode
 - Add installation script
 - Test on Windows machine
 - Improve README.md
