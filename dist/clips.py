import json
import re
import urllib.request
from math import floor

import requests

from .config import CLIENT_ID, PARAMS, HEADERS
from .logging import log


def get_clip_data(slug: str):
    clip_info = get_data(slug)
    thumb_url = clip_info['data'][0]['thumbnail_url']
    title = clip_info['data'][0]['title']
    slice_point = thumb_url.index("-preview-")
    mp4_url = thumb_url[:slice_point] + '.mp4'

    return mp4_url, title


def get_progress(count, block_size, total_size):
    percent = int(count * block_size * 100 / total_size)
    print(f"Downloading clip... {percent}%", end="\r", flush=True)


def get_slug(clip: str):
    slug = clip.split('/')

    return slug[len(slug) - 1]


def download_clip(clip: str, basepath: str):
    # clip er url
    slug = get_slug(clip)
    mp4_url, clip_title = get_clip_data(slug)
    regex = re.compile('[^a-zA-Z0-9_]')
    clip_title = clip_title.replace(' ', '_')
    out_filename = regex.sub('', clip_title) + '.mp4'
    output_path = (basepath + '/' + out_filename)

    log('info', f'Downloading clip with slug: {slug}')
    log('info', f'Saving "{clip_title}" as "{out_filename}"')
    urllib.request.urlretrieve(mp4_url, output_path, \
        reporthook=get_progress)
    log('info', 'Clip were successfully downloaded')


def get_data(slug: str) -> dict:
    url = f'https://api.twitch.tv/helix/clips?id={slug}'
    headers = {'Client-ID': CLIENT_ID}
    res = requests.get(url, headers=headers)

    try:
        return res.json()
    except ValueError:
        return {'success': False, 'text': res.text}


def get_clips(game: str, length: int, path: str):
    length *= 60
    data = {}

    PARAMS["game"] = game

    response = requests.get("https://api.twitch.tv/kraken/clips/top",
        headers=HEADERS, params=PARAMS).json()

    if 'clips' in response:

        for clip in response["clips"]:
            data[clip["tracking_id"]] = {
                "url": "https://clips.twitch.tv/" + clip["slug"],
                "title": clip["title"],
                "display_name": clip["broadcaster"]["display_name"],
                "duration": clip["duration"]
            }

        with open(f"{path}/clips.json", "w") as f:
            json.dump(data, f, indent=4)

        return data

    else:
        # error hos twitch eller timed out
        print(response)
        #log('error', response)

        return False


def download_clips(data: dict, length: int, path: str):
    length *= 60
    names = []

    for clip in data:

        download_clip(data[clip]["url"], path)
        length -= data[clip]["duration"]

        name = data[clip]["display_name"]

        if name not in names:
            names.append(name)
        
        log('info', f"Remaining video length: {floor(length)} seconds\n")

        if length <= 0:
            log('info', "Downloaded all clips.\n")
            return names
        else:
            continue
