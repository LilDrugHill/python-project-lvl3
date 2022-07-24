from urllib.parse import urlparse, urljoin
import re
import os.path


def create_resource_url(site_url: str, resource_link: str):
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


def create_relative_path(tag: str, path: str, attribute: str):
    dir, file = os.path.split(path)
    _, dir = os.path.split(dir)
    tag[attribute] = os.path.join(dir, file)


def rename_if_exists(obj_path):
    if os.path.exists(obj_path):
        input_name = os.path.split(obj_path)[-1]
        file_sys_objs = os.listdir(os.path.dirname(obj_path))
        file_format_obj = re.search(r"\.[a-z]{3,4}$", obj_path)

        if file_format_obj:
            file_format = file_format_obj.group(0)
        else:
            file_format = ""

        copy_num_list = []
        for file_sys_obj in file_sys_objs:
            if input_name in file_sys_obj:
                copy_num_obj = re.search(r"\([0-9]{1,2}\)", file_sys_obj)

                if copy_num_obj is not None:
                    copy_num = int(copy_num_obj.group(0)[1:-1])
                    copy_num_list.append(copy_num)

        copy_num_list.sort()
        if not copy_num_list:
            return obj_path + "(1)" + file_format
        for x, y in zip(copy_num_list, copy_num_list[1:]):
            if x + 1 != y:
                return obj_path + f"({x + 1})" + file_format
        return obj_path + f"({copy_num_list[-1] + 1})" + file_format
    return obj_path


def parse_resource_format(
    resource_url: str,
    save_format: str = ''
) -> str:  # Сохранение формата скаченного ресурса
    resource_format_obj = re.search(r"\.[a-z]{1,5}$", resource_url)

    if resource_format_obj is None:
        return create_name_for_downloads(resource_url) + save_format

    resource_format = resource_format_obj.group(0)
    url_without_format = resource_url.replace(resource_format, "")
    return create_name_for_downloads(url_without_format) + resource_format


def create_name_for_downloads(site: str) -> str:
    url = urlparse(site)
    netloc = url.netloc
    path = url.path
    return "-".join(re.split(r"[^a-z^A-Z^0-9]", netloc + path))
