import requests
from page_loader.names_and_url_parsers import (
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


def download(site_url: str, dir_path: str) -> str:
    path_for_downloads = os.path.join(dir_path, create_name_for_downloads(site_url))

    resources_dir_path = path_for_downloads + "_files"
    resources_dir_path = rename_if_exists(resources_dir_path)

    with alive_bar(title="Downloading site(html)") as bar:
        res = requests.get(site_url)
        res.raise_for_status()
        bar()

    soup = BeautifulSoup(res.text, features="html.parser")

    try:
        os.mkdir(resources_dir_path)
    except Exception as e:
        logging.error(e)
        raise

    logging.info("resources dir was created")
    download_resource(soup, resources_dir_path, site_url)  # Скачивает resource

    html_file_path = path_for_downloads + ".html"
    html_file_path = rename_if_exists(html_file_path)
    with open(html_file_path, "w+") as new_file:
        new_file.write(soup.prettify())

    print(
        f"Your html here: {html_file_path}\nYour resources here: {resources_dir_path}"
    )

    return html_file_path


def download_resource(soup: BeautifulSoup, resources_dir_path: str, site_url: str):
    tags_and_attributes_list = [('img', 'scr'), ('script', 'scr'), ('link', 'href')]
    for tag, attribute in tags_and_attributes_list:
        resource_tags = soup.find_all(tag)  # Поиск по тегу строк
        with alive_bar(title=f"Downloading {tag}s") as bar:
            for resource_tag in resource_tags:  # дальшейший их обход

                if not (resource_link := resource_tag.get(attribute)):  # получение ссылки
                    continue  # если нет необходимого атрибута - пропускаем

                if resource_url := create_resource_url(
                        site_url, resource_link
                ):  # Если None то не скачиваем
                    try:
                        resource_obj = requests.get(resource_url)  # скачивание
                    except requests.exceptions.ConnectionError:
                        logging.warning(f"image {resource_url} was not downloaded")
                    else:
                        resource_path = os.path.join(
                            resources_dir_path, parse_resource_format(resource_url)
                        )

                        with open(resource_path, "wb") as resource_file:
                            resource_file.write(resource_obj.content)

                        create_relative_path(
                            resource_tag, resource_path, attribute
                        )  # Подмена ссылки на путь до img
                        bar()
        logging.info(f"{tag}s downloaded")
