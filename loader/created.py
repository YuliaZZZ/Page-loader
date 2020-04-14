import re
import os.path


def create_name_file(site, way, head=0):
    tail = re.split(r'://|^\W+', site)
    start, postfix = os.path.splitext(tail[-1])
    if head == 0 and postfix != 'html':
        start = tail[-1]
        postfix = '.html'
    elif head == 1 and postfix == '':
        postfix = '.html'
    other_symbols = re.split(r'\W|\.', start)
    name_file = ''.join([way, '/', '-'.join(other_symbols), postfix])
    return name_file
