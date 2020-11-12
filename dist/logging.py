from datetime import datetime

from colorama import Fore as f
from colorama import init

init()

class log:

    def info(self, text: str):
        self.log(f.GREEN, 'info', text)

    def error(self, text: str):
        self.log(f.RED, 'error', text)

    def warn(self, text: str):
        self.log(f.MAGENTA, 'warn', text)

    def log(self, color, sort, text):
        time = datetime.now().time().strftime('%H:%M:%S')
        print(f'{f.GREEN}twitchtube {f.WHITE}| {time} - {color + sort}{f.WHITE}: {text}{f.WHITE}')
