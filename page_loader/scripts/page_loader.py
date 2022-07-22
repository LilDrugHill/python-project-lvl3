#!/usr/bin/env python
from page_loader.cli import parse
from page_loader import download


def main():
    args = parse()

    html_file_path, resources_dir_path = download(args.web, args.output)
    print(
        f"Your html here: {html_file_path}\nYour resources here: {resources_dir_path}"
    )


if __name__ == "__main__":
    main()
