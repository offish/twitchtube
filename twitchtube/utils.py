from .api import get
from .exceptions import InvalidCategory


def get_description(description: str, names: list) -> str:
    return description + "".join([f"https://twitch.tv/{name}\n" for name in names])


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
    if category not in ["g", "game", "c", "channel"]:
        raise InvalidCategory(
            category + ' is not supported. Use "g", "game", "c" or "channel"'
        )

    return "game" if category in ["g", "game"] else "channel"


def get_category_and_name(entry: str) -> (str, str):
    _category, name = entry.split(" ", 1)
    category = get_category(_category)

    return category, name


def name_to_ids(data: list, oauth_token: str, client_id: str) -> list:
    result = []

    for category, helix_category, helix_name in [
        (["channel", "c"], "users", "display_name"),
        (["game", "g"], "games", "name"),
    ]:
        current_list = []

        for entry in data:
            c, n = get_category_and_name(entry)

            if c in category:
                current_list.append(n)

        if len(current_list) > 0:
            info = (
                get(
                    "helix",
                    category=helix_category,
                    data=current_list,
                    oauth_token=oauth_token,
                    client_id=client_id,
                ).get("data")
                or []
            )

            result += [(category[0], i["id"], i[helix_name]) for i in info]

    return result


def remove_blacklisted(data: list, blacklist: list) -> (bool, list):
    did_remove = False

    # horrible code, but seems to work. feel free to improve
    for d in data:
        d_category, d_name = get_category_and_name(d)

        for b in blacklist:
            b_category, b_name = get_category_and_name(b)

            # category is either channel or game, both has to be equal
            # game fortnite != channel fortnite
            if b_category == d_category and b_name == d_name:
                data.remove(d)
                did_remove = True

    return did_remove, data


def format_blacklist(blacklist: list, oauth_token: str, client_id: str) -> list:
    return [f"{i[0]} {i[1]}" for i in name_to_ids(blacklist, oauth_token, client_id)]


def is_blacklisted(clip: dict, blacklist: list) -> bool:
    return (
        "broadcaster_id" in clip and "channel " + clip["broadcaster_id"] in blacklist
    ) or ("game_id" in clip and "game " + clip["game_id"] in blacklist)
