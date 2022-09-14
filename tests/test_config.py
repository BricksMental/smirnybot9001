from pathlib import Path

import pytest
import tomlkit

from smirnybot9001.config import parse_config

TEST_CONF = Path(__file__).resolve().parent / 'test.conf'


@pytest.fixture()
def toml_conf():
    return parse_config(TEST_CONF)


def test_parse(toml_conf):
    assert isinstance(toml_conf, tomlkit.toml_document.TOMLDocument)


def test_bot_section(toml_conf):
    assert toml_conf['chatbot']['token'] == 'TOPSECRET'
    assert toml_conf['chatbot']['channel'] == 'bricksmental'

