from pathlib import Path

from smirnybot9001.color_table import parse_color_table, scrape_color_table

MYDIR = Path(__file__).resolve().parent
COLOR_TABLE_HTML = MYDIR / 'bricklink_color_table.html'


def test_scrape():
    ct = scrape_color_table()


def test_parse():
    r = open(COLOR_TABLE_HTML).read()
    ct = parse_color_table(r)
