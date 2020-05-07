import re
import sys
import urllib.parse

import requests
from bs4 import BeautifulSoup

from loader.names_creator import make_filename
from loader.log import SomeException


LOCAL_PAGE = re.compile("^(?!https).+")


def write_in_file(content, file_, logger):
    try:
        with open(file_, 'w') as fd:
            fd.write(content)
    except FileNotFoundError as e:
        logger.debug(sys.exc_info()[:2])
        logger.error("Указанный каталог не существует.")
        raise SomeException() from e
    return file_


def download_page(site, logger, main_page=0):
    try:
        r = requests.get(site)
    except (requests.exceptions.InvalidSchema,
            requests.exceptions.InvalidURL,
            requests.exceptions.MissingSchema) as e:
        logger.debug(sys.exc_info()[:2])
        logger.error('Ошибка параметров запроса.')
        raise SomeException() from e
    except requests.exceptions.ConnectionError as e:
        logger.debug(sys.exc_info()[:2])
        logger.error(
            'Несуществующий адрес сайта либо ошибка подключения.')
        if main_page == 0:
            raise SomeException() from e
    if r.status_code in range(400, 500):
        logger.debug('Страница не существует.')
        if main_page == 0:
            logger.error('Страница не существует.')
            raise SomeException()
    elif r.status_code in range(500, 511):
        logger.debug('Сервер не отвечает.')
        if main_page == 0:
            logger.error('Сервер не отвечает.')
            raise SomeException()
    content = r.text
    return content


def give_link(tag):
    return tag['href'] if 'href' in tag.attrs else tag['src']


def make_local_site(content, htmlfile_name, site, directory):
    items_src = []
    soup = BeautifulSoup(content, 'xml')
    file_name = None
    for i in soup.find_all(['script', 'img'],
                           src=LOCAL_PAGE) + soup.find_all(
                               'link', href=LOCAL_PAGE):
        file_name = make_filename(give_link(i), directory, headfile_ex=1)
        items_src.append((urllib.parse.urljoin(site, give_link(i)),
                          file_name))
        if 'href' in i.attrs:
            i['href'] = file_name
        else:
            i['src'] = file_name
    text = str(soup)
    return text, items_src
