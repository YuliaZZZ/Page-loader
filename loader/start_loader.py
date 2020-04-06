import argparse    # pragma: no cover
from loader import engine  # pragma: no cover
import logging


def turn(argument='info'):
    if argument == 'debug':
        return logging.DEBUG
    elif argument == 'info':
        return logging.INFO
    elif argument == 'warning':
        return logging.WARNING
    elif argument == 'error':
        return logging.ERROR
    elif argument == 'critical':
        return logging.CRITICAL


parser = argparse.ArgumentParser(description='Page loader')  # pragma: no cover
parser.add_argument('site', type=str)      # pragma: no cover
parser.add_argument('-o', '--output', type=str, default='.',
                    help='folder to save page')            # pragma: no cover
parser.add_argument('-l', '--log', default='info',
                    choices=['debug', 'info', 'warning', 'error', 'critical'],
                    help='logs registration level')
args = parser.parse_args()     # pragma: no cover
file_new = engine.app(args.site, args.output, turn(args.log))      # pragma: no cover
