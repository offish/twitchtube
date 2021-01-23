from datetime import date
import json

from .config import *


def get_date() -> str:
    """
    Gets the current date and returns the date as a string.
    """
    return date.today().strftime("%b-%d-%Y")


def create_video_config(category: str, streamers: list) -> dict:
    """
    Creates the video config used for uploading to YouTube
    returns a dict.
    """
    return {
        "category": CATEGORY,
        "keywords": get_tags(category),
        "description": get_description(category, streamers),
        "title": get_title(category),
        "file": get_file(category),
    }


def get_tags(category: str) -> str:
    """
    Gets the tag for given category (if any) as a string.
    """
    return str(TAGS.get(category))


def get_description(category: str, streamers: list) -> str:
    """
    Gets the description with given list of streamers
    and category, returns the description as a string.
    """
    names = "Streamers in this video:\n"

    for name in streamers:
        names += f"https://twitch.tv/{name}\n"

    if category in DESCRIPTIONS:
        return DESCRIPTIONS[category].format(names)
    return names


def get_title(category: str) -> str:
    """
    Gets the title and returns it as a string.
    """
    if TITLE:
        return TITLE

    title = json.loads(
        open(f"{CLIP_PATH.format(get_date(), category)}/clips.json", "r").read()
    )

    for i in title:
        # Return the first entry's title
        return f"{title[i]['title']} - {category} Twitch Highlights"


def get_file(category: str) -> str:
    """
    Gets the path/file given category and returns it as a string.
    """
    return f"{CLIP_PATH.format(get_date(), category)}/{FILE_NAME}.mp4"
