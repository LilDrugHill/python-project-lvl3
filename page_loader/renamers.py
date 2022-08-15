from page_loader.url import generate_common_path
import re
import os


def create_name_for_saved(
    path: str, resource_url: str, desired_extension: str = ""
) -> str:
    resource_extension_re_obj = re.search(r"\.[a-z]{1,5}$", resource_url)

    if resource_extension_re_obj is None or desired_extension:
        return os.path.join(
            path, generate_common_path(resource_url) + desired_extension
        )

    resource_extension = resource_extension_re_obj.group(0)
    url_without_extension = resource_url.replace(resource_extension, "")
    return os.path.join(
        path, generate_common_path(url_without_extension) + resource_extension
    )
