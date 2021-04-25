from datetime import date
from string import ascii_lowercase, digits
from random import choice

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
