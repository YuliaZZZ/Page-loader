#!/usr/bin/env python3
import argparse  # pragma: no cover
import sys  # pragma: no cover

from loader.log import (SomeException, setup_log, transform,
                        DEBUG, INFO, WARNING, ERROR,
                        CRITICAL)  # pragma: no cover
from loader.process import make_loader  # pragma: no cover


parser = argparse.ArgumentParser(
       description='Page loader')  # pragma: no cover
parser.add_argument('site', type=str)  # pragma: no cover
parser.add_argument(
                    '-o', '--output', type=str, default='.',
                    help='folder to save page')  # pragma: no cover
parser.add_argument(
                    '-l', '--log', type=transform,
                    choices=[
                             DEBUG, INFO, WARNING, ERROR,
                             CRITICAL], default=transform(INFO),
                    help='logs registration level')  # pragma: no cover
args = parser.parse_args()  # pragma: no cover
logslevel = args.log  # pragma: no cover
site = args.site  # pragma: no cover
directory = args.output  # pragma: no cover


def main():    # pragma: no cover
    logger = setup_log(logslevel)
    try:
        make_loader(site, directory, logger)
    except SomeException:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == '__main__':    # pragma: no cover
    main()
