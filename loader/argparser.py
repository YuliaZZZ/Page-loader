import argparse
import logging


[DEBUG, INFO, WARNING, ERROR, CRITICAL] = ['debug', 'info',
                                           'warning', 'error',
                                           'critical']


def transform(logslevel):
    if logslevel == DEBUG:
        return logging.DEBUG
    elif logslevel == INFO:
        return logging.INFO
    elif logslevel == WARNING:
        return logging.WARNING
    elif logslevel == ERROR:
        return logging.ERROR
    elif logslevel == CRITICAL:
        return logging.CRITICAL


def arg_parse():     # pragma: no cover
    parser = argparse.ArgumentParser(
           description='Page loader')
    parser.add_argument('site', type=str)
    parser.add_argument(
                        '-o', '--output', type=str, default='.',
                        help='folder to save page')
    parser.add_argument(
                        '-l', '--log', default=INFO,
                        choices=[
                                 DEBUG, INFO, WARNING,
                                 ERROR, CRITICAL],
                        help='logs registration level')
    args = parser.parse_args()
    return args.site, args.output, transform(args.log)
