import requests
from page_loader.refactors import (
    create_name_for_downloads,
    rename_if_exists,
    create_relative_path,
    create_resource_url,
    parse_resource_format,
)
import os.path
from bs4 import BeautifulSoup
from alive_progress import alive_bar
import logging

logging.basicConfig(level=logging.INFO)


def download(site_url: str, dir_path: str, downloader: classmethod = requests) -> str:
    abs_dir_path = os.path.abspath(dir_path)

    logging.info(f"requested url: {site_url}")
    logging.info(f"output path: {abs_dir_path}")

    path_for_downloads = os.path.join(dir_path, create_name_for_downloads(site_url))

    resources_dir_path = path_for_downloads + "_files"
    resources_dir_path = rename_if_exists(resources_dir_path)
    try:
        os.mkdir(resources_dir_path)
    except PermissionError:
        logging.error(
            f"sorry you don't have permission to change directory {abs_dir_path}."
            f" Change permission or use another directory."
        )
        raise PermissionError()

    except FileNotFoundError:
        logging.error(
            f"sorry directory {abs_dir_path}is not exists. Check specified path."
        )
        raise FileNotFoundError()

    logging.info("resources dir was created")

    try:
        with alive_bar(title="Downloading site(html)") as bar:
            res = downloader.get(site_url)

    except requests.exceptions.ConnectionError:
        logging.error(
            "failed to establish a new connection: nodename nor servname provided, or not known."
        )
        os.rmdir(resources_dir_path)
        logging.info('resources dir was deleted')
        raise requests.exceptions.ConnectionError()

    except requests.exceptions.MissingSchema:
        logging.error(f"url '{site_url}' is invalid.")
        os.rmdir(resources_dir_path)
        logging.info('resources dir was deleted')
        raise requests.exceptions.MissingSchema()

    else:
        if not res:
            raise requests.exceptions.ConnectionError(f'{res.status_code}')

        bar()
        soup = BeautifulSoup(res.text, features="html.parser")

    img_download(soup, resources_dir_path, site_url, downloader)  # Скачивает img
    scripts_download(
        soup, resources_dir_path, site_url, downloader
    )  # Скачивает scripts
    links_download(soup, resources_dir_path, site_url, downloader)  # Скачивает links

    html_file_path = path_for_downloads + ".html"
    html_file_path = rename_if_exists(html_file_path)
    with open(html_file_path, "w+") as new_file:
        new_file.write(soup.prettify())

    print(
        f"Your html here: {html_file_path}\nYour resources here: {resources_dir_path}"
    )

    return html_file_path


def img_download(
    soup: BeautifulSoup, resources_dir_path: str, site_url: str, downloader: classmethod
):
    img_tags = soup.find_all("img")  # Поиск по тегу строк с img
    with alive_bar(title="Downloading images") as bar:
        for img_tag in img_tags:  # дальшейший их обход
            img_link = img_tag["src"]  # получение ссылки на img

            if img_url := create_resource_url(
                site_url, img_link
            ):  # Если None то не скачиваем
                try:
                    img_resource = downloader.get(img_url)  # скачивание
                except requests.exceptions.ConnectionError:
                    logging.warning(f"image {img_url} was not downloaded")
                else:
                    img_path = os.path.join(
                        resources_dir_path, parse_resource_format(img_url)
                    )

                    with open(img_path, "wb") as img_file:
                        img_file.write(img_resource.content)

                    create_relative_path(
                        img_tag, img_path, "src"
                    )  # Подмена ссылки на путь до img
                    bar()
    logging.info("images downloaded")


def scripts_download(
    soup: BeautifulSoup, resources_dir_path: str, site_url: str, downloader: classmethod
):
    script_tags = soup.find_all("script")
    with alive_bar(title="Downloading scripts") as bar:
        for script_tag in script_tags:
            if not (script_link := script_tag.get("src")):
                continue

            if script_url := create_resource_url(site_url, script_link):
                try:
                    script_resource = downloader.get(script_url)
                except requests.exceptions.ConnectionError:
                    logging.warning(f"script {script_url} was not downloaded")
                else:
                    script_path = os.path.join(
                        resources_dir_path, parse_resource_format(script_url)
                    )

                    with open(script_path, "wb") as script_file:
                        script_file.write(script_resource.content)

                    create_relative_path(
                        script_tag, script_path, "src"
                    )  # Подмена ссылки на путь до script
                    bar()
    logging.info("scripts downloaded")


def links_download(
    soup: BeautifulSoup, resources_dir_path: str, site_url: str, downloader: classmethod
):
    link_tags = soup.find_all("link")
    with alive_bar(title="Downloading links") as bar:
        for link_tag in link_tags:
            link_link = link_tag["href"]

            if link_url := create_resource_url(site_url, link_link):
                try:
                    link_resource = downloader.get(link_url)
                    link_path = os.path.join(
                        resources_dir_path, parse_resource_format(link_url, '.html')
                    )

                except requests.exceptions.ConnectionError:
                    logging.warning(f"link {link_url} was not downloaded")
                else:
                    with open(link_path, "wb") as link_file:
                        link_file.write(link_resource.content)

                    create_relative_path(
                        link_tag, link_path, "href"
                    )  # Подмена ссылки на путь до link
                    bar()
    logging.info("links downloaded")
