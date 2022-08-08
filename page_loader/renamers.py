from page_loader.url import generate_common_path
import re

# import os.path


# def if_exists(obj_path):
#     if os.path.exists(obj_path):
#         file_sys_objs = os.listdir(os.path.dirname(obj_path))
#         file_format_re_obj = re.search(r"\.[a-z]{3,4}$", obj_path)
#
#         if file_format_re_obj:
#             file_format = file_format_re_obj.group(0)
#             obj_path = obj_path[: -len(file_format)]
#         else:
#             file_format = ""
#
#         input_name = os.path.split(obj_path)[-1]
#
#         copy_num_list = []
#         for file_sys_obj in file_sys_objs:
#             file_sys_format_re_obj = re.search(r"\.[a-z]{3,4}$", file_sys_obj)
#
#             if file_sys_format_re_obj:
#                 file_sys_format = file_sys_format_re_obj.group(0)
#             else:
#                 file_sys_format = ""
#
#             if input_name in file_sys_obj and file_sys_format == file_format:
#                 copy_num_obj = re.search(r"\([0-9]{1,2}\)", file_sys_obj)
#
#                 if copy_num_obj is not None:
#                     copy_num = int(copy_num_obj.group(0)[1:-1])
#                     copy_num_list.append(copy_num)
#
#         copy_num_list.sort()
#         if not copy_num_list:
#             return obj_path + "(1)" + file_format
#         for x, y in zip(copy_num_list, copy_num_list[1:]):
#             if x + 1 != y:
#                 return obj_path + f"({x + 1})" + file_format
#         return obj_path + f"({copy_num_list[-1] + 1})" + file_format
#     return obj_path


def save_resource_extension(resource_url: str) -> str:
    resource_extension_re_obj = re.search(r"\.[a-z]{1,5}$", resource_url)

    if resource_extension_re_obj is None:
        return generate_common_path(resource_url)

    resource_extension = resource_extension_re_obj.group(0)
    url_without_extension = resource_url.replace(resource_extension, "")
    return generate_common_path(url_without_extension) + resource_extension
