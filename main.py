from pathlib import Path
from time import sleep
from json import dump, JSONDecodeError
from glob import glob
import os

from twitchtube.logging import Log
from twitchtube.config import *
from twitchtube.utils import create_video_config, get_path
from twitchtube.clips import get_clips, download_clips
from twitchtube.video import render
from twitchtube import __name__, __version__

from opplast import Upload


log = Log()

log.info(f"Running {__name__} at v{__version__}")

while True:

    for category in LIST:
        path = get_path(category)

        # Here we check if we've made a video for today
        # by checking if the rendered file exists.
        if not os.path.exists(path + f"/{FILE_NAME}.mp4"):

            # We want to retry because Twitch often gives a
            # 500 Internal Server Error when trying to get clips
            for i in range(RETRIES):

                # Here we make a directory for the clips
                Path(path).mkdir(parents=True, exist_ok=True)

                # Get the top Twitch clips
                clips = get_clips(category, path)

                # Check if the API gave us a successful response
                if clips:
                    log.info(f"Starting to make a {category} video")
                    # Download all needed clips
                    names = download_clips(clips, VIDEO_LENGTH, path)
                    config = create_video_config(category, names)

                    if RENDER_VIDEO:
                        render(path)

                    if SAVE_TO_FILE:
                        with open(path + f"/{SAVE_FILE_NAME}.json", "w") as f:
                            dump(config, f, indent=4)

                    if UPLOAD_TO_YOUTUBE and RENDER_VIDEO:
                        upload = Upload(ROOT_PROFILE_PATH, SLEEP, HEADLESS, DEBUG)

                        log.info("Trying to upload video to YouTube")

                        try:
                            was_uploaded, video_id = upload.upload(config)

                            if was_uploaded:
                                log.info(
                                    f"{video_id} was successfully uploaded to YouTube"
                                )

                        except Exception as e:
                            log.error(
                                f"There was an error {e} when trying to upload to YouTube"
                            )

                    if DELETE_CLIPS:
                        # Get all the mp4 files in the path and delte them
                        # if they're not the rendered video
                        files = glob(f"{path}/*.mp4")

                        for file in files:
                            if (
                                not file.replace("\\", "/")
                                == path + f"/{FILE_NAME}.mp4"
                            ):
                                try:
                                    os.remove(file)
                                    log.info(f"Deleted {file.replace(path, '')}")
                                # Sometimes a clip is "still being used" giving
                                # us an exception that would else crash the program
                                except PermissionError as e:
                                    log.error(f"Could not delete {file} because {e}")

                    break

                else:
                    # Response was most likely an Internal Server Error and we retry
                    log.info(
                        f"There was an error Twitch's end or no clips were found. If no error has been thrown please check your PARAMS option in config.py, retrying... {i + 1}/{RETRIES}"
                    )

        else:
            # Rendered video does already exist
            log.info(
                f"Already made a video for {category}. Rechecking after {TIMEOUT} seconds."
            )

    # Sleep for given timeout to check if it's a different date
    sleep(TIMEOUT)
