from pathlib import Path

import pytest
from bs4 import BeautifulSoup

from smirnybot9001.overlay import extract_bricklink_part_info

MYDIR = Path(__file__).resolve().parent
TEST_CONF = MYDIR / 'bricklink_part_6339079.html'


def test_read():
    r = open(TEST_CONF).read()
    name, bl_number = extract_bricklink_part_info(r)
    print('name', name)
    print('BL', bl_number)
