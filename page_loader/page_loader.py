import requests
from page_loader.renamers import (
    generate_common_path,
    save_resource_extension,
)

# from page_loader import renamers
from page_loader import url
import os.path
from bs4 import BeautifulSoup
from alive_progress import alive_bar
import logging

logging.basicConfig(level=logging.INFO)


def download(site_url: str, dir_path: str) -> str:
    path_for_downloads = os.path.join(dir_path, generate_common_path(site_url))

    resources_dir_path = path_for_downloads + "_files"
    # resources_dir_path = renamers.if_exists(resources_dir_path)

    with alive_bar(title="Downloading site(html)") as bar:
        downloaded_obj = requests.get(site_url)
        downloaded_obj.raise_for_status()
        bar()

    soup = BeautifulSoup(downloaded_obj.text, features="html.parser")

    os.mkdir(resources_dir_path)

    logging.info("resources dir was created")
    download_resources(soup, resources_dir_path, site_url)

    html_file_path = path_for_downloads + ".html"
    # html_file_path = renamers.if_exists(html_file_path)
    with open(html_file_path, "w+") as new_file:
        new_file.write(soup.prettify())

    print(
        f"Your html here: {html_file_path}\nYour resources here: {resources_dir_path}"
    )

    return html_file_path


def download_resources(soup: BeautifulSoup, resources_dir_path: str, site_url: str):
    tags_and_attributes_list = [("img", "src"), ("script", "src"), ("link", "href")]
    for tag, attribute in tags_and_attributes_list:
        resource_tags = soup.find_all(tag)
        with alive_bar(title=f"Downloading {tag}s") as bar:
            for resource_tag in resource_tags:

                if not (resource_link := resource_tag.get(attribute)):
                    continue

                if resource_url := url.for_resource(site_url, resource_link):
                    resource_path = download_resource(resource_url, resources_dir_path)

                    dir, file = os.path.split(resource_path)
                    _, dir = os.path.split(dir)
                    resource_tag[attribute] = os.path.join(dir, file)

                    bar()
        logging.info(f"{tag}s downloaded")


def download_resource(resource_url: str, resources_dir_path: str):
    downloaded_obj = requests.get(resource_url)

    try:
        downloaded_obj.raise_for_status()
    except Exception as e:
        logging.warning(f"resource {resource_url} was not downloaded. {e}")
    else:
        resource_path = os.path.join(
            resources_dir_path, save_resource_extension(resource_url)
        )

        with open(resource_path, "wb") as resource_file:
            resource_file.write(downloaded_obj.content)

    return resource_path
