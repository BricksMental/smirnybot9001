import signal
import sys
from multiprocessing import Process
from pathlib import Path

import typer
from rich import print

from smirnybot9001.chatbot import run_bot
from smirnybot9001.config import SmirnyBot9001Config, create_config_and_inject_values, CONFIG_PATH_OPTION, WIDTH_OPTION, HEIGHT_OPTION, \
    ADDRESS_OPTION, PORT_OPTION, CHANNEL_OPTION, START_BROWSER_OPTION, DEBUG_OPTION
from smirnybot9001.overlay import start_overlay

root = typer.Typer(add_completion=False, invoke_without_command=True, no_args_is_help=True,
                   pretty_exceptions_show_locals=False)


class SmirnyBot9001Boot:
    def __init__(self, config: SmirnyBot9001Config):
        # init the members to None before installing the signal handler
        self.overlay = None
        self.chatbot = None

        signal.signal(signal.SIGINT, self.signal_handler)

        self.overlay = Process(target=start_overlay, args=(config, ))
        self.chatbot = Process(target=run_bot, args=(config, ))
        self.overlay.start()
        self.chatbot.start()
        self.overlay.join()
        self.overlay.join()
        print('[green]DONE')

    def signal_handler(self, signum, _frame):
        print(f"[red] Got signal {signum}. Terminating Overlay and Chatbot")
        if self.overlay and self.overlay.is_alive():
            self.overlay.terminate()
        if self.chatbot and self.chatbot.is_alive():
            self.chatbot.terminate()
        sys.exit(0)


def main():
    app = typer.Typer(add_completion=False, invoke_without_command=True, no_args_is_help=True,
                      pretty_exceptions_enable=False)

    @app.command()
    def start(config_path: Path = CONFIG_PATH_OPTION,
              width: int = WIDTH_OPTION,
              height: int = HEIGHT_OPTION,
              channel: str = CHANNEL_OPTION,
              address: str = ADDRESS_OPTION,
              port: int = PORT_OPTION,
              start_browser: bool = START_BROWSER_OPTION,
              debug: bool = DEBUG_OPTION, ):

        config = create_config_and_inject_values(config_path, locals())
        SmirnyBot9001Boot(config)

    app(help_option_names=('-h', '--help'))


if __name__ == '__main__':
    main()
