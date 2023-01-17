from pathlib import Path

import pytest
import tomlkit

from smirnybot9001.config import parse_config, SmirnyBot9001Config

MYDIR = Path(__file__).resolve().parent
TEST_CONF = MYDIR / 'test.conf'
MINIMAL_CONF = MYDIR / 'minimal.conf'
BAD_CONF = MYDIR / 'bad.conf'


@pytest.fixture()
def toml_conf():
    return parse_config(TEST_CONF)


def test_parse(toml_conf):
    assert isinstance(toml_conf, tomlkit.toml_document.TOMLDocument)


def test_create_good_config_obj():
    config = SmirnyBot9001Config.from_file_path(TEST_CONF)
    assert isinstance(config, SmirnyBot9001Config)
    assert config.width == 666
    assert config.height == 1337
    assert config.address == 'WTF'
    assert config.port == 567
    assert config.channel == 'BRICKSMENTAL'
    assert config.token == 'TOPSECRET'
    assert config.display_wav_abs_path.parent == Path(__file__).parent
    assert config.debug is True
    assert config.start_browser is True
    assert config.default_duration == 23


def test_create_minimal_config_obj():
    config = SmirnyBot9001Config.from_file_path(MINIMAL_CONF)
    assert isinstance(config, SmirnyBot9001Config)
    assert config.width == 1920
    assert config.height == 1080
    assert config.address == '::'
    assert config.port == 4711
    assert config.channel is None
    assert config.token == 'TOPSECRET'
    assert config.display_wav_abs_path is None
    assert config.debug is False
    assert config.start_browser is False



def test_bot_section(toml_conf):
    assert toml_conf['chatbot']['token'] == 'TOPSECRET'
    assert toml_conf['chatbot']['channel'] == 'BRICKSMENTAL'

