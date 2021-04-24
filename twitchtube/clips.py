from math import ceil
from json import dump
import urllib.request
import re

from .exceptions import WrongKrakenResponse
from .logging import Log
from .api import get


log = Log()


def get_data(slug: str) -> dict:
    """
    Gets the data from a given slug,
    returns a JSON respone from the Helix API endpoint
    """
    response = get("data", slug=slug)

    try:
        return response["data"][0]
    except KeyError as e:
        log.error(f"Ran into exception: {e}, {response}")
        return response


def get_clip_data(slug: str) -> tuple:
    """
    Gets the data for given slug, returns a tuple first
    entry being the mp4_url used to download the clip,
    second entry being the title of the clip to be used as filename.
    """
    clip_info = get_data(slug)

    if "thumbnail_url" in clip_info and "title" in clip_info:
        # All to get what we need to return
        # the mp4_url and title of the clip
        thumb_url = clip_info["thumbnail_url"]
        slice_point = thumb_url.index("-preview-")
        mp4_url = thumb_url[:slice_point] + ".mp4"

        return mp4_url, clip_info["title"]

    raise TypeError(
        f"We didn't receieve what we wanted. /helix/clips endpoint gave:\n{clip_info}"
    )


def get_progress(count, block_size, total_size) -> None:
    """
    Used for printing the download progress
    """
    percent = int(count * block_size * 100 / total_size)
    print(f"Downloading clip... {percent}%", end="\r", flush=True)


def get_slug(clip: str) -> str:
    """
    Splits up the URL given and returns the slug
    of the clip.
    """
    slug = clip.split("/")
    return slug[len(slug) - 1]


def download_clip(clip: str, basepath: str) -> None:
    """
    Downloads the clip, does not return anything.
    """
    slug = get_slug(clip)
    mp4_url, _ = get_clip_data(slug)
    # Remove special characters so we can save the video
    regex = re.compile("[^a-zA-Z0-9_]")
    out_filename = regex.sub("", slug) + ".mp4"
    output_path = basepath + "/" + out_filename

    log.clip(f"Downloading clip with slug: {slug}.")
    log.clip(f"Saving '{slug}' as '{out_filename}'.")
    # Download the clip with given mp4_url
    urllib.request.urlretrieve(mp4_url, output_path, reporthook=get_progress)
    log.clip(f"{slug} has been downloaded.\n")


def get_clips(
    category: str,
    name: str,
    path: str,
    seconds: float,
    ids: list,
    client_id: str,
    oauth_token: str,
    period: str,
    language: str,
    limit: int,
) -> (dict, list):
    """
    Gets the top clips for given game, returns JSON response
    from the Kraken API endpoint.
    """
    data = {}
    new_ids = []

    headers = {"Accept": "application/vnd.twitchtv.v5+json", "Client-ID": client_id}

    params = {"period": period, "language": language, "limit": limit}
    params[category] = name

    response = get("top_clips", headers=headers, params=params)

    if not response.get("clips"):
        if response.get("error") == "Internal Server Error":
            # the error is twitch's fault, we try again
            get_clips(
                category,
                name,
                path,
                seconds,
                ids,
                client_id,
                oauth_token,
                period,
                language,
                limit,
            )

        else:
            raise WrongKrakenResponse(f"Could not find 'clips' in response. {response}")

    for clip in response["clips"]:
        duration = clip["duration"]

        if seconds <= 0.0:
            break

        tracking_id = clip["tracking_id"]

        if not tracking_id in ids:
            data[clip["tracking_id"]] = {
                "url": "https://clips.twitch.tv/" + clip["slug"],
                "title": clip["title"],
                "display_name": clip["broadcaster"]["display_name"],
                "duration": duration,
            }
            new_ids.append(tracking_id)

            seconds -= duration

    return (data, new_ids)


def download_clips(data: dict, path: str) -> list:
    """
    Downloads clips, returns a list of streamer names.
    """
    names = []

    for clip in data:
        download_clip(data[clip]["url"], path)

        name = data[clip]["display_name"]

        names.append(name)

    log.info(f"Downloaded {len(data)} clips from this batch.\n")
    return names
