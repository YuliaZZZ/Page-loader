import os.path
import re


def make_filename(site, directory, headfile_ex=0):
    host = re.split(r'://|^\W+', site)
    hostname, postfix = os.path.splitext(host[-1])
    if headfile_ex == 0 and postfix != 'html':
        hostname = host[-1]
        postfix = '.html'
    elif headfile_ex == 1 and postfix == '':
        postfix = '.html'
    name_parts = re.split(r'\W|\.', hostname)
    name_file = '{}/{}{}'.format(directory, '-'.join(name_parts), postfix)
    return name_file


def make_directname(html_file):
    name_directory = html_file.replace('.html', '_files')
    return name_directory
