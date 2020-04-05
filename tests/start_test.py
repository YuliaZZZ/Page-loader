# -*- coding:utf-8 -*-
import pytest
from loader import engine, created, file_conversion
import tempfile
import os


def readed(file):
    with open(file, 'r') as input_file:
        answer = input_file.read()
    return answer


def check_create_html(site):
    fd = tempfile.TemporaryDirectory()
    dir_name = fd.name
    file1 = created.page_load(site, created.create_name_file(site, dir_name))
    return readed(file1)


def check_src(site):
    fd = tempfile.TemporaryDirectory()
    dir_name = fd.name
    file1 = created.page_load(site, created.create_name_file(site, dir_name))
    c = created.create_catalog(file1)
    result = file_conversion.change_html(file1, dir_name, site)
    return result


def check_load_files(site):
    fd = tempfile.TemporaryDirectory()
    dir_name = fd.name
    engine.app(site, dir_name)
    files = os.listdir(dir_name)
    return files


def test_answer():
    assert './_static-jquery.js' == created.create_name_file('./_static/jquery.js', '.', head=1)
    test_dir = tempfile.TemporaryDirectory()
    name_dir = test_dir.name
    new_file = created.page_load('https://learngitbranching.js.org/?locale=ru_RU',
                                 created.create_name_file('https://learngitbranching.js.org/?locale=ru_RU',
                                 name_dir))
    assert check_create_html('https://learngitbranching.js.org/?locale=ru_RU') == readed(new_file)
    catalog = created.create_catalog(new_file)
    assert os.path.isdir(catalog) == True
    items_src = file_conversion.change_html(new_file, catalog, 'https://learngitbranching.js.org/?locale=ru_RU')
    assert check_src('https://learngitbranching.js.org/?locale=ru_RU') == items_src
    assert os.listdir(name_dir) == check_load_files('https://learngitbranching.js.org/?locale=ru_RU')
