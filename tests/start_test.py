# -*- coding:utf-8 -*-
import pytest
from loader import engine, created, file_conversion
import tempfile
import os
import logging
import warnings


def check_load_files(site):
    fd = tempfile.TemporaryDirectory()
    dir_name = fd.name
    engine.app(site, dir_name)
    files = os.listdir(dir_name)
    return files


def test_answer():
    assert './static-jquery.js' == created.create_name_file('static/jquery.js', '.', head=1)
    assert './static-jquery.html' == created.create_name_file('static/jquery', '.', head=1)
    test_dir = tempfile.TemporaryDirectory()
    name_dir = test_dir.name
    new_file = created.page_load('https://python-poetry.org',
                                 created.create_name_file('https://python-poetry.org',
                                 name_dir))
    assert os.path.isfile(new_file) == True
    catalog = created.create_catalog(new_file)
    assert os.path.isdir(catalog) == True
    items = file_conversion.change_html(new_file, catalog, 'https://python-poetry.org')
    assert os.listdir(name_dir) == check_load_files('https://python-poetry.org')
