#!/usr/bin/env python
from page_loader.cli import parse
from page_loader import download


def main():
    args = parse()

    print(download(args.web, args.output))


if __name__ == "__main__":
    main()
