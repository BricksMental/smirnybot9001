import re
import requests
from fake_user_agent import user_agent

MAX_SET_NR_LENGTH = 128
VALID_SET_CHARS = r'[\w\d\-]'


def is_valid_set_number(candidate):
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

is_valid_fig_number = is_valid_set_number






def get_with_user_agent(url):
    return requests.get(url, headers={'User-Agent': user_agent()})