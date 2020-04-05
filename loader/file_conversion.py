from loader.created import create_name_file, page_load
from bs4 import BeautifulSoup
import re


def change_html(html_file, catalog, site):
    items_src = []
    with open(html_file) as fp:
        soup = BeautifulSoup(fp, 'xml')
        for i in soup.find_all(['script', 'img'],
            src=re.compile("^/|^\./|^\.//|^\.\./")):   # noqa  W605
            items_src.append(i['src'])
            i['src'] = page_load(
                     site + items_src[-1],
                     create_name_file(items_src[-1], catalog, head=1)
                     )
        for j in soup.find_all('link',
            href=re.compile("^/|^\./|^\.//|^\.\./")):   # noqa  W605
            items_src.append(j['href'])
            j['href'] = page_load(
                      site + items_src[-1],
                      create_name_file(items_src[-1], catalog, head=1)
                      )
    text = str(soup)
    with open(html_file, 'w') as fp:
        fp.write(text)
    return items_src
