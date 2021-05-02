import pathlib

# Note:
# Changing FRAMES and or RESOULTION will heavily impact load on CPU.
# If you have a powerful enough computer you may set it to 1080p60

# other
PATH = str(pathlib.Path().absolute()).replace("\\", "/")
CLIP_PATH = PATH + "/clips/{}/{}"
CHECK_VERSION = (
    True  # see if youre running the latest version of twitchtube and opplast
)

DATA = ["c xQcOW", "c Trainwreckstv", "g Just Chatting"]

# twitch
CLIENT_ID = ""  # Twitch Client ID
OAUTH_TOKEN = ""  # Twitch OAuth Token
PERIOD = "day"  # day, week, month or all
LANGUAGE = "en"  # en, es, th etc.
LIMIT = 100  # 1-100


# selenium
ROOT_PROFILE_PATH = ""  # Path to the Firefox profile where you are logged into YouTube
SLEEP = 3  # How many seconds Firefox should sleep for when uploading
HEADLESS = True  # If True Firefox will be hidden (True/False)
DEBUG = True  # If information when uploading should be printed (True/False)


# video options
RENDER_VIDEO = True  # If clips should be rendered into one video (True/False). If set to False everything else under Video will be ignored
RESOLUTION = (
    720,
    1280,
)  # Resoultion of the rendered video (height, width) for 1080p: ((1080, 1920))
FRAMES = 30  # Frames per second (30/60)
VIDEO_LENGTH = 10.5  # Minumum video length in minutes (doesn't always work)
RESIZE_CLIPS = True  # Resize clips to fit RESOLUTION (True/False) If any RESIZE option is set to False the video might end up having a weird resolution
FILE_NAME = "rendered"  # Name of the rendered video
ENABLE_INTRO = False  # Enable (True/False)
RESIZE_INTRO = True  # Resize (True/False) read RESIZE_CLIPS
INTRO_FILE_PATH = PATH + "/assets/intro.mp4"  # Path to video file (str)
ENABLE_TRANSITION = True
RESIZE_TRANSITION = True
TRANSITION_FILE_PATH = PATH + "/assets/transition.mp4"
ENABLE_OUTRO = False
RESIZE_OUTRO = True
OUTRO_FILE_PATH = PATH + "/assets/outro.mp4"


# other options
SAVE_TO_FILE = True  # If YouTube stuff should be saved to a separate file e.g. title, description & tags (True/False)
SAVE_FILE_NAME = "youtube"  # Name of the file YouTube stuff should be saved to
UPLOAD_TO_YOUTUBE = True  # If the rendered video should be uploaded to YouTube after rendering (True/False)
DELETE_CLIPS = True  # If the downloaded clips should be deleted after rendering the video (True/False)


# youtube
TITLE = ""  # youtube title, leave empty for the first clip's title
DESCRIPTION = (
    "Streamers in this video:\n"  # youtube description, streamers will be added
)
THUMBNAIL = ""  # path to the image file to be set as thumbnail
TAGS = ["twitch", "just chatting", "xqc"]  # your youtube tags
