import json
import re
import urllib.request
from math import floor

import requests

from .config import CLIENT_ID, OAUTH_TOKEN, PARAMS, HEADERS
from .logging import log

log = log()


def get_clip_data(slug: str):
    clip_info = get_data(slug)

    if 'thumbnail_url' in clip_info \
        and 'title' in clip_info:
        thumb_url = clip_info['thumbnail_url']
        title = clip_info['title']
        slice_point = thumb_url.index('-preview-')
        mp4_url = thumb_url[:slice_point] + '.mp4'

        return mp4_url, title

    raise TypeError(f'Twitch didn\'t send what we wanted as response (could not find \'data\' in response). Response from /helix/ API endpoint:\n{clip_info}')


def get_progress(count, block_size, total_size):
    percent = int(count * block_size * 100 / total_size)
    print(f'Downloading clip... {percent}%', end='\r', flush=True)


def get_slug(clip: str):
    slug = clip.split('/')
    return slug[len(slug) - 1]


def download_clip(clip: str, basepath: str):
    slug = get_slug(clip)
    mp4_url, clip_title = get_clip_data(slug)
    regex = re.compile('[^a-zA-Z0-9_]')
    clip_title = clip_title.replace(' ', '_')
    out_filename = regex.sub('', clip_title) + '.mp4'
    output_path = (basepath + '/' + out_filename)

    log.info(f'Downloading clip with slug: {slug}.')
    log.info(f'Saving "{clip_title}" as "{out_filename}".')
    urllib.request.urlretrieve(mp4_url, output_path, reporthook=get_progress)
    log.info(f'{slug} has been downloaded.')


def get_data(slug: str) -> dict:
    _params = {'id': slug}
    _headers = {
        'Authorization': 'Bearer ' + OAUTH_TOKEN,
        'Client-Id': CLIENT_ID
    }
    response = requests.get('https://api.twitch.tv/helix/clips',
        headers=_headers, params=_params)

    return response.json()['data'][0]


def get_clips(game: str, length: float, path: str):
    length *= 60
    data = {}

    PARAMS['game'] = game

    response = requests.get('https://api.twitch.tv/kraken/clips/top',
        headers=HEADERS, params=PARAMS).json()

    if 'clips' in response:

        for clip in response['clips']:
            data[clip['tracking_id']] = {
                'url': 'https://clips.twitch.tv/' + clip['slug'],
                'title': clip['title'],
                'display_name': clip['broadcaster']['display_name'],
                'duration': clip['duration']
            }

        with open(f'{path}/clips.json', 'w') as f:
            json.dump(data, f, indent=4)

        return data

    else:
        log.error(f'Could not find \'clips\' in response. {response}')

        return False


def download_clips(data: dict, length: float, path: str):
    length *= 60
    names = []

    for clip in data:

        download_clip(data[clip]['url'], path)
        length -= data[clip]['duration']

        name = data[clip]['display_name']

        if name not in names:
            names.append(name)
        
        log.info(f'Remaining video length: {floor(length)} seconds.\n')

        if length <= 0:
            log.info('Downloaded all clips.\n')
            return names
        else:
            continue
