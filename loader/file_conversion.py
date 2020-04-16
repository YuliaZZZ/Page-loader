from loader.created import create_name_file, page_load
from bs4 import BeautifulSoup
import os.path
import re


def change_html(html_file, catalog):
    items_src = []
    with open(html_file) as fp:
        soup = BeautifulSoup(fp, 'xml')
        for i in soup.find_all(
            ['script', 'img'],
            src=re.compile("^(?!https).+")) + soup.find_all(
                'link',
                href=re.compile("^(?!https).+")):
            if i.name == 'script' or i.name == 'img':
                items_src.append(i['src'])
                i['src'] = create_name_file(items_src[-1], catalog, head=1)
            elif i.name == 'link':
                items_src.append(i['href'])
                i['href'] = create_name_file(items_src[-1], catalog, head=1)
    text = str(soup)
    with open(html_file, 'w') as fp:
        fp.write(text)
    return items_src


def files_loader(items_src, catalog, site):
    if items_src != []:
        for i in items_src:
            page_load(
                site + os.path.normpath('/' + i),
                create_name_file(i, catalog, head=1))
    return items_src
