from loader.scripts.page_loader import logger, SomeException
from loader.created import create_name_file, page_load, create_catalog
from loader.file_conversion import change_html, files_loader
import requests
from progress.spinner import Spinner
import sys


spinner = Spinner('Loading ')


def app(site, way):
    logger.info('Start program!')
    file_html = create_name_file(site, way)
    spinner.next()
    try:
        page_load(site, file_html)
        spinner.next()
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
    catalog = create_catalog(file_html)
    logger.info('Catalog created!')
    items_src = change_html(file_html, catalog)
    logger.info('HTML changed!')
    try:
        files_loader(items_src, site)
        spinner.next()
    except MemoryError as e:         # pragma: no cover
        logger.debug(sys.exc_info()[:2])
        logger.error('Недостаточно места на диске.')
        raise SomeException() from e
    logger.info('Files upload! The end')
    spinner.finish()
