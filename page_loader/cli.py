import argparse
import os


def parse():
    parser = argparse.ArgumentParser(
        description="Downloads the page from the network and puts it in the specified\
existing directory (by default, in the program launch directory)"
    )

    parser.add_argument("-o", "--output", help="Storage directory", default=os.getcwd())
    parser.add_argument("web", help="Downloadable site")

    return parser.parse_args()
