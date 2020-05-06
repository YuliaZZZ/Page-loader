#!/usr/bin/env python3
import argparse
import sys

from loader.log import (SomeException, setup_log, transform,
                        DEBUG, INFO, WARNING, ERROR, CRITICAL)
from loader.process import make_loader


parser = argparse.ArgumentParser(
       description='Page loader')
parser.add_argument('site', type=str)
parser.add_argument(
                    '-o', '--output', type=str, default='.',
                    help='folder to save page')
parser.add_argument(
                    '-l', '--log', type=transform,
                    choices=[
                             DEBUG, INFO, WARNING, ERROR,
                             CRITICAL], default=transform(INFO),
                    help='logs registration level')
args = parser.parse_args()
logslevel = args.log
site = args.site
directory = args.output


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
