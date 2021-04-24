import argparse

from twitchtube.logging import Log
from twitchtube.video import make_video
from twitchtube import __name__, __version__


log = Log()

log.info(f"Running {__name__} at v{__version__}")


parser = argparse.ArgumentParser(description="")


def str_to_bool(value):
    if isinstance(value, bool):
        return value
    if value.lower() in ("yes", "true", "t", "y", "1"):
        return True
    elif value.lower() in ("no", "false", "f", "n", "0"):
        return False
    else:
        raise argparse.ArgumentTypeError("Boolean value expected.")


parser.add_argument("data", type=str, help="")
parser.add_argument("--path", type=str, help="")
parser.add_argument("--client_id", type=str, help="")
parser.add_argument("--oauth_token", type=str, help="")
parser.add_argument("--period", type=str, help="")
parser.add_argument("--language", type=str, help="")
parser.add_argument("--limit", type=int, help="")
parser.add_argument("--profile_path", type=str, help="")
parser.add_argument("--sleep", type=int, help="")
parser.add_argument("--headless", type=str_to_bool, help="")
parser.add_argument("--debug", type=str_to_bool, help="")
parser.add_argument("--render_video", "--render", type=str_to_bool, help="")
parser.add_argument("--file_name", "--name", type=str, help="")
parser.add_argument("--resolution", nargs="+", type=int, help="")
parser.add_argument("--frames", type=int, help="")
parser.add_argument("--video_length", "--duration", type=float, help="")
parser.add_argument("--resize_clips", type=str_to_bool, help="")
parser.add_argument("--enable_intro", "--intro", type=str_to_bool, help="")
parser.add_argument("--resize_intro", type=str_to_bool, help="")
parser.add_argument("--intro_path", type=str, help="")
parser.add_argument("--enable_transition", "--transition", type=str_to_bool, help="")
parser.add_argument("--resize_transition", type=str_to_bool, help="")
parser.add_argument("--transition_path", type=str, help="")
parser.add_argument("--enable_outro", "--outro", type=str_to_bool, help="")
parser.add_argument("--resize_outro", type=str_to_bool, help="")
parser.add_argument("--outro_path", type=str, help="")
parser.add_argument("--save_file", type=str_to_bool, help="")
parser.add_argument("--save_file_name", type=str, help="")
parser.add_argument("--upload_video", "--upload", type=str_to_bool, help="")
parser.add_argument("--delete_clips", type=str_to_bool, help="")
parser.add_argument("--title", type=str, help="")
parser.add_argument("--description", type=str, help="")
parser.add_argument("--thumbnail", type=str, help="")
parser.add_argument("--tags", type=str, help="")

args = parser.parse_args()
parameters = {}

for key in vars(args):
    arg = getattr(args, key)

    try:
        if not arg == None:

            if key == "tags" or key == "data":
                arg = arg.split(", ")

            if key == "resolution":
                arg = tuple(arg)

            parameters[key] = arg

    except Exception as e:
        print(e)

make_video(**parameters)
