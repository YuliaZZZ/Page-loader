#!/usr/bin/env python3
from loader import start_loader, engine
import sys
import logging


class SomeException(Exception):
    pass


logger = logging.getLogger(__name__)


def main():
    site, way, logslevel = start_loader.start_program()
    logger.setLevel(logslevel)
    f = logging.FileHandler('logsapp.log')
    f.setLevel(logslevel)
    formatter = logging.Formatter(
              '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
              )
    f.setFormatter(formatter)
    logger.addHandler(f)
    console = logging.StreamHandler()
    console.setLevel(logging.ERROR)
    formatter_console = logging.Formatter('%(message)s')
    console.setFormatter(formatter_console)
    logger.addHandler(console)
    try:
        engine.app(site, way)
    except SomeException:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == '__main__':
    main()
