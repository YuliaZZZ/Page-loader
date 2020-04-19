# -*- coding:utf-8 -*-
from loader import engine, created, file_conversion
import os
import logging
import pytest
import tempfile


links_dict = {'images/logo-origami.svg': 'python-poetry-org_files/images-logo-origami.svg',
              '/images/favicon-origami-32.png': 'python-poetry-org_files/images-favicon-origami-32.png',
              '/css/plugins/bootstrap/bootstrap.min.css': 'python-poetry-org_files/css-plugins-bootstrap-bootstrap-min.css',
              '/css/highlight.css': 'python-poetry-org_files/css-highlight.css',
              '/css/global.min.css': 'python-poetry-org_files/css-global-min.css',
              '/css/icons.min.css': 'python-poetry-org_files/css-icons-min.css',
              '/css/fonts.css': 'python-poetry-org_files/css-fonts.css',
              '/css/main.css': 'python-poetry-org_files/css-main.css'}


def check_load_files(site):
    fd = tempfile.TemporaryDirectory()
    dir_name = fd.name
    engine.app(site, dir_name)
    files = os.listdir(dir_name)
    return files


def test_modules():
    assert './static-jquery.js' == created.create_name_file('static/jquery.js', '.', head=1)
    assert './static-jquery.html' == created.create_name_file('static/jquery', '.', head=1)
    test_dir = tempfile.TemporaryDirectory()
    name_dir = test_dir.name
    site = 'https://python-poetry.org'
    new_file = created.page_load(site, created.create_name_file(site, name_dir))
    assert os.path.isfile(new_file) == True
    catalog = created.create_catalog(new_file)
    assert os.path.isdir(catalog) == True
    items_src = file_conversion.change_html(new_file, catalog)
    assert links_dict.keys() == items_src.keys()
    file_conversion.files_loader(items_src, site)
    assert os.listdir(name_dir) == check_load_files(site)


def test_exceptions():
    test_dir = tempfile.TemporaryDirectory()
    name_dir = test_dir.name
    with pytest.raises(engine.SomeException) as excinfo:
         engine.app('hps://python-poetry.org', name_dir)
    with pytest.raises(engine.SomeException) as excinfo:
         engine.app('https://pyton-poetry.org', name_dir)
    with pytest.raises(engine.SomeException):
         engine.app('https://python-poetry.org', '/')
    with pytest.raises(engine.SomeException) as excinfo:
         engine.app('https://python-poetry.org', name_dir + '/lag')
