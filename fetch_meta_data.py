import requests
from lxml import html
import re
from pref import leo_perf
from regex import TITLE_REGEX
import os


def main():
    dvd_code = "UNKW-63"
    print(fetch(dvd_code))


def process_title(title):
    return re.compile(TITLE_REGEX).search(title).group(1)


def insert_zero(title):
    code = title.split("-")[0]
    number = title.split("-")[1]
    return code + "-" + "0" + number


def fetcher_001(dvd_code):
    # leo
    FETCHER_001_URL = os.getenv('FETCHER_001_URL')
    url = FETCHER_001_URL
    print(f"Fetching {dvd_code} using {FETCHER_001_URL}...")
    new_url = url + "/" + dvd_code.lower()
    r = requests.get(new_url)
    tree = html.fromstring(r.content)
    title = tree.xpath('//title/text()')
    if "not found" in title[0]:
        new_dvd_code = insert_zero(dvd_code)
        print(
            f"{dvd_code} not found, trying to insert 0 in front of number ({new_dvd_code})...")
        return fetcher_001(new_dvd_code)
    tags = tree.xpath('//span[@class="tags-links"]/a/text()')
    publisher = tree.xpath('//span[@class="cat-links"]/a/text()')
    img_url = tree.xpath('//div[@class="entry-content"]/p/a/img/@src')
    data_entry = {"dvd_code": dvd_code, "title": process_title(
        title[0]), "tags": tags, "publisher": publisher[0], "img_url": img_url[0]}
    return data_entry


def fetch(dvd_code):
    if dvd_code.startswith(tuple(leo_perf)):
        return fetcher_001(dvd_code)


if __name__ == "__main__":
    main()
