from pathlib import Path
from json import dump
from glob import glob
import os

from twitchtube import __version__ as twitchtube_version
from .exceptions import *
from .logging import Log
from .config import *
from .utils import *
from .clips import get_clips, download_clips

from moviepy.editor import VideoFileClip, concatenate_videoclips
from opplast import Upload, __version__ as opplast_version

log = Log()


# add language as param
def make_video(
        # required
        data: list = DATA,
        blacklist: list = BLACKLIST,
        # other
        path: str = get_path(),
        check_version: bool = CHECK_VERSION,
        # twitch
        client_id: str = CLIENT_ID,
        oauth_token: str = OAUTH_TOKEN,
        period: int = PERIOD,
        language: str = LANGUAGE,
        limit: int = LIMIT,
        # selenium
        profile_path: str = ROOT_PROFILE_PATH,
        sleep: int = SLEEP,
        headless: bool = HEADLESS,
        debug: bool = DEBUG,
        # video options
        render_video: bool = RENDER_VIDEO,
        file_name: str = FILE_NAME,
        resolution: tuple = RESOLUTION,
        frames: int = FRAMES,
        video_length: float = VIDEO_LENGTH,
        resize_clips: bool = RESIZE_CLIPS,
        enable_intro: bool = ENABLE_INTRO,
        resize_intro: bool = RESIZE_INTRO,
        intro_path: str = INTRO_FILE_PATH,
        enable_transition: bool = ENABLE_TRANSITION,
        resize_transition: bool = RESIZE_TRANSITION,
        transition_path: str = TRANSITION_FILE_PATH,
        enable_outro: bool = ENABLE_OUTRO,
        resize_outro: bool = RESIZE_OUTRO,
        outro_path: str = OUTRO_FILE_PATH,
        # other options
        save_file: bool = SAVE_TO_FILE,
        save_file_name: str = SAVE_FILE_NAME,
        upload_video: bool = UPLOAD_TO_YOUTUBE,
        delete_clips: bool = DELETE_CLIPS,
        # youtube
        title: str = TITLE,
        description: str = DESCRIPTION,
        thumbnail: str = THUMBNAIL,
        tags: list = TAGS,
) -> None:
    if check_version:
        try:

            for project, version in zip(
                    [
                        "twitchtube",
                        "opplast",
                    ],
                    [
                        twitchtube_version,
                        opplast_version,
                    ],
            ):
                current = get_current_version(project)

                if current != version:
                    log.warn(
                        f"You're running an old version of {project}, installed: {version}, current: {current}"
                    )
                else:
                    log.info(
                        f"You're running the latest version of {project} at {version}"
                    )

        except Exception as e:
            print(e)

    titles = []
    clips = []
    names = []
    ids = []

    video_length *= 60

    seconds = round(video_length / len(data), 1)

    log.info(
        f"Going to make video featuring {len(data)} streamers/games, that will end up being ~{seconds} seconds long"
    )

    if os.path.exists(f"{path}/{file_name}.mp4"):
        raise VideoPathAlreadyExists("specify another path")

    did_remove, data = remove_blacklisted(data, blacklist)

    if did_remove:
        log.info("Data included blacklisted content and was removed")

    data = convert_name_to_ids(data, oauth_token=oauth_token, client_id=client_id)

    # first we get all the clips for every entry in data
    # some bug here with loop or something
    for entry in data:
        category, name = entry[0], entry[1]

        # so we dont add the same clip twice
        new_clips, new_ids, new_titles = get_clips(
            blacklist,
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

        if new_clips:
            ids += new_ids
            titles += new_titles
            clips.append(new_clips)

    if not clips:
        raise NoClipsFound("Did not find any clips")

    Path(path).mkdir(parents=True, exist_ok=True)

    for batch in clips:
        names += download_clips(batch, path, oauth_token, client_id)

    log.info(f"Downloaded a total of {len(ids)} clips")

    # remove duplicate names
    names = list(dict.fromkeys(names))

    if not title:
        title = titles[0]

    config = create_video_config(
        "D:/Programming/twitchtube/clips/Jul-17-2021/r19am", file_name, title, description, thumbnail, tags, names
    )

    if save_file:
        with open(path + f"/{save_file_name}.json", "w") as f:
            dump(config, f, indent=4)

    if render_video:
        render(
            path,
            file_name,
            resolution,
            frames,
            resize_clips,
            enable_intro,
            resize_intro,
            intro_path,
            enable_transition,
            resize_transition,
            transition_path,
            enable_outro,
            resize_outro,
            outro_path,
        )

        if upload_video:
            upload = Upload(profile_path, sleep, headless, debug)

            log.info("Trying to upload video to YouTube")

            try:
                was_uploaded, video_id = upload.upload(config)

                if was_uploaded:
                    log.info(f"{video_id} was successfully uploaded to YouTube")

            except Exception as e:
                log.error(f"There was an error {e} when trying to upload to YouTube")

    if delete_clips:
        log.info("Getting files to delete...")
        files = glob(f"{path}/*.mp4")

        for file in files:
            if not file.replace("\\", "/") == path + f"/{file_name}.mp4":
                try:
                    os.remove(file)
                    log.clip(f"Deleted {file.replace(path, '')}")

                except Exception as e:
                    log.clip(f"Could not delete {file} because {e}")

    log.info("Done!")


def get_clip_paths(path: str) -> list:
    """
    Gets all the mp4 files listed in the given
    path and returns the paths as a list.
    """
    return [
        os.path.join(path, file) for file in os.listdir(path) if file.endswith(".mp4")
    ]


def add_clip(path: str, resolution: tuple, resize: bool = True) -> VideoFileClip:
    return VideoFileClip(path, target_resolution=resolution if resize else None)


def render(
        path: str,
        file_name: str,
        resolution: tuple,
        frames: int,
        resize_clips: bool,
        enable_intro: bool,
        resize_intro: bool,
        intro_path: str,
        enable_transition: bool,
        resize_transition: bool,
        transition_path: str,
        enable_outro: bool,
        resize_outro: bool,
        outro_path: str,
) -> None:
    """
    Concatenates a video with given path.
    Finds every mp4 file in given path, downloads
    them and add them into a list to be rendered.
    """
    log.info(f"Going to render video in {path}\n")

    video = []

    if enable_intro:
        video.append(add_clip(intro_path, resolution, resize_intro == True))

    number = 0

    clips = get_clip_paths(path)

    for clip in clips:

        # Don't add transition if it's the first or last clip
        if enable_transition and not (number == 0 or number == len(clips)):
            video.append(
                add_clip(transition_path, resolution, resize_transition == True)
            )

        video.append(add_clip(clip, resolution, resize_clips == True))

        # Just so we get cleaner logging
        name = clip.replace(path, "").replace("_", " ").replace("\\", "")

        log.info(f"Added {name} to be rendered")

        number += 1

        del clip
        del name

    if enable_outro:
        video.append(add_clip(outro_path, resolution, resize_outro == True))

    final = concatenate_videoclips(video, method="compose")
    final.write_videofile(
        f"{path}/{file_name}.mp4",
        fps=frames,
        temp_audiofile=f"{path}/temp-audio.m4a",
        remove_temp=True,
        codec="libx264",
        audio_codec="aac",
    )

    for clip in video:
        clip.close()

    final.close()

    print()  # New line for cleaner logging
    log.info("Video is done rendering!\n")

    del final
    del clips
    del video
