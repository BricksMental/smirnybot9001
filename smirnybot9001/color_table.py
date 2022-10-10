from bs4 import BeautifulSoup

from smirnybot9001.util import get_with_user_agent

COLOR_TABLE_URL = 'https://www.bricklink.com/catalogColors.asp'

COLOR_TABLE = None


def get_color_table():
    global COLOR_TABLE
    if COLOR_TABLE is None:
        COLOR_TABLE = scrape_color_table()
    return COLOR_TABLE



def scrape_color_table():
    r = get_with_user_agent(COLOR_TABLE_URL)
    return parse_color_table(r.text)


def parse_color_table(color_table_html):

    ret = dict()

    soup = BeautifulSoup(color_table_html, 'html.parser')
    t = soup.find('table', attrs={'id': 'id-main-legacy-table'})
    tables = t.td.find_all('table')
    # fetch all subtables of color groups
    for color_table_index in range(3, 33, 3):
        color_table = tables[color_table_index]
        # skip the column names
        for color_row in color_table.contents[2:]:
            id_td = color_row.contents[0]
            color_id = int(id_td.font.text)
            name_td = color_row.contents[3]
            color_name = name_td.font.text.strip().lower()
            # print(color_name, color_id)
            ret[color_name] = color_id
            ret[color_id] = color_name

    return ret
