# Copyrights rostepifanov.ru
#   Author: Rostislav Epifanov
#   Created: 27/07/2020

import pytest

@pytest.fixture(scope='function', autouse = True)
def function_setup():
    print('function scope')

@pytest.fixture(scope='module')
def module_setup():
    print('module scope')

def test_one(function_setup, module_setup):
    assert False

def test_two():
    assert False