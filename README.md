# twitchtube
Automatically make a compilation of the most viewed daily clips on Twitch, and upload the video to YouTube using Python 3. 

# Installation
```
pip install -r requirements.txt 
```

# Setup
In the `config.py` file you need to have set the `CLIENT_ID` to your Twitch client id.

You need to have a `client_secret.json` file in dist that looks something like this.
```json
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
```

And you also need a `credentials.json` file under the credentials folder that looks something like this.
``` json
"{\"token\": \"example\", \"expiry\": null, \"_scopes\": null, \"_refresh_token\": \"example\", \"_id_token\": null, \"_token_uri\": \"https://oauth2.googleapis.com/token\", \"_client_id\": \"example.apps.googleusercontent.com\", \"_client_secret\": \"example\"}"
```

# How it works
It makes video by sending a request to Twitch and gets the top 100 viewed clips for the game it's given. Then it will save that data in a JSON file and loop through each link in the file and download the clip as an mp4. When the video is long enough it will upload the video to YouTube. When the video is uploaded it will create the next video if it's given multiple games. When it's done it will check each hour if there already made a video for today (by checking folder date by name). If there is not made a folder with the current date as folder name, it will start to make a video.

# Example
[Here is an example of how the videos turn out on YouTube (made by me with this repo)](https://www.youtube.com/channel/UCd0wttXr03lIcTLv38U5d-w)


# Todo
* Add support for Counter-Strike: Global Offensive (does not work because folders cant include colons)
* Fix video length "bug" (video is sometimes shorter than the given minimum)

Thank you [Gobot1234](https://github.com/Gobot1234), for contributing to this repository.
