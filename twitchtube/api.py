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


def helix(
    category: str, data: list, oauth_token: str, client_id: str
) -> requests.Response:
    return request(
        "helix/" + category,
        {"Authorization": "Bearer " + oauth_token, "Client-Id": client_id},
        {"login" if category == "users" else "name": data},
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
