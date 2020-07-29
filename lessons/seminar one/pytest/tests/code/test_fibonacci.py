# Copyrights rostepifanov.ru
#   Author: Rostislav Epifanov
#   Created: 27/07/2020

import pytest

from code.fibonacci import *

class TestFibonacci(object):
    def test_get_CASE_negative_number(self):
        with pytest.raises(FibonacciError):
            Fibonacci.get(-1)

    def test_get_CASE_zero_number(self):
        assert Fibonacci.get(0) == 0

    def test_get_CASE_one_number(self):
        assert Fibonacci.get(1) == 1
