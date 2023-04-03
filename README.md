# twitchtube
[![License](https://img.shields.io/github/license/offish/twitchtube.svg)](https://github.com/offish/twitchtube/blob/master/LICENSE)
[![Stars](https://img.shields.io/github/stars/offish/twitchtube.svg)](https://github.com/offish/twitchtube/stargazers)
[![Issues](https://img.shields.io/github/issues/offish/twitchtube.svg)](https://github.com/offish/twitchtube/issues)
[![Size](https://img.shields.io/github/repo-size/offish/twitchtube.svg)](https://github.com/offish/twitchtube)
[![Discord](https://img.shields.io/discord/467040686982692865?color=7289da&label=Discord&logo=discord)](https://discord.gg/t8nHSvA)
[![Code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

[![Donate Steam](https://img.shields.io/badge/donate-steam-green.svg)](https://steamcommunity.com/tradeoffer/new/?partner=293059984&token=0-l_idZR)
[![Donate PayPal](https://img.shields.io/badge/donate-paypal-blue.svg)](https://www.paypal.me/0ffish)

Automatically make video compilations of the most viewed Twitch clips, and upload them to YouTube using Python 3. 

### twitchtube is currently being rewritten, which will include breaking changes
Follow the changes [here](https://github.com/offish/twitchtube/tree/v2.0.0).

## Usage
Example of making a video through terminal
```python
python main.py --data "g Just Chatting, c xQcOW, c Trainwreckstv" --client_id "1hq8ektpki36w5kn37mluioungyqjo" --oauth_token "9f5einm9qtp0bj4m9l1ykevpwdn98o" --duration 10.5 --resolution 1080 1920 --title "Top Just Chatting, xQc and Trainwrecks Twitch Clips Today" --tags "xqc, trainwrecks, twitch clips, xqc twitch, trainwrecks twitch"
```
`g` indicates game, `c` indicates channel. You can also use `channel` and `game`.

**Every parameter that is not specified, will default to an assigned value in [`config.py`](twitchtube/config.py).**

Example of running with only default values:

```text
python main.py
```

[`config.py`](twitchtube/config.py):
```python
DATA = ["channel maskenissen"]

CLIENT_ID = "1hq8ektpki36w5kn37mluioungyqjo"  # Twitch Client ID
OAUTH_TOKEN = "9f5einm9qtp0bj4m9l1ykevpwdn98o"  # Twitch OAuth Token
PERIOD = 24  # day, week, month or all
LANGUAGE = "en"  # en, es, th etc.
LIMIT = 100  # 1-100
...
```

You can also run the bot from a Python file like [`example.py`](example.py)
```python
from time import sleep
from twitchtube.video import make_video
from twitchtube.utils import get_path

while True:
    make_video(
        data=["channel xQcOW", "game Just Chatting"],
        path=get_path(),
        client_id="1hq8ektpki36w5kn37mluioungyqjo",  # example client id (fake)
        oauth_token="9f5einm9qtp0bj4m9l1ykevpwdn98o",  # example token (fake)
        video_length=10.5, # minutes as float
        resolution=(1080, 1920), # height x width
        frames=60,
        period=24, # most viewed clips today
    )
    sleep(24 * 60 * 60) # make a video daily
```

These are all the parameters `make_video` takes
```python
def make_video(
    data: list = DATA,
    blacklist: list = BLACKLIST,
    # other
    path: str = get_path(),
    check_version: bool = CHECK_VERSION,
    # twitch
    client_id: str = CLIENT_ID,
    oauth_token: str = OAUTH_TOKEN,
    period: int = PERIOD,
    language: str = LANGUAGE,
    limit: int = LIMIT,
    # selenium
    profile_path: str = ROOT_PROFILE_PATH,
    sleep: int = SLEEP,
    headless: bool = HEADLESS,
    debug: bool = DEBUG,
    # video options
    render_video: bool = RENDER_VIDEO,
    file_name: str = FILE_NAME,
    resolution: tuple = RESOLUTION,
    frames: int = FRAMES,
    video_length: float = VIDEO_LENGTH,
    resize_clips: bool = RESIZE_CLIPS,
    enable_intro: bool = ENABLE_INTRO,
    resize_intro: bool = RESIZE_INTRO,
    intro_path: str = INTRO_FILE_PATH,
    enable_transition: bool = ENABLE_TRANSITION,
    resize_transition: bool = RESIZE_TRANSITION,
    transition_path: str = TRANSITION_FILE_PATH,
    enable_outro: bool = ENABLE_OUTRO,
    resize_outro: bool = RESIZE_OUTRO,
    outro_path: str = OUTRO_FILE_PATH,
    # other options
    save_file: bool = SAVE_TO_FILE,
    save_file_name: str = SAVE_FILE_NAME,
    upload_video: bool = UPLOAD_TO_YOUTUBE,
    delete_clips: bool = DELETE_CLIPS,
    # youtube
    title: str = TITLE,
    description: str = DESCRIPTION,
    thumbnail: str = THUMBNAIL,
    tags: list = TAGS,
) -> None:
    ...
```
Information about every parameter can be found in [`config.py`](twitchtube/config.py).

## Installation
Download the repo as ZIP and unzip it somewhere accessible, or use git.

To install all the packages needed, you have to run this command, by being in the same directory as the `requirements.txt` and `main.py` files are.

```
pip install -r requirements.txt 
```

Download [geckodriver](https://github.com/mozilla/geckodriver/releases) and add it to PATH. If you are on Windows you can follow [this post](https://softwaretestingboard.com/q2a/2366/how-to-set-geckodriver-into-path-environment-variable).

You can now check if it works by running this command in the terminal:
```text
geckodriver --version
```
If geckodriver has been added to PATH, you should now see the current version number and some licensing text.

## Configuration
### Creating your Twitch Application
![image](https://user-images.githubusercontent.com/30203217/115958371-7e76c880-a507-11eb-8748-7bbc5f497a68.png)

Go to https://dev.twitch.tv/console/apps/create and register a new application.
The name of the application does not matter. Set "OAuth Redirect URLs" to https://twitchapps.com/tokengen/

Set category to "Application Integration" or "Other". 


![image](https://user-images.githubusercontent.com/30203217/115958430-cbf33580-a507-11eb-963e-14a7dccbfd7d.png)

Click "Manage".

![image](https://user-images.githubusercontent.com/30203217/115958485-eb8a5e00-a507-11eb-98f8-c01b4dabd163.png)

Copy the Client ID and go to [`config.py`](twitchtube/config.py). 
Find `CLIENT_ID` and paste it inside apostrophes.

### Getting your OAuth Token
![image](https://user-images.githubusercontent.com/30203217/115958569-402dd900-a508-11eb-8464-676b927acff5.png)

Now head over to https://twitchapps.com/tokengen/ and paste in your Client ID, which you just copied.
Scopes does not matter in our case. Click "Connect" and then authorize with Twitch.

![image](https://user-images.githubusercontent.com/30203217/115958582-5b004d80-a508-11eb-8e29-91669c71e987.png)

Copy your OAuth Token and go to [`config.py`](twitchtube/config.py), find `OAUTH_TOKEN` and paste it inside the apostrophes.

### Setting up Firefox

Open Firefox and create a new profile for Selenium, (this is not needed, but highly recommended). Go to `about:profiles` and click "Create a New profile", name it "Selenium" or whatever. 

![image](https://user-images.githubusercontent.com/30203217/115958696-c0543e80-a508-11eb-9d76-6ef5fd33e889.png)

Copy the "Root Directory" path of that profile and paste it into the `ROOT_PROFILE_PATH` in [`config.py`](twitchtube/config.py). Now click "Launch profile in new browser". Go to [YouTube](https://youtube.com) and login to the account you want to use with twitchtube.


*Don't use Selenium as your default profile.* 

You can now save your `config`.

## Troubleshooting
### Uploading
If you're having issues uploading try to update [opplast](https://github.com/offish/opplast).
```
pip install --upgrade opplast
```
Sometimes YouTube is weird, so trying multiple times *might* work. 
Set `debug=True` and `headless=False` to see what it's actually doing. Increasing `sleep` *might* also work. 
If you have configured everything correctly, and are still running into errors, leave a detailed issue [here](https://github.com/offish/opplast/issues).

## License
MIT License

Copyright (c) 2020 [offish](https://offi.sh)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
