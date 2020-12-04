# twitchtube
[![License](https://img.shields.io/github/license/offish/twitchtube.svg)](https://github.com/offish/twitchtube/blob/master/LICENSE)
[![Stars](https://img.shields.io/github/stars/offish/twitchtube.svg)](https://github.com/offish/twitchtube/stargazers)
[![Issues](https://img.shields.io/github/issues/offish/twitchtube.svg)](https://github.com/offish/twitchtube/issues)
[![Size](https://img.shields.io/github/repo-size/offish/twitchtube.svg)](https://github.com/offish/twitchtube)
[![Chat](https://img.shields.io/discord/467040686982692865.svg)](https://discord.gg/t8nHSvA)

[![Donate Steam](https://img.shields.io/badge/donate-steam-green.svg)](https://steamcommunity.com/tradeoffer/new/?partner=293059984&token=0-l_idZR)
[![Donate PayPal](https://img.shields.io/badge/donate-paypal-blue.svg)](https://www.paypal.me/0ffish)


Automatically make video compilations of the most viewed Twitch clips and upload it to YouTube using Python 3. 


## Installation
Download the repo as ZIP and unpack it somewhere accessible.

To install all the needed packages you either need to run install.bat or this command (has to be in
the right directory).

```
pip install -r requirements.txt 
```
   

## Configuration
### Creating your Twitch Application
Go to https://dev.twitch.tv/console and register a new application.
The name of the application does not matter. Set "OAuth Redirect URLs" to https://twitchapps.com/tokengen/
Set category to Application Integration or Other. 
You will now see your Client ID, copy this ID.
Go to config.py under dist, find CLIENT_ID and paste it inside apostrophes.

### Getting your OAuth Token
Now head over to https://twitchapps.com/tokengen/
Paste in your Client ID, scopes does not matter in our case. 
Click "Connect" and then authorize with Twitch.
Copy your OAuth Token, go to config.py, find OAUTH_TOKEN and paste it inside the apostrophes.

### Creating your Google Project
Go to https://console.cloud.google.com/ and create a new project.
Name does not matter.

### Enabling YouTube Data API v3
Click on the menu on the left side of your screen and navigate to "APIs & Services".
Hover over this button and click "Library".
Search for "YouTube Data API v3" and click the first result.
Enable this API. 

### Getting your client_secret
When you've clicked enable you should now be on the "Overview" tab.
Click "Credentials" and then "+ Create Credentials".
You will now see 3 options, click "OAuth client ID". 
Now you might need to configure consent screen.
If you need to configure this, click "External" and then "Create".
Write something in the application name field, might be wise to name it something you will remember like "twitchtube" or 
"YouTube Twitch Bot".
Now you will see your application, go to "Credentials" again and click "+ Create Credentials" and then "OAuth client ID".
Set application type to Desktop app and name it whatever.
Click Ok, and click the download icon.
Open the JSON file that gets downloaded, select everything and paste it into the client_secret file under dist.

### Adding/removing games
If you want to add a game/category, you simply write the name of the game how it appears on Twitch inside the GAMES list in [`config.py`](twitchtube/config.py).
If you want to add Just Chatting for example GAMES should look like this:

```python
GAMES = ['Rust', 'Just Chatting', 'Team Fortress 2']
```

Last entry in the list must not have a comma.

If only want to have 1 game/category GAMES, in this case Just Chatting it should look like this:

```python
GAMES = ['Just Chatting']
```

**EVERY ENTRY IN GAMES MUST ALSO BE FOUND IN TAGS AND DESCRIPTIONS**

Example:

```python
GAMES = ['Just Chatting']

TAGS = {
    'Just Chatting': 'just chatting, just chatting twitch, just chatting twitch highlights'
}

DESCRIPTIONS = {
    'Just Chatting': 'The most viewed Just Chatting clips today.\n\n{}\n#Twitch #TwitchHighlights #Just Chatting'
}
```

Counter-Strike: Global Offensive is currently not supported since folders can't include colons in their folder name.

## How it works
The script starts by checking every game listed in the config. It will then create a folder with 
the current date as the name and inside of this folder it will create another folder for the 
first game in the list (also specified in the config). It will send a request to Twitch's API 
and ask for the top 100 clips for that game that day. It will then save this data in a JSON 
file named `clips.json`. It will simply loop through the clip URLs and download each clip 
till it reaches the limit specifed in the config. When the limit it reached (the video is 
long enough) it will take all the mp4 files and concatenate these into 1 video. When this 
video is done rendering, it will upload it to YouTube. When the video is uploaded it will 
create a new folder for the next game in the list (if any) with the game title as folder 
name and redo the process written above.  

## Running
To run the script simply run start.bat or type python main.py in command prompt (must be in the correct folder).

## Example
[Here](https://www.youtube.com/channel/UCd0wttXr03lIcTLv38U5d-w) is an example of how the videos look like on YouTube. Majority of these videos are made using
this repo. Only a couple of titles and thumbnails have been changed.

## Note
I've only tested this script using Python 3.7.3, but should work with later versions.

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





