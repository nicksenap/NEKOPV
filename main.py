from os import listdir
from os.path import isfile, join
import re
from fetch_meta_data import fetch
from pref import leo_perf
import json
import time
from regex import DVD_CODE_REGEX
import os
from dotenv import load_dotenv


def apply_regex(x):
    p = re.compile(DVD_CODE_REGEX)
    dvd_code = None
    try:
        dvd_code = p.search(x).group(1)
    except:
        pass
    return dvd_code


def main():
    load_dotenv()
    FILE_DIR = os.getenv('FILE_DIR')
    f = open("data.json", "a")
    data_stash = []
    onlyfiles = list_file_in_dir(FILE_DIR, leo_perf)
    for file in onlyfiles:
        time.sleep(1)
        data_stash.append(fetch(file))
        # print(file)

    print(data_stash)
    json.dump(data_stash, f)


def list_file_in_dir(dir_path, prefix=[]):
    onlyfiles = [f for f in listdir(dir_path) if isfile(join(dir_path, f))]
    refined_files = list(set([apply_regex(x) for x in onlyfiles]))
    l2file = [file for file in refined_files if file is not None]
    if len(prefix) > 0:
        l2file = [file for file in l2file if file.startswith(tuple(prefix))]
    return l2file


if __name__ == "__main__":
    main()
