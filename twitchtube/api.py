import json

import requests

local = locals()


def request(endpoint: str, headers: dict, params: dict) -> requests.Response:
    return requests.get(
        "https://api.twitch.tv/" + endpoint, headers=headers, params=params
    )


def data(slug: str, oauth_token: str, client_id: str) -> requests.Response:
    return request(
        "helix/clips",
        {"Authorization": "Bearer " + oauth_token, "Client-Id": client_id},
        {"id": slug},
    )


def game(game_list: list, oauth_token: str, client_id: str) -> requests.Response:
    # returns data about every specified name of the game (including it's id)
    # e.g. [Minecraft] -> {'id': '27471', 'name': 'Minecraft',
    #                      'box_art_url': 'https://static-cdn.jtvnw.net/ttv-boxart/Minecraft-{width}x{height}.jpg'}
    return request(
        "helix/games",
        {"Authorization": "Bearer " + oauth_token, "Client-Id": client_id},
        {"name": game_list}
    )


def user(user_list: list, oauth_token: str, client_id: str) -> requests.Response:
    # just like game() but for users
    return request(
        "helix/users",
        {"Authorization": "Bearer " + oauth_token, "Client-Id": client_id},
        {"login": user_list}
    )


def top_clips(headers: dict, params: dict, oauth_token: str) -> requests.Response:
    headers.update({"Authorization": "Bearer " + oauth_token})
    return request("helix/clips", headers, params)


def get(name: str, **args) -> dict:
    response = local[name](**args)

    try:
        return response.json()
    except SyntaxError:
        # probably should remove this, but i imagine it's for python2.7 support? dunno
        return response
