import argparse    # pragma: no cover
import logging


def turn(argument='info'):   # pragma: no cover
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


def start():     # pragma: no cover
    parser = argparse.ArgumentParser(
           description='Page loader')
    parser.add_argument('site', type=str)
    parser.add_argument(
                        '-o', '--output', type=str, default='.',
                        help='folder to save page')
    parser.add_argument(
                        '-l', '--log', default='info',
                        choices=[
                                 'debug', 'info',
                                 'warning', 'error', 'critical'],
                        help='logs registration level')
    args = parser.parse_args()
    return args.site, args.output, turn(args.log)
