import yaml
import colorama

from datetime import datetime

config = yaml.load(open("./Config/config.yml", 'r'), Loader=yaml.FullLoader)
colorama.init(autoreset=True)

default = colorama.Fore.CYAN
start_up = colorama.Fore.GREEN
debug = colorama.Fore.YELLOW
error = colorama.Fore.BLUE
critical = colorama.Fore.RED


def timestamp():
    return datetime.now().strftime("%H:%M:%S")


class Log:
    def __init__(self):
        pass

    @staticmethod
    async def start_up(message):
        if config['logger']['start_up']:
            print(f'{start_up}[START UP|{timestamp()}] {message}')

    @staticmethod
    async def info(message):
        if config['logger']['info']:
            print(f'{default}[INFO|{timestamp()}] {message}')

    @staticmethod
    async def debug(message):
        if config['logger']['debug']:
            print(f'{debug}[DEBUG|{timestamp()}] {message}')

    @staticmethod
    async def error(err):
        if config['logger']['error']:
            print(f'{error}[ERROR|{timestamp()}] {err}')

    @staticmethod
    async def critical(err):
        if config['logger']['critical']:
            print(f'{critical}[CRITICAL|{timestamp()}] {err}')
