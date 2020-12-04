from datetime import date
import json

from .config import *


def get_date() -> str:
    return date.today().strftime('%b-%d-%Y')


def create_video_config(game, streamers) -> dict:
    return {
        'category': CATEGORY,
        'keywords': get_tags(game),
        'description': get_description(game, streamers),
        'title': get_title(game),
        'file': get_file(game)
    }


def get_tags(game) -> str:
    return TAGS.get(game)


def get_description(game, streamers) -> str:
    names = 'Streamers in this video:\n'
    
    for name in streamers:
        names += f'https://twitch.tv/{name}\n'

    if game in DESCRIPTIONS:
        return DESCRIPTIONS[game].format(names)
    return names


def get_title(game) -> str:
    if TITLE:
        return TITLE

    title = json.loads(open(f'{CLIP_PATH.format(get_date(), game)}/clips.json', 'r').read())
    
    for i in title:
        return f"{title[i]['title']} - {game} Twitch Highlights"


def get_file(game) -> str:
    return f'{CLIP_PATH.format(get_date(), game)}/{FILE_NAME}.mp4'
