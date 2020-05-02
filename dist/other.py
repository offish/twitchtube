from datetime import date
import json

from .config import TAGS, DESCRIPTIONS, CLIP_PATH


def get_date():
    return date.today().strftime("%b-%d-%Y")


def create_video_config(game, streamers):
    config = {
        "category": 20,
        "keywords": get_tags(game),
        "description": get_description(game, streamers),
        "title": get_title(game),
        "file": get_file(game)
    }

    return config


def get_tags(game):
    return TAGS[game]


def get_description(game, streamers):
    names = "Streamers in this video:\n"
    
    for name in streamers:
        names += f'https://twitch.tv/{name}\n'

    return DESCRIPTIONS[game].format(names)


def get_title(game):
    title = json.loads(open(f'{CLIP_PATH.format(get_date(), game)}/clips.json', 'r').read())

    for i in title:
        return f"{title[i]['title']} - {game} Highlights #"


def get_file(game):
    return f"{CLIP_PATH.format(get_date(), game)}/rendered.mp4"
