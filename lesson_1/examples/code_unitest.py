"""
Фамилия     Имя         Часов   Ставка
Иванов      Иван        45      400
Докукин     Филимон     20      1000
Ромашкин    Сидор       45      500
"""

import datetime
from collections import namedtuple

import unittest

Salary = namedtuple('Salary', ('surname', 'name', 'worked', 'rate'))

def get_salary(line):
    ''' Вычисление зарплаты работника
    '''
    line = line.split()
    if line:    
        data = Salary(*line)
        fio = ' '.join((data.surname, data.name))
        salary = int(data.worked) * int(data.rate)
        res = (fio, salary)
    else:
        res = ()    
    return res


class TestSalary(unittest.TestCase):

    def test_get_salary_summ(self):
        self.assertEqual(get_salary('Лютиков   Руслан     60    1000'),
                         ('Лютиков Руслан', 60000))

    def test_get_salary_fio(self):
        self.assertEqual(get_salary('Лютиков   Руслан     60    1000')[0],
                         'Лютиков Руслан')

    def test_get_salary_empty(self):
        self.assertEqual(get_salary(''), ('1', '2'))


if __name__ == "__main__":
    unittest.main()