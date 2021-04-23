from pathlib import Path
import os

from .logging import Log
from .config import *
from .exceptions import *
from .utils import get_path, create_video_config
from .clips import get_clips, download_clips

from moviepy.editor import VideoFileClip, concatenate_videoclips
from opplast import Upload


log = Log()

# add language as param
def make_video(
    data: list,
    path: str = get_path(),
    render_video: bool = RENDER_VIDEO,
    resolution: tuple = RESOLUTION,
    frames: int = FRAMES,
    video_length: float = VIDEO_LENGTH,
    resize_clips: bool = RESIZE_CLIPS,
    file_name: str = FILE_NAME,
    upload_video: bool = UPLOAD_TO_YOUTUBE,
    title: str = TITLE,
    description: str = DESCRIPTION,
    thumbnail: str = THUMBNAIL,
    tags: list = TAGS,
):
    clips = []
    names = []
    ids = []

    video_length *= 60

    seconds = round(video_length / len(data), 1)

    log.info(f"Starting to make video with {len(data)} streamers/games")

    if os.path.exists(f"{path}/{file_name}.mp4"):
        raise VideoPathAlreadyExists("specify another path")

    # first we get all the clips for every entry in data
    for entry in data:
        category, name = entry.split(" ", 1)

        if not (category == "game" or category == "channel"):
            raise InvalidCategory(
                category + ' is not supported. Use "game" or "channel"'
            )

        # so we dont add the same clip twice
        new_clips, new_ids = get_clips(category, name, path, seconds, ids)

        ids += new_ids
        clips.append(new_clips)

    Path(path).mkdir(parents=True, exist_ok=True)

    for batch in clips:
        names += download_clips(batch, path)

    # remove duplicate names
    names = list(dict.fromkeys(names))

    config = create_video_config(
        path, file_name, title, description, thumbnail, tags, names
    )

    if render_video:
        render(path, file_name)

        if upload_video:
            upload = Upload(ROOT_PROFILE_PATH, SLEEP, HEADLESS, DEBUG)

            log.info("Trying to upload video to YouTube")

            try:
                was_uploaded, video_id = upload.upload(config)

                if was_uploaded:
                    log.info(f"{video_id} was successfully uploaded to YouTube")

            except Exception as e:
                log.error(f"There was an error {e} when trying to upload to YouTube")


def get_clip_paths(path: str) -> list:
    """
    Gets all the mp4 files listed in the given
    path and returns the paths as a list.
    """
    return [
        os.path.join(path, file) for file in os.listdir(path) if file.endswith(".mp4")
    ]


def add_clip(path: str, resize: bool = True) -> VideoFileClip:
    return VideoFileClip(path, target_resolution=RESOLUTION if resize else None)


def render(path: str, file_name: str) -> None:
    """
    Concatenates a video with given path.
    Finds every mp4 file in given path, downloads
    them and add them into a list to be rendered.
    """
    log.info(f"Going to render video in {path}\n")

    video = []

    if ENABLE_INTRO:
        video.append(add_clip(INTRO_FILE_PATH, RESIZE_INTRO == True))

    number = 0

    clips = get_clip_paths(path)

    for clip in clips:

        # Don't add transition if it's the first or last clip
        if ENABLE_TRANSITION and not (number == 0 or number == len(clips)):
            video.append(add_clip(TRANSITION_FILE_PATH, RESIZE_TRANSITION == True))

        video.append(add_clip(clip, RESIZE_CLIPS == True))

        # Just so we get cleaner logging
        name = clip.replace(path, "").replace("_", " ").replace("\\", "")

        log.info(f"Added {name} to be rendered")

        number += 1

        del clip
        del name

    if ENABLE_OUTRO:
        video.append(add_clip(OUTRO_FILE_PATH, RESIZE_OUTRO == True))

    final = concatenate_videoclips(video, method="compose")
    final.write_videofile(
        f"{path}/{file_name}.mp4",
        fps=FRAMES,
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
