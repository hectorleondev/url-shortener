import json
import os
from datetime import datetime
from math import floor
import random

from src.data import schema
import string
from string import ascii_lowercase
from string import ascii_uppercase


def get_content_json(filename: str) -> dict:
    """
    get json content
    :param filename:
    :return:
    """
    with open(f"{os.path.dirname(schema.__file__)}/{filename}.json") as f:
        data = json.load(f)
    return data


def to_base62(num: int, b: int = 62) -> any:
    if b <= 0 or b > 62:
        return 0
    base = string.digits + ascii_lowercase + ascii_uppercase
    r = num % b
    res = base[r]
    q = floor(num / b)
    while q:
        r = q % b
        q = floor(q / b)
        res = base[int(r)] + res
    return res


def to_base10(num: str, b: int = 62) -> int:
    base = string.digits + ascii_lowercase + ascii_uppercase
    limit = len(num)
    res = 0
    for i in range(limit):
        res = b * res + base.find(num[i])
    return res


def generate_id() -> int:
    current_date = datetime.now()
    timestamp = int(current_date.strftime("%Y%m%d%H%M%S"))

    random_chars = ''.join(random.choices(string.digits, k=9))
    return timestamp + int(random_chars)
