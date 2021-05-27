from datetime import date
from string import ascii_lowercase, digits
from random import choice

from .exceptions import InvalidCategory
from .config import CLIP_PATH

from requests import get


def get_date() -> str:
    """
    Gets the current date and returns the date as a string.
    """
    return date.today().strftime("%b-%d-%Y")


def get_path() -> str:
    return CLIP_PATH.format(
        get_date(),
        "".join(choice(ascii_lowercase + digits) for _ in range(5)),
    )


def get_description(description: str, names: list) -> str:
    for name in names:
        description += f"https://twitch.tv/{name}\n"
    return description


def get_current_version(project: str) -> str:
    txt = '__version__ = "'
    response = get(
        f"https://raw.githubusercontent.com/offish/{project}/master/{project}/__init__.py"
    ).text
    response = response[response.index(txt) :].replace(txt, "")

    return response[: response.index('"\n')].replace('"', "")


def create_video_config(
    path: str,
    file_name: str,
    title: str,
    description: str,
    thumbnail: str,
    tags: list,
    names: list,
) -> dict:
    return {
        "file": f"{path}/{file_name}.mp4",
        "title": title,
        "description": get_description(description, names),
        "thumbnail": thumbnail,
        "tags": tags,
    }


def get_category(category: str) -> str:
    if category == "g" or category == "game":
        return "game"

    if category == "c" or category == "channel":
        return "channel"

    raise InvalidCategory(
        category + ' is not supported. Use "g", "game", "c" or "channel"'
    )


def get_category_and_name(entry: str) -> (str, str):
    _category, name = entry.split(" ", 1)
    category = get_category(_category)

    return (category, name)


def remove_blacklisted(data: list, blacklist: list) -> (bool, list):
    did_remove = False

    for d in data:
        d_category, d_name = get_category_and_name(d)

        for b in blacklist:
            b_category, b_name = get_category_and_name(b)

            if b_category == d_category and b_name == d_name:
                data.remove(d)
                did_remove = True

    return (did_remove, data)


def format_blacklist(blacklist: list) -> list:
    formatted = []

    for b in blacklist:
        category, name = get_category_and_name(b)
        formatted.append(category + " " + name)

    return formatted


def is_blacklisted(clip: dict, blacklist: list) -> bool:
    if "broadcaster" in clip and clip["broadcaster"].get("name"):
        if "channel " + clip["broadcaster"]["name"] in blacklist:
            return True

    if clip.get("game"):
        if "game " + clip["game"] in blacklist:
            return True

    return False
