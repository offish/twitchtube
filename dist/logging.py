from datetime import datetime
import colorama


colorama.init()


TYPE = {
    "warn": "\033[1;35;40m",
    "info": "\033[1;32;40m",
    "error": "\033[1;31;40m",
    "normal": "\033[0m"
}


def log(sort: str, to_print: str):
    time = datetime.now().time().strftime('%H:%M:%S')

    if sort in TYPE:
        print(f"{TYPE['info'] + 'twitchtube'} {TYPE['normal'] + '| ' + time } - {TYPE[sort] + sort}: {TYPE['normal'] + to_print}")
    else:
        print(f'{sort} not in TYPE. {to_print}')

