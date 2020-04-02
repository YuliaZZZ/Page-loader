# -*- coding:utf-8 -*-
import pytest
from loader import engine, created
import tempfile
import os


def readed(file):
    with open(file, 'r') as input_file:
        answer = input_file.read()
    return answer


def create_check_html(site):
    fd = tempfile.TemporaryDirectory()
    dir_name = fd.name
    file1 = created.page_load(site, created.create_name_file(site, dir_name))
    with open(file1, 'r') as h:
        content = h.read()
    return content


def check_create_catalog(site):
    fd = tempfile.TemporaryDirectory()
    dir_name = fd.name
    file1 = created.page_load(site, created.create_name_file(site, dir_name))
    c = created.create_catalog(file1)
    return c


def test_answer():
    file = created.page_load('https://docs.python.org/3/', './docs-python-org-3-.html')
    assert './hexlet-io-courses.html' == created.create_name_file('https://hexlet.io/courses', '.')
    assert './_static-jquery.js' == created.create_name_file('./_static/jquery.js', '.', head=1)
    assert readed(file) == create_check_html('https://docs.python.org/3/')
    os.remove(file)
