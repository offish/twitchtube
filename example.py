from time import sleep

from twitchtube.presets import *
from twitchtube.video import make_video


data = ["channel xQcOW", "game Just Chatting"]

while True:
    make_video(data, video_length=2.0)

    sleep(DAILY)
