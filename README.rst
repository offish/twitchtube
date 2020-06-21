twitchtube
==========
|license| |stars| |issues| |repo_size| |chat|

|donate_steam| |donate|

Automatically make a compilation of the most viewed daily clips on Twitch, and upload the video to YouTube using Python 3. 

.. contents:: Table of Contents
    :depth: 1

Installation
------------

.. code-block:: text

    pip install -r requirements.txt 

Setup
-----

In the `config.py` file you need to have set the `CLIENT_ID` to your Twitch Client ID.

Get `OAUTH_TOKEN` by going to `twitchapps`_.

https://dev.twitch.tv/console/apps/create

You need to have a `client_secret.json` file in dist that looks something like this.

.. _twitchapps: https://twitchapps.com/tokengen/

.. code-block:: json

    {
        "installed": {
            "client_id": "example.apps.googleusercontent.com",
            "project_id": "example-111111",
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_secret": "example",
            "redirect_uris": [
                "urn:ietf:wg:oauth:2.0:oob",
                "http://localhost"
            ]
        }
    }

And you also need a `credentials.json` file under the credentials folder that looks something like this.

.. code-block:: json

    "{\"token\": \"example\", \"expiry\": null, \"_scopes\": null, \"_refresh_token\": \"example\", \"_id_token\": null, \"_token_uri\": \"https://oauth2.googleapis.com/token\", \"_client_id\": \"example.apps.googleusercontent.com\", \"_client_secret\": \"example\"}"


How it works
------------
The script starts by checking every game listed in the config. It will then create a folder with the current date as the name and inside of this folder it will create another folder for the first game in the list (also specified in the config). It will send a request to Twitch's API and ask for the top 100 clips for that game that day. It will then save this data in a JSON file named `clips.json`. It will simply loop through the clip URLs and download each clip till it reaches the limit specifed in the config. When the limit it reached (the video is long enough) it will take all the mp4 files and concatenate these into 1 video. When this video is done rendering, it will upload it to YouTube. When the video is uploaded it will create a new folder for the next game in the list (if any) with the game title as folder name and redo the process written above.  

Example
-------
`Here`_ is an example of how the videos turn out on YouTube (made with this repo)

.. _Here: https://www.youtube.com/channel/UCd0wttXr03lIcTLv38U5d-w

License
-------
MIT License

Copyright (c) 2020 `offish`_

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

.. _offish: https://offi.sh

.. |license| image:: https://img.shields.io/github/license/offish/twitchtube.svg
    :target: https://github.com/offish/twitchtube/blob/master/LICENSE
    :alt: License

.. |stars| image:: https://img.shields.io/github/stars/offish/twitchtube.svg
    :target: https://github.com/offish/twitchtube/stargazers
    :alt: Stars

.. |issues| image:: https://img.shields.io/github/issues/offish/twitchtube.svg
    :target: https://github.com/offish/twitchtube/issues
    :alt: Issues

.. |repo_size| image:: https://img.shields.io/github/repo-size/offish/twitchtube.svg
    :target: https://github.com/offish/twitchtube
    :alt: Repo Size

.. |chat| image:: https://img.shields.io/discord/467040686982692865.svg
    :target: https://discord.gg/t8nHSvA
    :alt: Discord

.. |donate_steam| image:: https://img.shields.io/badge/donate-steam-green.svg
    :target: https://steamcommunity.com/tradeoffer/new/?partner=293059984&token=0-l_idZR
    :alt: Donate via Steam

.. |donate| image:: https://img.shields.io/badge/donate-paypal-blue.svg
    :target: https://www.paypal.me/0ffish
    :alt: Done via PayPal
