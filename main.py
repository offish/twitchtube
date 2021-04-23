from twitchtube.logging import Log
from twitchtube.config import *
from twitchtube.video import make_video
from twitchtube.utils import get_path
from twitchtube import __name__, __version__

import argparse


log = Log()

log.info(f"Running {__name__} at v{__version__}")


# [("game", "Just Chatting"), ("channel", "xQcOW")]


"""data = [("game", "Just Chatting"), ("channel", "xQcOW"), ("channel", "Trainwreckstv")]

make_video(data, video_length=0.2)"""

parser = argparse.ArgumentParser(description="Optional app description")

# Required positional argument
parser.add_argument(
    "-data",
    "--data",
    nargs="+",
    help="A required integer positional argument",
    required=True,
)
parser.add_argument("--path", type=str, help="An optional integer argument")
parser.add_argument("--render_video", type=bool, help="An optional integer argument")
parser.add_argument("--resolution", type=tuple, help="An optional integer argument")
parser.add_argument("--frames", type=int, help="An optional integer argument")
parser.add_argument("--video_length", type=float, help="An optional integer argument")
parser.add_argument("--resize_clips", type=bool, help="An optional integer argument")
parser.add_argument("--file_name", type=str, help="An optional integer argument")
parser.add_argument("--upload_video", type=bool, help="An optional integer argument")
parser.add_argument("--title", type=str, help="An optional integer argument")
parser.add_argument("--description", type=str, help="An optional integer argument")
parser.add_argument("--thumbnail", type=str, help="An optional integer argument")
parser.add_argument("--tags", nargs="+", help="An optional integer argument")

args = parser.parse_args()

print(args.data)

make_video(
    args.data,
    path=args.path if args.path else get_path(),
    render_video=args.render_video if args.render_video else RENDER_VIDEO,
    resolution=args.resolution if args.resolution else RESOLUTION,
    frames=args.frames if args.frames else FRAMES,
    video_length=args.video_length if args.video_length else VIDEO_LENGTH,
    resize_clips=args.resize_clips if args.resize_clips else RESIZE_CLIPS,
    file_name=args.file_name if args.file_name else FILE_NAME,
    upload_video=args.upload_video if args.upload_video else UPLOAD_TO_YOUTUBE,
    title=args.title if args.title else TITLE,
    description=args.description if args.description else DESCRIPTION,
    thumbnail=args.thumbnail if args.thumbnail else THUMBNAIL,
    tags=args.tags if args.tags else TAGS,
)

"""
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
"""
