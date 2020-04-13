from loader.scripts.page_loader import logger, SomeException
import re
import requests
import os
import os.path


def create_name_file(site, way, head=0):
    tail = re.split(r'://|^\W+', site)
    start, postfix = os.path.splitext(tail[-1])
    if head == 0 and postfix != 'html':
        start = tail[-1]
        postfix = '.html'
    elif head == 1 and postfix == '':
        postfix = '.html'
    other_symbols = re.split(r'\W|\.', start)
    name_file = ''.join([way, '/', '-'.join(other_symbols), postfix])
    return name_file


def page_load(site, name_file):
    try:
        r = requests.get(site)
    except requests.exceptions.InvalidSchema as e:
        logger.error('Ошибка параметров запроса.')
        raise SomeException() from e
    except requests.exceptions.ConnectionError as e:
        logger.error(
                    'Неверный адрес сайта либо ошибка подключения.'
                    )
        raise SomeException() from e
    except requests.exceptions.Timeout as e:
        logger.error('Истекло время ожидания ответа.')
        raise SomeException() from e
    r.encoding
    try:
        with open(name_file, 'wb') as fd:
            for chunk in r.iter_content(chunk_size=45):
                fd.write(chunk)
    except FileNotFoundError as e:
        logger.error("Указанный каталог не существует")
        raise SomeException() from e
    return name_file


def create_catalog(head_file):
    catalog_name = head_file.replace('.html', '_files')
    try:
        os.mkdir(catalog_name, mode=0o777, dir_fd=None)
    except PermissionError as e:
        logger.error('Нет прав на внесение изменений')
        raise SomeException() from e
    return str(catalog_name)
