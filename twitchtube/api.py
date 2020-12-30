import json

from .config import OAUTH_TOKEN, CLIENT_ID

import requests


local = locals()


def request(endpoint: str, headers: dict, params: dict) -> dict:
    return requests.get(
        'https://api.twitch.tv/' + endpoint,
        headers = headers,
        params = params
    )


def data(slug: str) -> dict:
    return request(
        'helix/clips',
        {
            'Authorization': f'Bearer {OAUTH_TOKEN}',
            'Client-Id': CLIENT_ID
        },
        {'id': slug}
    )


def top_clips(headers: dict, params: dict) -> dict:
    return request(
        'kraken/clips/top',
        headers,
        params
    )


def get(name: str, **args) -> dict:
    response = local[name](**args)

    try:
        return response.json()
    except SyntaxError:
        return response
