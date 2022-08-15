from urllib.parse import urlparse, urljoin
import re


def for_resource(site_url: str, resource_link: str):
    parsed_resource_url = urlparse(resource_link)
    resource_netloc = parsed_resource_url.netloc
    if resource_netloc in site_url or resource_netloc == "":
        if resource_netloc == "":
            return urljoin(site_url, parsed_resource_url.path)
        return resource_link
    return None


def generate_common_path(site: str) -> str:
    url = urlparse(site)
    netloc = url.netloc
    path = url.path
    return "-".join(re.split(r"[^a-z^A-Z^0-9]", netloc + path))
