import os.path
import re
import urllib


def make_filename(site, directory, headfile_ex=0):
    parts_url = urllib.parse.urlparse(site)
    if headfile_ex == 0:
        host = parts_url.netloc + parts_url.path
    else:
        host = re.split(r'^\W+', parts_url.path)[-1]
    hostname, postfix = os.path.splitext(host)
    if headfile_ex == 0 and postfix != 'html':
        hostname = host
        postfix = '.html'
    elif headfile_ex == 1 and postfix == '':
        postfix = '.html'
    name_parts = re.split(r'\W|\.', hostname)
    name_file = '{}/{}{}'.format(directory, '-'.join(name_parts), postfix)
    return name_file


def make_directoryname(html_file):
    name_directory = html_file.replace('.html', '_files')
    return name_directory
