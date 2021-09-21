from datetime import datetime

from colorama import Fore as f
from colorama import init

from .config import DEBUG
from .utils import get_date

init()


def write_to_logs(text: str) -> None:
    with open("twitchtube/files/logs.txt", "a") as f:
        f.write("\n" + text)


def log(color: int, sort: str, text: str) -> None:
    """
    Used for colored printing, does not return anything.
    """
    time = datetime.now().time().strftime("%H:%M:%S")
    text.encode(encoding="UTF-8", errors="ignore")

    if not DEBUG and sort == "debug":
        return

    if DEBUG:
        write_to_logs(f"{get_date()} @ {time} - {sort}: {text}")

    print(
        f"{f.GREEN}twitchtube {f.WHITE}| {time} - {color + sort}{f.WHITE}: {text}{f.WHITE}"
    )


class Log:
    @staticmethod
    def info(text: str):
        log(f.GREEN, "info", text)

    @staticmethod
    def error(text: str):
        log(f.RED, "error", text)

    @staticmethod
    def warn(text: str):
        log(f.YELLOW, "warn", text)

    @staticmethod
    def clip(text: str):
        log(f.CYAN, "clip", text)

    @staticmethod
    def debug(text: str):
        log(f.BLUE, "debug", text)
