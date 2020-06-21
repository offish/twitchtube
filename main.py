from dist.config import GAMES, VIDEO_LENGTH, CLIP_PATH
from dist.other import create_video_config, get_date
from dist.clips import get_clips, download_clips
from dist.upload import upload_video_to_youtube
from dist.video import render
from dist.logging import log
from os.path import isdir
from pathlib import Path
from time import sleep

log = log()

while True:

    for game in GAMES:
        
        path = CLIP_PATH.format(get_date(), game)

        if not isdir(path):
            tries = 3

            for i in range(tries):

                Path(path).mkdir(parents=True, exist_ok=True)

                clips = get_clips(game, VIDEO_LENGTH, path)

                if clips:
                    log.info(f'Starting to make a video for {game}')
                    names = download_clips(clips, VIDEO_LENGTH, path)
                    config = create_video_config(game, names)
                    
                    render(path)
                    upload_video_to_youtube(config)

                    del names
                    del config

                else:
                    log.error(f'There was an error or timeout on Twitch\'s end, retrying... {i + 1}/{tries}')

        else:
            log.info(f'Already made a video for {game}. Rechecking in an hour.')

    sleep(3600)
