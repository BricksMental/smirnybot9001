from pathlib import Path

import tomlkit.toml_file
import typer

DEFAULT_CONFIG_PATH = Path.home() / 'smirnybot9001.conf'
CONFIG_PATH_OPTION = typer.Option(DEFAULT_CONFIG_PATH, '-c', '--config')
CHANNEL_OPTION = typer.Option(None, '--channel')
WIDTH_OPTION = typer.Option(1920, '--width', '-w')
HEIGHT_OPTION = typer.Option(1080, '--height', '-h')
ADDRESS_OPTION = typer.Option('localhost', '--address', '-a')
PORT_OPTION = typer.Option(4711, '--port', '-p')
DEBUG_OPTION = typer.Option(False, '--debug', '-d')
START_BROWSER_OPTION = typer.Option(False, '--start-browser', '-sb')


def parse_config(config_path):
    tf = tomlkit.toml_file.TOMLFile(config_path)
    return tf.read()




