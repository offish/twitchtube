from datetime import date
import json

from .config import TAGS, DESCRIPTIONS, CLIP_PATH, TITLE


def get_date():
    return date.today().strftime('%b-%d-%Y')


def create_video_config(game, streamers) -> dict:
    return {
        'category': 20,
        'keywords': get_tags(game),
        'description': get_description(game, streamers),
        'title': get_title(game),
        'file': get_file(game)
    }


def get_tags(game):
    return TAGS.get(game)


def get_description(game, streamers):
    names = 'Streamers in this video:\n'
    
    for name in streamers:
        names += f'https://twitch.tv/{name}\n'

    if game in DESCRIPTIONS:
        return DESCRIPTIONS[game].format(names)
    return f'Made with twitchtube by offish\n{names}'


def get_title(game):
    if TITLE:
        return TITLE

    title = json.loads(open(f'{CLIP_PATH.format(get_date(), game)}/clips.json', 'r').read())

    for i in title:
        return '{} - {} Highlights #'.format(title[i]['title'], game)


def get_file(game):
    return f'{CLIP_PATH.format(get_date(), game)}/rendered.mp4'
