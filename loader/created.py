import re
import requests
import pathlib
import os
import os.path


def create_name_file(site, way, head=0):
    _, tail = re.split('://|^/|^./|^.//', site)
    n = pathlib.PurePath(tail)
    if head == 0 and n.suffix != 'html':
        postfix = '.html'
    elif head == 1:
        postfix = str(n.suffix)
        tail = tail[: -len(n.suffix)]
    other_symbols = re.split('\W|\.', tail)
    name_file = way + '/' + '-'.join(other_symbols) + postfix
    return name_file


def page_load(site, name_file):
    r = requests.get(site)
    r.encoding
    with open(name_file, 'wb') as fd:
        for chunk in r.iter_content(chunk_size=45):
            fd.write(chunk)
    return name_file


def create_catalog(head_file):
    p = pathlib.PurePath(head_file)
    catalog_name = p.with_name(p.stem + '_files')
    os.mkdir(catalog_name, mode=0o777, dir_fd=None)
    catalog = pathlib.PurePath(catalog_name)
    return str(catalog)


def load_files(items_src, catalog, site):
    items_files = []
    for i in items_src:
        items_files.append(page_load(site+i,
                           create_name_file(i, catalog, head=1)))
    return items_files
