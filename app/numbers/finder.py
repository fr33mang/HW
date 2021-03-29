import logging
import re
import sys
from concurrent.futures import ThreadPoolExecutor

import requests

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def get_number(link):
    try:
        response = requests.get(link)
    except Exception as e:
        logger.warning(e)
        return

    regex = (r">(?:\+)?(?: )?([7,8])?(?: )?(?:\(?([0-9]{3,4})\)?)?"
             r"(?: )?([0-9]{2,3}[?: \-]?[0-9]{2,3}[?: \-]?[0-9]{2,3})<")  # оптимизировать
    res = re.findall(regex, str(response.content))  # CPU bound, GIL
    if not res:
        logger.warning(f"Finder error, link: {link}")
        return

    country, city, number = res[0]

    city = city or "495"
    number = number.replace("-", "").replace(" ", "")

    number = f"8{city}{number}"

    logger.info(f"Found number {number} in url {link}")
    return number


def find(filepath, max_workers=10):
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        for link in open(filepath, "r"):
            executor.submit(get_number, link.strip("\n"))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise ValueError("pass links file path")

    links_file = sys.argv[1]
    find(links_file)
