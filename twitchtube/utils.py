from datetime import date
import json

from .config import *


def get_date() -> str:
    """
    Gets the current date and returns the date as a string.
    """
    return date.today().strftime("%b-%d-%Y")


def create_video_config(game: str, streamers: list) -> dict:
    """
    Creates the video config used for uploading to YouTube
    returns a dict.
    """
    return {
        "category": CATEGORY,
        "keywords": get_tags(game),
        "description": get_description(game, streamers),
        "title": get_title(game),
        "file": get_file(game),
    }


def get_tags(game: str) -> str:
    """
    Gets the tag for given game (if any) as a string.
    """
    return str(TAGS.get(game))


def get_description(game: str, streamers: list) -> str:
    """
    Gets the description with given list of streamers
    and game, returns the description as a string.
    """
    names = "Streamers in this video:\n"

    for name in streamers:
        names += f"https://twitch.tv/{name}\n"

    if game in DESCRIPTIONS:
        return DESCRIPTIONS[game].format(names)
    return names


def get_title(game: str) -> str:
    """
    Gets the title and returns it as a string.
    """
    if TITLE:
        return TITLE

    title = json.loads(
        open(f"{CLIP_PATH.format(get_date(), game)}/clips.json", "r").read()
    )

    for i in title:
        # Return the first entry's title
        return f"{title[i]['title']} - {game} Twitch Highlights"


def get_file(game: str) -> str:
    """
    Gets the path/file given game and returns it as a string.
    """
    return f"{CLIP_PATH.format(get_date(), game)}\\{FILE_NAME}.mp4"
