import pathlib

# Note:
# Changing FRAMES and or RESOLUTION will heavily impact load on CPU.
# If you have a powerful enough computer you may set it to 1080p60

# other
PATH = str(pathlib.Path().absolute()).replace("\\", "/")
CLIP_PATH = PATH + "/clips/{}/{}"
CHECK_VERSION = True  # see if you're running the latest versions
DEBUG = True  # If additional/debug information should be printed (True/False)

DATA = ["c xQcOW", "c Trainwreckstv", "g Just Chatting"]
BLACKLIST = [
    "c ludwig",
    "g Pools, Hot Tubs, and Beaches",
]  # channels/games you dont want to be included in the video

# twitch
CLIENT_ID = ""  # Twitch Client ID
OAUTH_TOKEN = ""  # Twitch OAuth Token
PERIOD = 24  # how many hours since the clip's creation should've passed e.g. 24, 48 etc 0 for all time
LANGUAGE = "en"  # en, es, th etc.
LIMIT = 100  # 1-100


# selenium
ROOT_PROFILE_PATH = r"C:/Users/USERNAME/AppData/Roaming/Mozilla/Firefox/Profiles/r4Nd0m.selenium"  # Path to the Firefox profile where you are logged into YouTube
EXECUTABLE_PATH = r"geckodriver"
FIREFOX_PATH = r"" #specify this if your gecko driver can't find firefox ("Expected browser binary location...")
SLEEP = 3  # How many seconds Firefox should sleep for when uploading
HEADLESS = True  # If True Firefox will be hidden (True/False)


# video options
RENDER_VIDEO = True  # If clips should be rendered into one video (True/False). If set to False everything else under Video will be ignored
RESOLUTION = (
    720,
    1280,
)  # Resolution of the rendered video (height, width) for 1080p: ((1080, 1920))
FRAMES = 30  # Frames per second (30/60)
VIDEO_LENGTH = 10.5  # Minimum video length in minutes (doesn't always work)
RESIZE_CLIPS = True  # Resize clips to fit RESOLUTION (True/False) If any RESIZE option is set to False the video might end up having a weird resolution
FILE_NAME = "rendered"  # Name of the rendered video
ENABLE_INTRO = False  # Enable (True/False)
RESIZE_INTRO = True  # Resize (True/False) read RESIZE_CLIPS
INTRO_FILE_PATH = PATH + "/twitchtube/files/intro.mp4"  # Path to video file (str)
ENABLE_TRANSITION = True
RESIZE_TRANSITION = True
TRANSITION_FILE_PATH = PATH + "/twitchtube/files/transition.mp4"
ENABLE_OUTRO = False
RESIZE_OUTRO = True
OUTRO_FILE_PATH = PATH + "/twitchtube/files/outro.mp4"


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
