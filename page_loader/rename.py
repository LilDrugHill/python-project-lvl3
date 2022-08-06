from page_loader.url import gen_common_path
import re
import os.path


def if_exists(obj_path):
    if os.path.exists(obj_path):
        file_sys_objs = os.listdir(os.path.dirname(obj_path))
        file_format_obj = re.search(r"\.[a-z]{3,4}$", obj_path)

        file_format, obj_path = save_if_format_exists(file_format_obj, obj_path)

        input_name = os.path.split(obj_path)[-1]

        copy_num_list = []
        for file_sys_obj in file_sys_objs:
            file_sys_format_obj = re.search(r"\.[a-z]{3,4}$", file_sys_obj)

            if file_sys_format_obj:
                file_sys_format = file_sys_format_obj.group(0)
            else:
                file_sys_format = ""

            if input_name in file_sys_obj and file_sys_format == file_format:
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


def save_if_format_exists(file_format_obj, obj_path):
    if file_format_obj:
        file_format = file_format_obj.group(0)
        obj_path = obj_path[: -len(file_format)]
    else:
        file_format = ""
    return file_format, obj_path


def parse_resource_format(
    resource_url: str, save_format: str = ""
) -> str:  # Сохранение формата скаченного ресурса
    resource_extension_obj = re.search(r"\.[a-z]{1,5}$", resource_url)

    if resource_extension_obj is None:
        return gen_common_path(resource_url) + save_format

    resource_extension = resource_extension_obj.group(0)
    url_without_format = resource_url.replace(resource_extension, "")
    return gen_common_path(url_without_format) + resource_extension
