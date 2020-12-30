from datetime import datetime

from colorama import Fore as f
from colorama import init


init()


def log(color: int, sort: str, text: str) -> None:
    """
    Used for colored printing, does not return anything.
    """
    time = datetime.now().time().strftime('%H:%M:%S')
    text.encode(encoding='UTF-8', errors='ignore')
    print(f'{f.GREEN}twitchtube {f.WHITE}| {time} - {color + sort}{f.WHITE}: {text}{f.WHITE}')


class Log:

    def info(self, text: str):
        log(f.GREEN, 'info', text)

    def error(self, text: str):
        log(f.RED, 'error', text)

    def warn(self, text: str):
        log(f.MAGENTA, 'warn', text)
