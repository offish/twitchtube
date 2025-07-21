from dataclasses import dataclass
from pathlib import Path


@dataclass
class Options:
    client_id: str
    oauth_token: str
    period: int = 0
    language: str = "en"
    max_amount_clips: int = 100
    check_updates: bool = True
    debug: bool = True
    delete_clips_after_render: bool = True
    save_youtube_metadata: bool = True


@dataclass
class SeleniumOptions:
    headless: bool = True
    profile_path: Path = None
    executable_path: str = "geckodriver"


@dataclass
class YoutubeOptions:
    upload: bool = True
    visibility: str = "public"
    title: str = None
    description: str = None
    tags: list[str] = None
    playlists: list[str] = None


@dataclass
class VideoOptions:
    resolution: tuple = (1080, 1920)
    fps: int = 60
    resize_clips: bool = True
    output_path: Path = None
    intro_path: Path = None
    outro_path: Path = None
    transition_path: Path = None
    background_music_path: Path = None


@dataclass
class MoviePyOptions:
    # render with gpu etc.
    pass
