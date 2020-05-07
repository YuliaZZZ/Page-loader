# -*- coding:utf-8 -*-
import logging
import os
import requests
import tempfile
import urllib.parse

import pytest

from loader import files_creator, names_creator, process
from loader.log import SomeException, setup_log


def readed(file):
    with open(file, 'r') as input_file:
        answer = input_file.read()
    return answer


def downloads_files_check(url_list):
    for (_, i) in url_list:
        if not os.path.exists(i):
            return False
    return True


def check_process_module(site, log):
    with tempfile.TemporaryDirectory() as tmpdirname:
        process.make_loader(site, tmpdirname, log)
        files_items = os.listdir(tmpdirname)
    return files_items


def test_nameholder():
    assert names_creator.make_filename('static/jquery.js', '.', headfile_ex=1) == './static-jquery.js'
    assert names_creator.make_filename('static/jquery', '.', headfile_ex=1) == './static-jquery.html'
    assert names_creator.make_filename('https://python-poetry.org', '.') == './python-poetry-org.html'
    assert names_creator.make_directoryname('./python-poetry-org.html') == './python-poetry-org_files'


CONTENT = 'TEXT'
URL = 'https://yuliazzz.github.io/python-project-lvl3/'
logger = setup_log(logging.DEBUG)
DIRECTORY_NAME = '/yuliazzz-github-io-python-project-lvl3-_files'
CONTENT1 = "./chef.cooking.jpg"
CONTENT2 = './chocolate cake.html'
EXAMPLE_SITE = './tests/fixtures/example_site.html'


def test_filesmaker():
    text = files_creator.download_page(URL, logger)
    assert readed(EXAMPLE_SITE) == text
    with tempfile.TemporaryDirectory() as tmpdir:
        new_file = names_creator.make_filename(URL, tmpdir)
        assert readed(EXAMPLE_SITE) == text
        t_direct = process.create_directory(tmpdir + DIRECTORY_NAME, logger)
        assert os.path.isdir(t_direct) is True
        url_list = [
            (urllib.parse.urljoin(URL, CONTENT1), t_direct + '/chef-cooking.jpg'),
            (urllib.parse.urljoin(URL, CONTENT2), t_direct + '/chocolate-cake.html')]
        new_text, url_src = files_creator.make_local_site(text, new_file, URL, t_direct)
        assert url_src == url_list
        files_creator.write_in_file(new_text, new_file, logger)
        assert os.path.isfile(new_file) is True
        assert readed(new_file) is not readed(EXAMPLE_SITE)
        for (l, f) in url_src:
            files_creator.write_in_file(files_creator.download_page(l, logger, main_page=1), f, logger)
        assert downloads_files_check(url_list) is True
        assert len(os.listdir(t_direct)) == len(url_list)
        assert check_process_module(URL, logger) == os.listdir(tmpdir)


def test_exceptions():
    with tempfile.TemporaryDirectory() as tmpdir:
        with pytest.raises(SomeException):
            process.create_directory('/tes', logger)                          # Testing PermissionError
        with pytest.raises(SomeException):
            files_creator.write_in_file(CONTENT, './godzilla/pp.txt', logger)  # Testing FileNotFoundError
        with pytest.raises(SomeException):
            files_creator.download_page('htts://python-poetry.org', logger)    # Testing
                                                                               # requests.exceptions.InvalidSchema
        with pytest.raises(SomeException):
            files_creator.download_page('https:python-poetry.org', logger)     # Testing
                                                                               # requests.exceptions.MissingSchema
        with pytest.raises(SomeException):
            files_creator.download_page('https://pyon-poetry.org', logger)     # Testing
                                                                               # requests.exceptions.ConnectionError
        with pytest.raises(SomeException):
            files_creator.download_page('https://httpbin.org/status/404', logger)  # Testing invalid response
        with pytest.raises(SomeException):
            files_creator.download_page('https://httpbin.org/status/503', logger)
