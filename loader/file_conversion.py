from loader.created import create_name_file, page_load
from bs4 import BeautifulSoup
import os.path
import re


def change_html(html_file, catalog):
    items_src = {}
    with open(html_file) as fp:
        soup = BeautifulSoup(fp, 'xml')
        for i in soup.find_all(
            ['script', 'img'],
            src=re.compile("^(?!https).+")) + soup.find_all(
                'link',
                href=re.compile("^(?!https).+")):
            if i.name == 'script' or i.name == 'img':
                items_src[i['src']] = create_name_file(
                                                       i['src'],
                                                       catalog, head=1)
                i['src'] = items_src[i['src']]
            elif i.name == 'link':
                items_src[i['href']] = create_name_file(
                                                        i['href'],
                                                        catalog, head=1)
                i['href'] = items_src[i['href']]
    text = str(soup)
    with open(html_file, 'w') as fp:
        fp.write(text)
    return items_src


def files_loader(items_src, site):
    if len(items_src) > 0:
        for links, names_files in items_src.items():
            page_load(
                site + os.path.normpath('/' + links),
                names_files)
    return items_src
