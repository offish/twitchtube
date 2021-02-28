# twitchtube
[![License](https://img.shields.io/github/license/offish/twitchtube.svg)](https://github.com/offish/twitchtube/blob/master/LICENSE)
[![Stars](https://img.shields.io/github/stars/offish/twitchtube.svg)](https://github.com/offish/twitchtube/stargazers)
[![Issues](https://img.shields.io/github/issues/offish/twitchtube.svg)](https://github.com/offish/twitchtube/issues)
[![Size](https://img.shields.io/github/repo-size/offish/twitchtube.svg)](https://github.com/offish/twitchtube)
[![Discord](https://img.shields.io/discord/467040686982692865?color=7289da&label=Discord&logo=discord)](https://discord.gg/t8nHSvA)
[![Code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

[![Donate Steam](https://img.shields.io/badge/donate-steam-green.svg)](https://steamcommunity.com/tradeoffer/new/?partner=293059984&token=0-l_idZR)
[![Donate PayPal](https://img.shields.io/badge/donate-paypal-blue.svg)](https://www.paypal.me/0ffish)

Automatically make video compilations of the most viewed Twitch clips and upload them to YouTube using Python 3. 

## Features
* Downloads the most popular clips from given `channel` or `game`
* Downloads only the needed clips to reach `VIDEO_LENGTH`
* Uploads automatically to YouTube using Selenium and Firefox
* Customizable
* Option for concatenating clips into one video 
* Option for custom intro, transition and outro
* Option for custom resolution
* Option for custom frame rate
* Option for minimum video length
* Option for automatically uploading to YouTube
* Option for creating a JSON file with title, description and tags for given category
* Option for automatically deleting clips after renderering

## Example
![Screenshot](https://user-images.githubusercontent.com/30203217/103347433-4e5a7400-4a97-11eb-833a-0f5d59b0cd7e.png)

[Here](https://www.youtube.com/channel/UCd0wttXr03lIcTLv38U5d-w) is an example of how the videos look like on YouTube. Majority of these videos are made using
this repo. Only a couple of titles and thumbnails have been changed.

## Installation
Download the repo as ZIP and unzip it somewhere accessible.

To install all the packages needed, you have to run this command. Has to be in same directory as the `requirements.txt` and `main.py` files are.

```
pip install -r requirements.txt 
```

Download [geckodriver](https://github.com/mozilla/geckodriver/releases) and place the .exe file inside `C:\Users\USERNAME\AppData\Local\Programs\Python\Python37`.

## Configuration
### Creating your Twitch Application
Go to https://dev.twitch.tv/console and register a new application.
The name of the application does not matter. Set "OAuth Redirect URLs" to https://twitchapps.com/tokengen/
Set category to "Application Integration" or "Other". 
You will now see your Client ID, copy this ID.
Go to [`config.py`](twitchtube/config.py), find `CLIENT_ID` and paste it inside apostrophes.

### Getting your OAuth Token
Now head over to https://twitchapps.com/tokengen/ and paste in your Client ID.
Scopes does not matter in our case. Click "Connect" and then authorize with Twitch.
Copy your OAuth Token, go to [`config.py`](twitchtube/config.py), find `OAUTH_TOKEN` and paste it inside the apostrophes.

### Setting up Firefox
Open Firefox and create a new profile for Selenium, (this is not needed, but highly recommended). Go to `about:profiles` and click "Create a New profile", name it "Selenium" or whatever. When you have done that, copy the "Root Directory" path of that profile and paste it into the `ROOT_PROFILE_PATH` in [`config.py`](twitchtube/config.py). Now click "Launch profile in new browser". Go to [YouTube](https://youtube.com) and login to the account you want to use with twitchtube. Voilà, you are now set. 
*Don't use Selenium as your default profile.* 

### Adding and removing games or channels to LIST
**`LIST` MUST MATCH `MODE`. IF `MODE` IS SET TO `GAME`, THERE SHOULD ONLY BE GAMES INSIDE OF `LIST`, SAME GOES FOR `CHANNEL`.**

If you want to add a game or channel, you simply write the name of the game or channel, how it appears on Twitch, inside the `LIST` in [`config.py`](twitchtube/config.py).
If you want to add Rust for example, then `LIST` should look like this:

```python
LIST = ["Rust", "Just Chatting", "Team Fortress 2"]
```

Last entry in the list should not have a comma.

If you only want to have one game or channel, `LIST` should look like this:

```python
LIST = ["Just Chatting"]
```

Example:

```python
MODE = "game"

LIST = ["Just Chatting"]

TITLE = "Most Viewed Just Chatting Clips - 14.02.2021"

DESCRIPTIONS = {
    "Just Chatting": "The most viewed Just Chatting clips today.\n\n{}\n #Twitch #TwitchHighlights #Just Chatting"
}

THUMBNAILS = {
    "Just Chatting": "path/to/file.jpg"
}

# Currently not supported
TAGS = {
    "Just Chatting": "just chatting, just chatting twitch, just chatting twitch highlights"
}
```

or

```python
MODE = "channel"

LIST = ["xQcOW"]

TITLE = "Most Viewed xQc Clips - 14.02.2021"

DESCRIPTIONS = {
    "xQcOW": "The most viewed xQc clips today.\n\n{}\n #Twitch #TwitchHighlights #xQcOW"
}

THUMBNAILS = {
    "xQcOW": "path/to/file.jpg"
}

# Currently not supported
TAGS = {
    "xQcOW": "xqc, xqc twitch, xqc twitch highlights"
}
```

## Running
To run the bot, use this command. Has to be in same directory as the  `requirements.txt` and `main.py` files are.

```
python main.py
``` 

## Note
I've only tested this bot using Windows 10 and Python 3.7.3, but should work with other operating systems, and Python 3 versions.

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
