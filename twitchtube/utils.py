from datetime import date
from string import ascii_lowercase, digits
from random import choice

from .api import get
from .exceptions import InvalidCategory
from .config import CLIP_PATH


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

    return category, name


def convert_name_to_ids(data: list, oauth_token: str, client_id: str) -> list:
    # all data that is gets
    new_data = []
    users_to_check, games_to_check = [], []
    user_info, game_info = [], []

    for entry in data:
        cat, name = get_category_and_name(entry)
        if cat == 'channel':
            users_to_check.append(name)
        elif cat == 'game':
            games_to_check.append(name)

    # if there are more than 100 entries in users_to_check or games_to_check, this *WILL NOT WORK*
    if users_to_check:
        user_info = get("user", user_list=users_to_check, oauth_token=oauth_token, client_id=client_id)["data"]
    if games_to_check:
        game_info = get("game", game_list=games_to_check, oauth_token=oauth_token, client_id=client_id)["data"]
    return [('channel', i["id"]) for i in user_info] + [('game', i["id"]) for i in game_info]


def remove_blacklisted(data: list, blacklist: list) -> (bool, list):
    did_remove = False

    for d in data:
        d_category, d_name = get_category_and_name(d)

        for b in blacklist:
            b_category, b_name = get_category_and_name(b)

            if b_category == d_category and b_name == d_name:
                data.remove(d)
                did_remove = True

    return did_remove, data


def format_blacklist(blacklist: list, oauth_token: str, client_id: str) -> list:
    formatted = convert_name_to_ids(blacklist, oauth_token, client_id)
    return [f'{i[0]} {i[1]}' for i in formatted]


def is_blacklisted(clip: dict, blacklist: list) -> bool:
    if "broadcaster_id" in clip:
        if "channel " + clip["broadcaster_id"].lower() in [i.lower() for i in blacklist]:
            return True

    if clip.get("game_id"):
        if "game " + clip["game_id"] in blacklist:
            return True

    return False
