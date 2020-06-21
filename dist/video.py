import os

from moviepy.editor import VideoFileClip, concatenate_videoclips

from .config import RESOLUTION, FRAMES
from .logging import log


log = log()


def get_clip_files(path: str):
    clips = []

    for file in os.listdir(path):
        if file.endswith('.mp4'):
            clips.append(os.path.join(path, file))
    return clips


def render(path: str):
    log.info(f'Going to render video in {path}\n')

    videos = []

    for video in get_clip_files(path):

        movie = VideoFileClip(video, target_resolution=RESOLUTION)
        name = video.replace(path, '') \
            .replace('_', ' ') \
            .replace('\\', '')

        videos.append(movie)

        log.info(f'Added {name} to be rendered')

        del video
        del movie
        del name

    final = concatenate_videoclips(videos, method='compose')
    final.write_videofile(f'{path}/rendered.mp4', fps=FRAMES)

    print() # New line for cleaner logging
    log.info('Video is done rendering!\n')
