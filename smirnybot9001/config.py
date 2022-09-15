from pathlib import Path
from dataclasses import dataclass

import tomlkit.toml_file
import typer

DEFAULT_CONFIG_PATH = Path.home() / 'smirnybot9001.conf'
CONFIG_PATH_OPTION = typer.Option(DEFAULT_CONFIG_PATH, '-c', '--config')
CHANNEL_OPTION = typer.Option(None, '--channel', show_default=False)
WIDTH_OPTION = typer.Option(None, '--width', '-w', show_default=False)
HEIGHT_OPTION = typer.Option(None, '--height', '-h', show_default=False)
ADDRESS_OPTION = typer.Option(None, '--address', '-a', show_default=False)
PORT_OPTION = typer.Option(None, '--port', '-p', show_default=False)
DEBUG_OPTION = typer.Option(None, '--debug', '-d', show_default=False)
START_BROWSER_OPTION = typer.Option(None, '--start-browser', '-sb', show_default=False)


@dataclass()
class SmirnyBot9001Config():
    width: int
    height: int
    channel: str
    token: str
    display_wav_abs_path: Path=None
    address: str='127.0.0.1'
    port: int=4711
    start_browser: bool=False
    debug: bool=False

    @classmethod
    def from_file_path(cls, config_path: Path):
        conf_toml = parse_config(config_path)
        def get_value(section, key, notfound=None):
            try:
                return conf_toml[section][key]
            except KeyError:
                return notfound

        width = get_value('overlay', 'width')
        height = get_value('overlay', 'height')
        channel = get_value('chatbot', 'channel')
        token = get_value('chatbot', 'token')
        address =  get_value('overlay', 'address', notfound='127.0.0.1')
        port = get_value('overlay', 'port', notfound=4711)
        start_browser = get_value('overlay', 'start_browser', notfound=False)
        debug = get_value('overlay', 'debug', notfound=False)

        display_wav_path = get_value('overlay', 'display_wav_path', notfound=None)
        if display_wav_path:
            display_wav_path = Path(display_wav_path)
            if not display_wav_path.is_absolute():
                display_wav_path = config_path.parent / display_wav_path

        return cls(width, height, channel, token, display_wav_path, address, port, start_browser, debug)

    def inject_values(self, value_dict: dict):
        for key, value in value_dict.items():
            if value and hasattr(self, key):
                setattr(self, key, value)


def parse_config(config_path):
    tf = tomlkit.toml_file.TOMLFile(config_path)
    return tf.read()


def create_config_and_inject_values(config_path: Path, values: dict):
    if not config_path.exists():
        print(f"[red] Unable to find config file: {config_path}")
        raise typer.Exit(23)
    config = SmirnyBot9001Config.from_file_path(config_path)
    config.inject_values(values)
    return config
