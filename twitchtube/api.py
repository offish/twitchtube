import json

import requests


local = locals()


def request(endpoint: str, headers: dict, params: dict) -> dict:
    return requests.get(
        "https://api.twitch.tv/" + endpoint, headers=headers, params=params
    )


def data(slug: str, oauth_token: str, client_id: str) -> dict:
    return request(
        "helix/clips",
        {"Authorization": "Bearer " + oauth_token, "Client-Id": client_id},
        {"id": slug},
    )


def top_clips(headers: dict, params: dict) -> dict:
    return request("kraken/clips/top", headers, params)


def get(name: str, **args) -> dict:
    response = local[name](**args)

    try:
        return response.json()
    except SyntaxError:
        return response
