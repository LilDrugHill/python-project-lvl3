from urllib.parse import urlparse, urljoin
import re
import os


def for_resource(site_url: str, resource_link: str):
    parsed_site_url = urlparse(site_url)
    parsed_resource_url = urlparse(resource_link)
    resource_netloc = parsed_resource_url.netloc
    site_netloc = parsed_site_url.netloc
    if (
        resource_netloc == site_netloc
        or resource_netloc
        == ""  # Проверяем путь относительный или ведет к другому домен
    ):
        if resource_netloc == "":
            return urljoin(site_url, parsed_resource_url.path)
        return resource_link
    return None


def gen_common_path(site: str) -> str:
    url = urlparse(site)
    netloc = url.netloc
    path = url.path
    return "-".join(re.split(r"[^a-z^A-Z^0-9]", netloc + path))


def to_dir(site: str) -> str:
    return gen_common_path(site) + "_files"


def to_file(site: str) -> str:
    return gen_common_path(site) + ".html"


def replace_with_path(tag: str, path: str, attribute: str):
    dir, file = os.path.split(path)
    _, dir = os.path.split(dir)
    tag[attribute] = os.path.join(dir, file)
