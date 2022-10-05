from pathlib import Path

import pytest
from bs4 import BeautifulSoup

from smirnybot9001.overlay import extract_bricklink_part_info

MYDIR = Path(__file__).resolve().parent
TEST_CONF = MYDIR / 'bricklink_part_6339079.html'


def test_read():
    r = open(TEST_CONF).read()
    name, bl_number = extract_bricklink_part_info(r)
    assert name == 'LEGO Minifigure, Head Dual Sided Black Eyebrows, Moustache, Open Mouth Grin, White Teeth / Bandage on Forehead Pattern - Hollow Stud'
    assert bl_number == '3626cpb2900'
    print('name', name)
    print('BL', bl_number)
