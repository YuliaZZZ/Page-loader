# -*- coding:utf-8 -*-
import pytest
from loader import engine
import tempfile
import filecmp


def readed(file):
    with open(file, 'r') as input_file:
        answer = input_file.read()
    return answer


def compare(site):
    fd = tempfile.TemporaryDirectory()
    dir_name = fd.name
    file1 = engine.page_load(site, dir_name)
    with open(file1, 'r') as h:
        content = h.read()
    return content


def test_answer():
    assert 'hexlet-io-courses.html' == engine.create_name_file('https://hexlet.io/courses')
    assert  readed('tests/fixtures/docs-python-org-3-.html') == compare(
        'https://docs.python.org/3/')
