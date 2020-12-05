from math import ceil
from json import dump
import urllib.request
import re

from .config import CLIENT_ID, OAUTH_TOKEN, PARAMS, HEADERS
from .logging import Log

import requests


log = Log()


def get_data(slug: str) -> dict:
    """
    Gets the data from a given slug,
    returns a JSON respone from the Helix API endpoint
    """
    response = requests.get(
        'https://api.twitch.tv/helix/clips',
        headers={
            'Authorization': 'Bearer ' + OAUTH_TOKEN,
            'Client-Id': CLIENT_ID
        },
        params={
            'id': slug
        }
    ).json()

    try:
        return response['data'][0]
    except KeyError as e:
        log.error(f'Ran into exception: {e}')
        log.error(f'Response: {response}')
        return response


def get_clip_data(slug: str) -> tuple:
    """
    Gets the data for given slug, returns a tuple first
    entry being the mp4_url used to download the clip,
    second entry being the title of the clip to be used as filename.
    """
    clip_info = get_data(slug)

    if 'thumbnail_url' in clip_info \
        and 'title' in clip_info:
        # All to get what we need to return 
        # the mp4_url and title of the clip
        thumb_url = clip_info['thumbnail_url']
        title = clip_info['title']
        slice_point = thumb_url.index('-preview-')
        mp4_url = thumb_url[:slice_point] + '.mp4'

        return mp4_url, title

    raise TypeError(f'Twitch didn\'t send what we wanted as response (could not find \'data\' in response). Response from /helix/ API endpoint:\n{clip_info}')


def get_progress(count, block_size, total_size) -> None:
    """
    Used for printing the download progress
    """
    percent = int(count * block_size * 100 / total_size)
    print(f'Downloading clip... {percent}%', end='\r', flush=True)


def get_slug(clip: str) -> str:
    """
    Splits up the URL given and returns the slug
    of the clip.
    """
    slug = clip.split('/')
    return slug[len(slug) - 1]


def download_clip(clip: str, basepath: str) -> None:
    """
    Downloads the clip, does not return anything.
    """
    slug = get_slug(clip)
    mp4_url, clip_title = get_clip_data(slug)
    # Remove special characters so we can save the video 
    regex = re.compile('[^a-zA-Z0-9_]')
    clip_title = clip_title.replace(' ', '_')
    out_filename = regex.sub('', clip_title) + '.mp4'
    output_path = (basepath + '/' + out_filename)

    log.info(f'Downloading clip with slug: {slug}.')
    log.info(f'Saving "{clip_title}" as "{out_filename}".')
    # Download the clip with given mp4_url
    urllib.request.urlretrieve(mp4_url, output_path, reporthook=get_progress)
    log.info(f'{slug} has been downloaded.')


def get_clips(game: str, path: str) -> dict:
    """
    Gets the top clips for given game, returns JSON response
    from the Kraken API endpoint.
    """
    data = {}

    PARAMS['game'] = game

    response = requests.get(
        'https://api.twitch.tv/kraken/clips/top',
        headers = HEADERS, 
        params = PARAMS
    ).json()

    if 'clips' in response:

        for clip in response['clips']:
            data[clip['tracking_id']] = {
                'url': 'https://clips.twitch.tv/' + clip['slug'],
                'title': clip['title'],
                'display_name': clip['broadcaster']['display_name'],
                'duration': clip['duration']
            }

        # Save the data to a JSON file
        with open(f'{path}/clips.json', 'w') as f:
            dump(data, f, indent=4)

        return data

    else:
        log.error(f'Could not find \'clips\' in response. {response}')

        return {}


def download_clips(data: dict, length: float, path: str) -> list:
    """
    Downloads clips, returns a list of streamer names.
    """
    amount = 0
    length *= 60
    names = []

    for clip in data:

        download_clip(data[clip]['url'], path)
        length -= data[clip]['duration']

        name = data[clip]['display_name']
        amount += 1

        if name not in names:
            names.append(name)
        
        log.info(f'Remaining video length: {ceil(length)} seconds.\n')

        # If the rendered video would be long enough
        # we break out of the loop, else continue
        if length <= 0:
            break
    
    # If the rendered video would be long enough or we
    # have ran out of clips, we return the streamer names
    log.info(f'Downloaded {amount} clips.\n')
    return names
