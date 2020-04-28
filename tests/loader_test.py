# -*- coding:utf-8 -*-
import logging
import os
import tempfile

import pytest

from loader import argparser, filesmaker, nameholder, process
from loader.scripts.page_loader import logger, SomeException


def readed(file):
    with open(file, 'r') as input_file:
        answer = input_file.read()
    return answer


def check_files_loader(url_list):
    for (_, i) in url_list:
        if not os.path.exists(i):
            return False
    return True


def check_process_module(site):
    with tempfile.TemporaryDirectory() as tmpdirname:
        process.app(site, tmpdirname)
        files_items = os.listdir(tmpdirname)
    return files_items


def test_argparser():
    assert argparser.transform(argparser.DEBUG) == logging.DEBUG
    assert argparser.transform(argparser.INFO) == logging.INFO
    assert argparser.transform(argparser.ERROR) == logging.ERROR
    assert argparser.transform(argparser.WARNING) == logging.WARNING
    assert argparser.transform(argparser.CRITICAL) == logging.CRITICAL


def test_nameholder():
    assert nameholder.make_filename('static/jquery.js', '.', headfile_ex=1) == './static-jquery.js'
    assert nameholder.make_filename('static/jquery', '.', headfile_ex=1) == './static-jquery.html'
    assert nameholder.make_filename('https://python-poetry.org', '.') == './python-poetry-org.html'
    assert nameholder.make_directname('./python-poetry-org.html') == './python-poetry-org_files'


def test_filesmaker():
    url = 'https://yuliazzz.github.io/site_for_testing/'
    text = filesmaker.download_page(url)
    assert readed('./tests/fixtures/example_site.html') == text
    with tempfile.TemporaryDirectory() as tmpdir:
        new_file = nameholder.make_filename(url, tmpdir)
        filesmaker.write_cont('TEXT', new_file)
        assert os.path.isfile(new_file) == True
        assert readed(new_file) == 'TEXT'
        t_direct = filesmaker.create_directory(tmpdir + '/yuliazzz-github-io-site_for_testing-_files')
        assert os.path.isdir(t_direct) == True
        url_list = [
            (url + os.path.normpath('/' + './chef&cooking.jpg'), t_direct + '/chef-cooking.jpg'),
            (url + os.path.normpath('/' +
                '/site_for_testing/assets/css/style.css?v=3a1cae6e260fc3026c0093222f0708050a6c11ca'),
             t_direct + '/site_for_testing-assets-css-style.css?v=3a1cae6e260fc3026c0093222f0708050a6c11ca'),
            (url + os.path.normpath('/' + './chocolate cake.html'), t_direct + '/chocolate-cake.html')]
        assert filesmaker.make_localsite(text, new_file, url, t_direct) == url_list
        assert readed(new_file) is not readed('./tests/fixtures/example_site.html')
        filesmaker.files_loader(url_list)
        assert check_files_loader(url_list) == True
        assert len(os.listdir(t_direct)) == len(url_list)
        assert check_process_module(url) == os.listdir(tmpdir)


def test_exceptions():
    with tempfile.TemporaryDirectory() as tmpdir:
        with pytest.raises(SomeException) as excinfo:
            filesmaker.create_directory('/python-poetry_files')
        with pytest.raises(SomeException) as excinfo:
            filesmaker.write_cont('ttt', './godzilla/pp.txt')
        with pytest.raises(SomeException) as excinfo:
            filesmaker.download_page('htts://python-poetry.org')
        with pytest.raises(SomeException) as excinfo:
            filesmaker.download_page('https:python-poetry.org')
        with pytest.raises(SomeException) as excinfo:
            filesmaker.download_page('https://pyon-poetry.org')
        with pytest.raises(SomeException) as excinfo:
            filesmaker.write_cont(filesmaker.download_page('https://httpbin.org/status/404'), './t_file')
