import requests
from urllib.parse import urlparse
import re
import os.path


def parse_name(site):
    url = urlparse(site)
    netloc = url.netloc
    path = url.path
    return "-".join(re.split(r"[^a-z^A-Z^0-9]", netloc + path)) + ".html"


def download(site, dir_path):
    res = requests.get(site)
    file_name = parse_name(site)
    new_file_path = os.path.join(dir_path, file_name)
    with open(new_file_path, "w+") as new_file:
        new_file.write(res.text)
    return new_file_path
