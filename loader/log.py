import logging


class SomeException(Exception):   # pragma: no cover
    pass


[DEBUG, INFO, WARNING, ERROR, CRITICAL] = [10, 20, 30, 40, 50]


def transform(log):    # pragma: no cover
    value_log = logging.DEBUG
    if DEBUG == log:
        value_log = logging.DEBUG
    elif INFO == log:
        value_log = logging.INFO
    elif WARNING == log:
        value_log = logging.WARNING
    elif ERROR == log:
        value_log = logging.ERROR
    elif CRITICAL == log:
        value_log = logging.CRITICAL
    return value_log


def setup_log(logslevel, logfile='logsapp.log'):     # pragma: no cover
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    console = logging.StreamHandler()
    console.setLevel(logging.ERROR)
    formatter_console = logging.Formatter('%(message)s')
    console.setFormatter(formatter_console)
    logger.addHandler(console)
    f = logging.FileHandler(logfile)
    f.setLevel(logslevel)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
    f.setFormatter(formatter)
    logger.addHandler(f)
    return logger
