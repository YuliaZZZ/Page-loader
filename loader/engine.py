import re
import requests


def create_name_file(site):
    _, tail = site.split('://')
    other_symbols = re.split('[\W|^.]', tail)  # noqa W605
    name_file = '-'.join(other_symbols)
    name_file += '.html'
    return name_file


def page_load(site, way):
    r = requests.get(site)
    r.encoding
    new_file = way + '/' + create_name_file(site)
    with open(new_file, 'wb') as fd:
        for chunk in r.iter_content(chunk_size=45):
            fd.write(chunk)
    return new_file
