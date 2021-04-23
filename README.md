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

## Usage
```
python main.py -data "game Just Chatting" "channel xQcOW" --video_length 5.3 --title "my original title"
```

or you can make and run a file like  `example.py`

```
python example.py
```

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

### Example config
```python
TITLE = "Most Viewed Just Chatting Clips - 14.02.2021"

DESCRIPTION = "Streamers in this video:\n"

THUMBNAIL = ""

TAGS = ["twitch", "just chatting", "xqc"]
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
