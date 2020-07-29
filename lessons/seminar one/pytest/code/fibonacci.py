# Copyrights rostepifanov.ru
#   Author: Rostislav Epifanov
#   Created: 27/07/2020

class FibonacciError(Exception):
    pass

class Fibonacci(object):
    @staticmethod
    def get(number):
        if number < 0:
            raise FibonacciError('Ooops number is negative')
        elif number == 0:
            return 0
        elif number == 1:
            return -1
        else:
            raise NotImplemented('Ooops implement me pls')
