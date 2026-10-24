from __future__ import annotations

import argparse
import logging
import sys


def main():
    logging.basicConfig(
        stream=sys.stderr, level="INFO", format="%(levelname)s;%(asctime)s;%(message)s"
    )

    argparser = argparse.ArgumentParser(description="Solve SALBP-1 Instance")
    # argparser.add_argument(
    #     "input_file", type=str, help="Path to the input instance file"
    # )
    _ = argparser.parse_args()

    # with open(args.input_file) as _:
    #     ...


if __name__ == "__main__":
    main()
