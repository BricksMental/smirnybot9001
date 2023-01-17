import re
import requests
from fake_user_agent import user_agent

MAX_SET_NR_LENGTH = 128
VALID_SET_CHARS = r'[\w\d\-]'


def is_identifier(candidate):
    try:
        candidate = str(candidate)
    except ValueError:
        return False
    if len(candidate) > MAX_SET_NR_LENGTH:
        return False
    pattern = f"^{VALID_SET_CHARS}+$"
    m = re.search(pattern, candidate, re.ASCII)
    if m is None:
        return False
    return True


def get_with_user_agent(url):
    return requests.get(url, headers={'User-Agent': user_agent()})


def parse_bricklink_meta_description(meta_description):
    pattern = 'ItemName: LEGO (?P<name>.*), ItemType: (?P<type>.*), ItemNo: (?P<nr>.*?), '
    match = re.search(pattern, meta_description)
    if match is None:
        raise ValueError(f"Not a valid bricklink meta description: {meta_description}")
    return match.group('name'), match.group('type'), match.group('nr')
