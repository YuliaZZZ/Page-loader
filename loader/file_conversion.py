from loader.created import create_name_file
from bs4 import BeautifulSoup
import re


def change_html(html_file, catalog):
    items_src = []
    with open(html_file) as fp:
        soup = BeautifulSoup(fp, 'xml')
        for i in (soup.find_all(['script', 'img'], src=re.compile("^[/|//]")) +
                  soup.find_all('link', href=re.compile("^/"))):
            if i.name == 'src':
                items_src.append(i['src'])
                i['src'] = create_name_file(items_src[-1], catalog, head=1)
            elif i.name == 'link':
                items_src.append(i['href'])
                i['href'] = create_name_file(items_src[-1], catalog, head=1)
    text = str(soup)   # pragma: no cover
    write_content(html_file, text)    # pragma: no cover
    return items_src


def write_content(file_, content):
    with open(file_, 'w') as fp:
        fp.write(content)
    return file_
