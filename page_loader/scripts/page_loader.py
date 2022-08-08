#!/usr/bin/env python
import sys

from page_loader.cli import parse
from page_loader import download
import logging
import os


def main():
    logging.basicConfig(level=logging.INFO)

    args = parse()

    logging.info(f"requested url: {args.web}")
    logging.info(f"output path: {os.path.abspath(args.output)}")

    try:
        download(args.web, args.output)
    except Exception as e:
        logging.error(e)
        raise
    finally:
        sys.exit()


if __name__ == "__main__":
    main()
