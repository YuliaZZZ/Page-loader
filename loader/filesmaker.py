import os
import os.path
import re
import sys

import requests
from bs4 import BeautifulSoup
from progress.bar import ShadyBar

from loader.nameholder import make_filename
from loader.scripts.page_loader import SomeException, logger


def write_cont(content, file_):
    bar = ShadyBar('Loading', suffix='%(percent)d%%')
    if content:
        try:
            with open(file_, 'w') as fd:
                fd.write(content)
                bar.next()
            bar.finish()
        except FileNotFoundError as e:
            logger.debug(sys.exc_info()[:2])
            logger.error("Указанный каталог не существует.")
            raise SomeException() from e
        return file_
    raise SomeException()


def download_page(site):
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
        raise SomeException() from e
    if r.status_code in list(range(400, 501)):
        logger.error('Страница не отвечает.')
    content = r.text
    return content


def create_directory(name_directory):
    try:
        os.mkdir(name_directory, mode=0o700, dir_fd=None)
    except PermissionError as e:
        logger.debug(sys.exc_info()[:2])
        logger.error('Нет прав на внесение изменений.')
        raise SomeException() from e
    return str(name_directory)


def make_localsite(content, htmlfile_name, site, directory):
    items_src = []
    soup = BeautifulSoup(content, 'xml')
    file_name = None
    for i in soup.find_all(
          ['script', 'img'],
          src=re.compile("^(?!https).+")) + soup.find_all(
              'link',
              href=re.compile("^(?!https).+")):
        if i.name == 'link':
            file_name = make_filename(i['href'], directory, headfile_ex=1)
            items_src.append((site + os.path.normpath('/' + i['href']),
                              file_name))
            i['href'] = file_name
        else:
            file_name = make_filename(i['src'], directory, headfile_ex=1)
            items_src.append((site + os.path.normpath('/' + i['src']),
                              file_name))
            i['src'] = file_name
    text = str(soup)
    write_cont(text, htmlfile_name)
    return items_src


def files_loader(items_src):
    for (links, names_files) in items_src:
        try:
            write_cont(download_page(links), names_files)
        except requests.exceptions.Timeout:   # pragma: no cover
            logger.debug(sys.exc_info()[:2])
            logger.error('Истекло время ожидания ответа.')
            continue
