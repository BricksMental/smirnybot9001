from pathlib import Path

import pytest

from smirnybot9001.overlay import extract_fig_description_and_price

MYDIR = Path(__file__).resolve().parent
TEST_HTML = MYDIR / 'brickset_fig_mk003.html'


def test_read():
    r = open(TEST_HTML, 'r', encoding='utf-8').read()
    description, price_new, price_used = extract_fig_description_and_price(r)
    assert description == 'MK003: Mei - Dragon Armor Suit, Helmet'
    assert price_new == '~€7.66'
    assert price_used == '~€8.94'
