# -*- coding:utf-8 -*-
import pytest
from loader import engine
import tempfile
import os


def readed(file):
    with open(file, 'r') as input_file:
        answer = input_file.read()
    return answer


def create_check_file(site):
    fd = tempfile.TemporaryDirectory()
    dir_name = fd.name
    file1 = engine.page_load(site, dir_name)
    with open(file1, 'r') as h:
        content = h.read()
    return content


def test_answer():
    file = engine.page_load('https://docs.python.org/3/', './tests/fixtures')
    assert 'hexlet-io-courses.html' == engine.create_name_file('https://hexlet.io/courses')
    assert readed(file) == create_check_file('https://docs.python.org/3/')
    os.unlink(file)
