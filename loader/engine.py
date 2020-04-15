from loader.created import create_name_file, page_load, create_catalog
from loader.change_files import change_html, files_loader
import logging
import sys
import requests


class SomeException(Exception):   # pragma: no cover
    pass


def app(site, way):
    logger.info('Start program!')
    try:
        file1 = page_load(site, create_name_file(site, way))
    except requests.exceptions.InvalidSchema as e:
        logger.debug(sys.exc_info()[:2])
        logger.error('Ошибка параметров запроса.')
        raise SomeException() from e
    except requests.exceptions.ConnectionError as e:
        logger.debug(sys.exc_info()[:2])
        logger.error(
                     'Неверный адрес сайта либо ошибка подключения.'
                     )
        raise SomeException() from e
    except requests.exceptions.Timeout as e:
        logger.debug(sys.exc_info()[:2])
        logger.error('Истекло время ожидания ответа.')
        raise SomeException() from e
    except FileNotFoundError as e:
        logger.debug(sys.exc_info()[:2])
        logger.error("Указанный каталог не существует.")
        raise SomeException() from e
    except PermissionError as e:
        logger.debug(sys.exc_info()[:2])
        logger.error('Нет прав на внесение изменений.')
        raise SomeException() from e
    logger.info('File created!')
    catalog = create_catalog(file1)
    logger.info('Catalog created!')
    items_src = change_html(file1, catalog, site)
    logger.info('HTML changed!')
    try:
        files_loader(items_src, catalog, site)
    except MemoryError as e:         # pragma: no cover
        logger.debug(sys.exc_info()[:2])
        logger.error('Недостаточно места на диске.')
        raise SomeException() from e
    logger.info('Files upload! The end')
    return file1


logger = logging.getLogger(__name__)    # pragma: no cover
logger.setLevel(logging.DEBUG)    # pragma: no cover


def start_app(site, way, logslevel):   # pragma: no cover
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
        app(site, way)
    except SomeException:
        sys.exit(1)
    else:
        sys.exit(0)
