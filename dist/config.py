import pathlib


# Secrets
CLIENT_ID = ""


# Paths
PATH = str(pathlib.Path().absolute())
CLIP_PATH = PATH + "/clips/{}/{}"


# Requests
HEADERS = {"Accept": "application/vnd.twitchtv.v5+json", "Client-ID": CLIENT_ID}
PARAMS = {"period": "day", "language": "en", "limit": 100}


# Video
GAMES = ["Team Fortress 2", "Rust", "Escape From Tarkov"]
VIDEO_LENGTH = 13.0 # in minutes


TAGS = {
#    "Counter-Strike: Global Offensive": "top csgo twitch clips,best csgo twitch clips,csgo top twitch clips,csgo daily twitch clips,crudecs,crude csgo,most viewed twitch clips csgo,twitch csgo videos,most watched csgo twitch clips ever,csgo twitch clip compilation,twitch csgo clips compilation,csgo clips twitch,csgo clips reddit,csgo clips download,csgo clips in desc,csgo twitch highlights,twitch cs go highlights,twitch highlights csgo,competitive cs go clips,csgo awp wildfire stattrak",
    "Rust": "crude,rust highlights,rust gameplay highlights,rust twitch,rust twitch stream,rust twitch bot,rust twitch prime,rust twitch overlay,rust twitch live,twitch rust clips,twitch rust streamers,top twitch rust streamers,female twitch streamers rust,rust twitch highlights,hjune rust twitch,highlights twitch rust,rust gameplay,rust raid,rust raid clips,rust raid videos,rust stream,rust stream sniping,rust streamer settings,popular rust streamers",
    "Team Fortress 2": "crude,crude tf2,tf2 twitch streamers,tf2 twitch b4nny,tf2 twitch experience,tf2 twitch tv,twitch tf2 klown,twitch tf2 clips,tf2 twitch casual,twitch highlights tf2,tf2 highlights,tf2 clips,tf2 compilation,tf2 clip compilation,tf2 twitch compilation,tf2 stream snipe,tf2 stream highlights,tf2 stream sniping,tf2 stream overlay,twitch experience tf2,team fortress 2 stream,team fortress 2 highlights,team fortress 2 live stream,twitch team fortress 2,b4nny",
    "Escape From Tarkov": "crude,escape from tarkov,escape from tarkov steam,escape from tarkov stream,escape from tarkov streamer items,escape from tarkov streamers,escape from tarkov twitch,escape from tarkov tips and tricks,escape from tarkov twitch drops,escape from tarkov twitch streamers,streamers escape from tarkov,twitch escape from tarkov,twitch escape from tarkov drops,dr disrespect escape from tarkov,escape from tarkov highlights,escape from tarkov nvidia highlights,eft,eft clips"
}


DESCRIPTIONS = {
#   "Counter-Strike: Global Offensive": "",    
    "Rust": "The most viewed RUST Twitch clips today. Daily RUST Twitch clip compilations by crude.\n\n{}\n#RUST #RustHighlights #RustTwitch",
    "Team Fortress 2": "The most viewed TF2 Twitch clips today. Team Fortress 2 twitch highlights compilation by crude.\n\n{}\n#TF2 #TF2Highlights #TeamFortress2",
    "Escape From Tarkov": "Most popular Twitch clips from Escape from Tarkov today - compilation by crude.\n\n{}\n#EscapeFromTarkov #EscapeFromTarkovHighlights #TwitchHighlights"
}
