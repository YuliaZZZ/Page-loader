import re


def create_name_file(site):
    _, tail = site.split('://')
    other_symbols = re.split('[\W|^.]', tail)  # noqa W605
    name_file = '-'.join(other_symbols)
    name_file += '.html'
    return name_file
