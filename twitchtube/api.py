import requests


class TwitchAPI:
    def __init__(self, client_id: str, oauth_token: str) -> None:
        self.client_id = client_id
        self.oauth_token = oauth_token
        self.headers = {
            "Authorization": f"Bearer {self.oauth_token}",
            "Client-Id": self.client_id,
        }

    def _get_request(self, endpoint: str, params: dict, **kwargs) -> dict:
        url = f"https://api.twitch.tv/helix/{endpoint}"
        response = requests.get(url, headers=self.headers, params=params, **kwargs)
        response.raise_for_status()

        return response.json()

    def get_clip(self, slug: str) -> dict:
        params = {"id": slug}
        return self.get_clips(params=params)

    def get_clips(self, **kwargs) -> dict:
        return self._get_request("clips", **kwargs)

    def get_helix_category(self, category: str, data: list) -> dict:
        params = {"login" if category == "users" else "name": data}
        return self._get_request(category, params)
