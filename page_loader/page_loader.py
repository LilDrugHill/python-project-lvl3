import requests
from page_loader import url
import os.path
from bs4 import BeautifulSoup
from progress.spinner import Spinner
import logging
import threading


def download(site_url: str, dir_path: str) -> str:
    resources_dir_path = os.path.join(
        dir_path, url.to_name(site_url, default_extension="_files")
    )

    spinner = Spinner("Downloading site(html) ")
    downloaded_obj = requests.get(site_url)
    downloaded_obj.raise_for_status()
    spinner.next()

    soup = BeautifulSoup(downloaded_obj.text, features="html.parser")

    os.mkdir(resources_dir_path)

    logging.info("resources dir was created")
    soup, assets = prepare_data_for_download(soup, resources_dir_path, site_url)

    download_and_save_resources(assets)
    logging.info("resources downloaded")

    html_file_path = os.path.join(
        dir_path, url.to_name(site_url, default_extension=".html")
    )

    with open(html_file_path, "w+") as new_file:
        new_file.write(soup)

    print(
        f"Your html here: {html_file_path}\nYour resources here: {resources_dir_path}"
    )

    return html_file_path


def prepare_data_for_download(
    soup: BeautifulSoup, resources_dir_path: str, site_url: str
):
    tags_and_attributes = (
        ("img", "src", ""),
        ("script", "src", ""),
        ("link", "href", ".html"),
    )
    resources = []
    for tag, attribute, default_extension in tags_and_attributes:
        resource_tags = soup.find_all(tag)
        #
        for resource_tag in resource_tags:

            if not (resource_link := resource_tag.get(attribute)):
                continue

            if resource_url := url.get_valid_resource(site_url, resource_link):
                resource_path = os.path.join(
                    resources_dir_path,
                    url.to_name(resource_url, default_extension=default_extension),
                )

                resources.append((resource_path, resource_url))

                dir, file = os.path.split(resource_path)
                _, dir = os.path.split(dir)
                resource_tag[attribute] = os.path.join(dir, file)

    return soup.prettify(), resources


def download_and_save_resources(assets: list):
    spinner = Spinner("Downloading resources ")

    for resource_path, resource_url in assets:
        t = threading.Thread(target=download_and_save_one, args=(resource_url, resource_path))
        t.start()
        spinner.next()
    t.join()


def download_and_save_one(resource_url, resource_path):
    response = requests.get(resource_url)

    response.raise_for_status()

    with open(resource_path, "wb") as resource_file:
        resource_file.write(response.content)
