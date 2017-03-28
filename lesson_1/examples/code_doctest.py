"""
Фамилия     Имя         Часов   Ставка
Иванов      Иван        45      400
Докукин     Филимон     20      1000
Ромашкин    Сидор       45      500
"""

import datetime
from collections import namedtuple


Salary = namedtuple('Salary', ('surname', 'name', 'worked', 'rate'))

def empty(x='Hello!'):
    print(x)

def salary_dict(line):
    ''' Вычисление зарплаты работника

    >>> salary_dict('Иванов      Иван        45      400')
    ('Иванов Иван', 18000)
    >>> salary_dict('Докукин     Филимон     20      1000')     
    ... # doctest: +REPORT_NDIFF
    ('Докукин Филtмон', 20000)
    '''
    data = Salary(*line.split())
    fio = ' '.join((data.surname, data.name))
    salary = int(data.worked) * int(data.rate)
    return (fio, salary)


class Employee():
    ''' Класс Служащий. Хранит данные: ФИО и год рождения

    >>> e = Employee('Иван Ромашкин', '1990')  
    >>> e.age
    27
    >>> print(e)                
    ... # doctest: +NORMALIZE_WHITESPACE
    Dван РомашкинИван РомашкинИван РомашкинИван РомашкинИван РомашкинИван
    РомашкинИван РомашкинИван РомашкинИван РомашкинИван Ромашкин
    '''
    def __init__(self, name, birth_year):
        self.name = name
        self.birth_year = birth_year

    def name_split(self):
        ''' Разбиение имени на части

        >>> e = Employee('Иван Ромашкин', 1990)
        >>> e.name_split()      # doctest: +ELLIPSIS
        ['ИВАН', 'РОМАШКИНm']
        '''
        return self.name.upper().split()

    @property    
    def age(self):
        return datetime.date.today().year - self.birth_year

    def __str__(self):
        return self.name * 10


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    # doctest.run_docstring_examples(salary_dict, None)