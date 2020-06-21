import pathlib

# Note: 
# Changing FRAMES and or RESOULTION will heavily impact load on CPU.
# If you have a powerful enough computer you may set it to 1080p60 

# Secrets
CLIENT_ID = ''
OAUTH_TOKEN = ''

# Paths
PATH = str(pathlib.Path().absolute())
CLIP_PATH = PATH + '/clips/{}/{}'


# Video
GAMES = ['Rust', 'Team Fortress 2']
VIDEO_LENGTH = 10.5 # in minutes (doesn't always work for some reason)
FRAMES = 30 # Frames per second 30 or 60
RESOLUTION = (720, 1280) # (height, width) for 1080p: (1080, 1920)


# Twitch

# Twitch API Request Options
HEADERS = {'Accept': 'application/vnd.twitchtv.v5+json', 'Client-ID': CLIENT_ID}
PARAMS = {'period': 'day', 'language': 'en', 'limit': 100}  # 100 is max


# YouTube

# YouTube Video
TITLE = ''
# If not given a title it would take the title of the first clip, and add "- *game* Highlights #"

CATEGORY = 20 # 20 for Gaming


# YouTube Tags
TAGS = {
#    'Counter-Strike: Global Offensive': 'top csgo twitch clips,best csgo twitch clips,csgo top twitch clips,csgo daily twitch clips,crudecs,crude csgo,most viewed twitch clips csgo,twitch csgo videos,most watched csgo twitch clips ever,csgo twitch clip compilation,twitch csgo clips compilation,csgo clips twitch,csgo clips reddit,csgo clips download,csgo clips in desc,csgo twitch highlights,twitch cs go highlights,twitch highlights csgo,competitive cs go clips,csgo awp wildfire stattrak',
    'Rust': 'rust, rust twitch, rust twitch clips',
    'Team Fortress 2': 'tf2, tf2 twitch, tf2 twitch clips',
}

# YouTube Descriptions
DESCRIPTIONS = {
#   'Counter-Strike: Global Offensive': ',    
    'Rust': 'The most viewed RUST Twitch clips today. Daily RUST Twitch clip compilations.\n\n{}\n#RUST #RustHighlights #RustTwitch',
    'Team Fortress 2': 'The most viewed TF2 Twitch clips today. Daily TF2 Twitch clip compilations.\n\n{}\n#TF2 #TF2Highlights #TeamFortress2'
}
