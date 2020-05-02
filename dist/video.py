import os

from moviepy.editor import VideoFileClip, concatenate_videoclips

from .logging import log


def get_clip_files(path: str):
    clips = []

    for file in os.listdir(path):
        if file.endswith(".mp4"):
            clips.append(os.path.join(path, file))
    return clips


def render(game, path: str):
    log('info', f"Going to render video in {path}\n")

    videos = []

    for video in get_clip_files(path):

        movie = VideoFileClip(video, target_resolution=(720, 1280))
        name = video.replace(path, "") \
            .replace("_", " ") \
            .replace("\\", "")

        videos.append(movie)

        log('info', f"Added {name} to be rendered")

        del video
        del movie
        del name

    final = concatenate_videoclips(videos, method="compose")
    final.write_videofile(f"{path}/rendered.mp4", fps=30)

    print()
    log('info', "Video is done rendering!\n")
