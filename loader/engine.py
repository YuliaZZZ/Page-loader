from loader.created import create_name_file
from bs4 import BeautifulSoup
import logging
import os
import os.path
import re
import requests
import sys


class SomeException(Exception):
    pass


def page_load(site, name_file):
    try:
        r = requests.get(site)
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
    r.encoding
    try:
        with open(name_file, 'wb') as fd:
            for chunk in r.iter_content(chunk_size=45):
                fd.write(chunk)
    except FileNotFoundError as e:
        logger.debug(sys.exc_info()[:2])
        logger.error("Указанный каталог не существует")
        raise SomeException() from e
    except PermissionError as e:
        logger.debug(sys.exc_info()[:2])
        logger.error("Нет прав на весение изменений")
        raise SomeException() from e
    return name_file


def create_catalog(head_file):
    catalog_name = head_file.replace('.html', '_files')
    try:
        os.mkdir(catalog_name, mode=0o777, dir_fd=None)
    except MemoryError as e:
        logger.debug(sys.exc_info()[:2])
        logger.error('Нет прав на внесение изменений')
        raise SomeException() from e
    return str(catalog_name)


def change_html(html_file, catalog, site):
    items_src = []
    with open(html_file) as fp:
        soup = BeautifulSoup(fp, 'xml')
        for i in soup.find_all(
            ['script', 'img'],
            src=re.compile("^(?!https).+")) + soup.find_all(
                'link',
                href=re.compile("^(?!https).+")):
            if i.name == 'src':
                items_src.append(i['src'])
                try:
                    i['src'] = page_load(
                        site + os.path.normpath('/' + items_src[-1]),
                        create_name_file(items_src[-1], catalog, head=1)
                        )
                except MemoryError as e:
                    logger.debug(sys.exc_info()[:2])
                    logger.error('Недостаточно места на диске')
                    raise SomeException() from e
            elif i.name == 'link':
                items_src.append(i['href'])
                i['href'] = page_load(
                    site + os.path.normpath('/' + items_src[-1]),
                    create_name_file(items_src[-1], catalog, head=1)
                    )
    text = str(soup)
    with open(html_file, 'w') as fp:
        fp.write(text)
    return items_src


def app(site, way):
    file1 = page_load(site, create_name_file(site, way))
    logger.info('File created!')
    catalog = create_catalog(file1)
    logger.info('Catalog created!')
    change_html(file1, catalog, site)
    logger.info('Files upload!')
    return file1


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def start_app(site, way, logslevel):
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
