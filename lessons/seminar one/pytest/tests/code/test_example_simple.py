# Copyrights rostepifanov.ru
#   Author: Rostislav Epifanov
#   Created: 27/07/2020

import pytest

from code.example_simple import *

def test_incrementer():
    assert incrementer(3) == 5

def test_errorers():
    with pytest.raises(SystemExit):
        errorers()