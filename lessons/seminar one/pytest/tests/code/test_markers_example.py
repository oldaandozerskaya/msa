# Copyrights rostepifanov.ru
#   Author: Rostislav Epifanov
#   Created: 27/07/2020

import os
import pytest

def are_you_wanna_play_with_me():
    return os.getenv('ANSWER', True)

@pytest.mark.callmeboy
def test_guilty_pleasure():
    print('Oops you call guilty please test')
    assert False

@pytest.mark.questionable
@pytest.mark.skipif(are_you_wanna_play_with_me(), reason='Nobody want play with me')
def test_complicated():
    print('Yeaahh catch some tricks')
    assert False