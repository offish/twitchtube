import os

from twitchtube.logging import Log
from twitchtube.config import *

from moviepy.editor import VideoFileClip, concatenate_videoclips


log = Log()


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


def render(path: str) -> None:
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
        f"{path}/{FILE_NAME}.mp4",
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
