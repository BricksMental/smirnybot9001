from pathlib import Path

from smirnybot9001.overlay import extract_bricklink_set_info
from smirnybot9001.util import get_with_user_agent

MYDIR = Path(__file__).resolve().parent
SET_NUM = 'col14-16'
SET_URL = f"https://www.bricklink.com/v2/catalog/catalogitem.page?S={SET_NUM}"
TEST_HTML = MYDIR / f"bricklink_set_col{SET_NUM}.html"


def atest_write():
    r = get_with_user_agent(SET_URL)
    with open(TEST_HTML, 'w', encoding='utf-8') as of:
        of.write(r.text)


def test_read():
    r = open(TEST_HTML).read()
    description = extract_bricklink_set_info(r)
    assert description == 'Spider Lady, Series 14 (Complete Set with Stand and Accessories)'
