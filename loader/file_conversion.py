from loader.created import create_name_file
from bs4 import BeautifulSoup
import re


def change_html(html_file, catalog):
    items_src = []
    with open(html_file) as fp:
        soup = BeautifulSoup(fp, 'xml')
        for i in soup.find_all(['script', 'img'], src=re.compile("^[/|//]")):
            items_src.append(i['src'])
            i['src'] = create_name_file(items_src[-1], catalog, head=1)
        for j in soup.find_all('link', href=re.compile("^/")):
            items_src.append(j['href'])
            j['href'] = create_name_file(items_src[-1], catalog, head=1)
        text = str(soup)
    with open(html_file, 'w') as fp:
        fp.write(text)
    return items_src
