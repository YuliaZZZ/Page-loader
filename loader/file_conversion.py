from loader.created import create_name_file, page_load
from loader.scripts.page_loader import logger, SomeException
from bs4 import BeautifulSoup
import re
import os.path


def change_html(html_file, catalog, site):
    items_src = []
    with open(html_file) as fp:
        soup = BeautifulSoup(fp, 'xml')
        for i in soup.find_all(['script', 'img'],
            src=re.compile("^(?!https).*")):   # noqa  W605
            items_src.append(i['src'])
            try:
                i['src'] = page_load(
                     site + os.path.normpath('/' + items_src[-1]),
                     create_name_file(items_src[-1], catalog, head=1)
                     )
            except MemoryError as e:
                logger.error('Недостаточно места в памяти')
                raise SomeException() from e
        for j in soup.find_all('link',
            href=re.compile("^(?!https).*")):   # noqa  W605
            items_src.append(j['href'])
            j['href'] = page_load(
                      site + os.path.normpath('/' + items_src[-1]),
                      create_name_file(items_src[-1], catalog, head=1)
                      )
    text = str(soup)
    with open(html_file, 'w') as fp:
        fp.write(text)
    return items_src
