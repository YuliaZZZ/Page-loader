import re
import requests
import os
import os.path


def create_name_file(site, way, head=0):
    tail = re.split('^\W*|://', site)   # noqa  W605
    start, postfix = os.path.splitext(tail[-1])
    if head == 0 and postfix != 'html':
        start = tail[-1]
        postfix = '.html'
    elif head == 1 and postfix == '':
        postfix = '.html'
    other_symbols = re.split('\W|\.', start)   # noqa  W605
    name_file = ''.join([way, '/', '-'.join(other_symbols), postfix])
    return name_file


def page_load(site, name_file):
    r = requests.get(site)
    r.encoding
    with open(name_file, 'wb') as fd:
        for chunk in r.iter_content(chunk_size=45):
            fd.write(chunk)
    return name_file


def create_catalog(head_file):
    catalog_name = head_file.replace('.html', '_files')
    os.mkdir(catalog_name, mode=0o777, dir_fd=None)
    return str(catalog_name)
