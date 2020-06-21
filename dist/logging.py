from datetime import datetime

import colorama

colorama.init()

class log:
    white = '\033[0m'
    green = '\033[1;32;40m'
    red = '\033[1;31;40m'
    purple = '\033[1;35;40m'

    def info(self, text: str):
        self.log(self.green, 'info', text)

    def error(self, text: str):
        self.log(self.red, 'error', text)

    def warn(self, text: str):
        self.log(self.purple, 'warn', text)

    def log(self, color, sort, text):
        time = datetime.now().time().strftime('%H:%M:%S')
        print(f'{self.green}twitchtube {self.white}| {time} - {color + sort}{self.white}: {text}')
