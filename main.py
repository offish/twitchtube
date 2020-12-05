from os.path import exists
from pathlib import Path
from time import sleep
from json import dump
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

        # Here we check if we've made a video for today
        # by checking if the rendered file exists.
        if not exists(path + f'\\{FILE_NAME}.mp4'):

            # We want to retry because Twitch often gives a
            # 500 Internal Server Error when trying to get clips
            for i in range(RETRIES):

                # Here we make a directory for the clips
                Path(path).mkdir(parents=True, exist_ok=True)

                # Get the top Twitch clips
                clips = get_clips(game, path)

                # Check if the API gave us a successful response
                if clips:
                    log.info(f'Starting to make a video for {game}')
                    # Download all needed clips
                    names = download_clips(clips, VIDEO_LENGTH, path)
                    config = create_video_config(game, names)

                    if RENDER_VIDEO:
                        render(path)

                    if UPLOAD_TO_YOUTUBE:
                        upload_video_to_youtube(config)
                    
                    if SAVE_TO_FILE:
                        with open(path + f'\\{SAVE_FILE_NAME}.json', 'w') as f:
                            dump(config, f, indent=4)

                    if DELETE_CLIPS:
                        # Get all the mp4 files in the path and delte them
                        # if they're not the rendered video
                        files = glob(f'{path}/*.mp4')

                        for file in files:
                            if not file == path + f'\\{FILE_NAME}.mp4':
                                try:
                                    remove(file)
                                # Sometimes a clip is "still being used" giving
                                # us an exception that would else crash the program
                                except PermissionError as e:
                                    log.error(f'Could not delete {file} because {e}')
                    
                    break

                else:
                    # Response was most likely an Internal Server Error and we retry
                    log.error(f'There was an error or timeout on Twitch\'s end, retrying... {i + 1}/{RETRIES}')

        else:
            # Rendered video does already exist
            log.info(f'Already made a video for {game}. Rechecking after {TIMEOUT} seconds.')

    # Sleep for given timeout to check if it's a different date
    sleep(TIMEOUT)
