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
    def info(self, text: str):
        log(f.GREEN, "info", text)

    def error(self, text: str):
        log(f.RED, "error", text)

    def warn(self, text: str):
        log(f.YELLOW, "warn", text)

    def clip(self, text: str):
        log(f.CYAN, "clip", text)

    def debug(self, text: str):
        log(f.BLUE, "debug", text)
