from os.path import exists
from pathlib import Path
from time import sleep
from glob import glob
from os import remove

from twitchtube.logging import Log
from twitchtube.config import *
from twitchtube.upload import upload_video_to_youtube
from twitchtube.utils import create_video_config, get_date
from twitchtube.clips import get_clips, download_clips
from twitchtube.video import render


log = Log()


while True:

    for game in GAMES:
        
        path = CLIP_PATH.format(get_date(), game)

        if not exists(path + f'/{FILE_NAME}.mp4'):

            for i in range(RETRIES):

                Path(path).mkdir(parents=True, exist_ok=True)

                clips = get_clips(game, VIDEO_LENGTH, path)

                if clips:
                    log.info(f'Starting to make a video for {game}')
                    names = download_clips(clips, VIDEO_LENGTH, path)
                    render(path)

                    if UPLOAD_TO_YOUTUBE:
                        config = create_video_config(game, names)
                        upload_video_to_youtube(config)
                    
                    if DELETE_CLIPS:
                        files = glob(f'{path}/*.mp4')

                        for file in files:
                            if not file == path + '\\' + FILE_NAME + '.mp4':
                                try:
                                    remove(file)
                                except PermissionError:
                                    log.error(f'Could not remove {file} because its being used')
                    
                    break

                else:
                    log.error(f'There was an error or timeout on Twitch\'s end, retrying... {i + 1}/{RETRIES}')

        else:
            log.info(f'Already made a video for {game}. Rechecking after {TIMEOUT} seconds.')

    sleep(TIMEOUT)
