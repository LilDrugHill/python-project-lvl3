from urllib.parse import urlparse, urljoin
import re


def get_valid_resource(site_url: str, resource_link: str):
    parsed_resource_url = urlparse(resource_link)
    resource_netloc = parsed_resource_url.netloc

    if resource_netloc == "":
        return urljoin(site_url, parsed_resource_url.path)

    if resource_netloc in site_url:
        return resource_link

    return None


def generate_common_path(url: str) -> str:
    url = urlparse(url)
    netloc = url.netloc
    path = url.path
    return "-".join(re.split(r"[^a-z^A-Z^0-9]", netloc + path))


def to_name(resource_url: str, default_extension: str = "") -> str:
    parsed_resource_url = urlparse(resource_url)
    found_extension_regex = re.search(r"\.[a-z]{1,5}$", parsed_resource_url.path)

    if found_extension_regex is None and default_extension:
        return generate_common_path(resource_url) + default_extension

    resource_extension = found_extension_regex.group(0)
    url_without_extension = resource_url.replace(resource_extension, "")
    return generate_common_path(url_without_extension) + resource_extension
