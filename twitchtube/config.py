import pathlib

# Note:
# Changing FRAMES and or RESOULTION will heavily impact load on CPU.
# If you have a powerful enough computer you may set it to 1080p60

# Secrets
# Twitch Client ID
CLIENT_ID = ""

# Twitch OAuth Token
OAUTH_TOKEN = ""

# Path to the Firefox profile where you are logged into YouTube
ROOT_PROFILE_PATH = ""

# Selenium
# How many seconds Firefox should sleep for when uploading
SLEEP = 3

# If True Firefox will be hidden (True/False)
HEADLESS = True

# If information when uploading should be printed (True/False)
DEBUG = True


# Paths
PATH = str(pathlib.Path().absolute()).replace("\\", "/")
CLIP_PATH = PATH + "/clips/{}/{}"


# Video
# Set the mode (game/channel)
MODE = "game"

# If mode is channel put channel names e.g. ["trainwreckstv", "xqcow"]
# If mode is game put game names e.g. ["Team Fortress 2", "Just Chatting"]
LIST = ["Team Fortress 2", "Just Chatting"]

# If clips should be rendered into one video (True/False)
# If set to False everything else under Video will be ignored
RENDER_VIDEO = True

# Resoultion of the rendered video (height, width) for 1080p: ((1080, 1920))
RESOLUTION = (720, 1280)

# Frames per second (30/60)
FRAMES = 30

# Minumum video length in minutes (doesn't always work)
VIDEO_LENGTH = 10.5

# Resize clips to fit RESOLUTION (True/False)
# If any RESIZE option is set to False the video might end up having a weird resolution
RESIZE_CLIPS = True

# Name of the rendered video
FILE_NAME = "rendered"

# Name of downloaded clip (slug/title)
CLIP_TITLE = "slug"

# Enable (True/False)
# Resize (True/False) read RESIZE_CLIPS
# Path to video file (str)
ENABLE_INTRO = False
RESIZE_INTRO = True
INTRO_FILE_PATH = PATH + "/assets/intro.mp4"

ENABLE_TRANSITION = True
RESIZE_TRANSITION = True
TRANSITION_FILE_PATH = PATH + "/assets/transition.mp4"

ENABLE_OUTRO = False
RESIZE_OUTRO = True
OUTRO_FILE_PATH = PATH + "/assets/outro.mp4"


# Other
# If YouTube stuff should be saved to a separate file e.g. title, description & tags (True/False)
SAVE_TO_FILE = True

# Name of the file YouTube stuff should be saved to
SAVE_FILE_NAME = "youtube"

# If the rendered video should be uploaded to YouTube after rendering (True/False)
UPLOAD_TO_YOUTUBE = True

# If the downloaded clips should be deleted after rendering the video (True/False)
DELETE_CLIPS = True

# How often it should check if it has made a video today (in seconds)
TIMEOUT = 3600


# Twitch
RETRIES = 5

# Twitch API Request Options
HEADERS = {"Accept": "application/vnd.twitchtv.v5+json", "Client-ID": CLIENT_ID}
PARAMS = {"period": "day", "language": "en", "limit": 100}  # 100 is max


# YouTube
# If empty, it would take the title of the first clip, and add "- *category* Highlights Twitch"
TITLE = ""

# Category
# Not supported yet
CATEGORY = 20  # 20 for gaming

# Descriptions
# {} will be replaced with a list of streamer names
DESCRIPTIONS = {
    "Just Chatting": "Just Chatting twitch clips \n\n{}\n",
    "Team Fortress 2": "TF2 twitch clips\n\n{}\n",
}

# Thumbnails
THUMBNAILS = {
    "Just Chatting": "path/to/file.jpg",
    "Team Fortress 2": "path/to/file.jpg",
}

# Tags
# Not supported yet
TAGS = {
    "Just Chatting": "just chatting, just chatting clips, just chatting twitch clips",
    "Team Fortress 2": "tf2, tf2 twitch, tf2 twitch clips",
}
