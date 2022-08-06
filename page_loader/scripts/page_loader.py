#!/usr/bin/env python
from page_loader.cli import parse
from page_loader import download
import logging
import os

logging.basicConfig(level=logging.INFO)


def main():
    args = parse()

    logging.info(f"requested url: {args.web}")
    logging.info(f"output path: {os.path.abspath(args.output)}")

    try:
        download(args.web, args.output)
    except Exception as e:
        logging.error(e)
        raise


if __name__ == "__main__":
    main()
