

# with open('test', 'w') as f:
#     f.write('Stroka')

# Менеджеры контекста
    
class ListTransaction:
    def __init__(self, thelist):
        self.thelist = thelist

    def __enter__(self):
        self.workingcopy = list(self.thelist)
        return self.workingcopy

    def __exit__(self, exc_type, value, traceback):
        print(exc_type, value, traceback)
        if exc_type is None:
            self.thelist[:] = self.workingcopy
            # self.thelist[:] = 'Python'
        return False


items = [1, 2, 3]

with ListTransaction(items) as tr:
    tr.append(4)
    tr.append(5)
    # tr = 'strokka'

print(items) 


try:
    with ListTransaction(items) as working:
        working.append(6)
        working.append(7)
        raise ValueError("Фига вам, а не транзакция!")

except ValueError:
    print("Кто-то потрогал наши транзакции! Грязные хоббитсы")
    

print(items) 


# Небольшое упрощение...

from contextlib import contextmanager


@contextmanager
def ListTransaction(thelist):
    workingcopy = list(thelist)
    yield workingcopy
    print('No exception')
    # Изменить оригинальный список, только если не возникло ошибок
    thelist[:] = workingcopy



items = ['Фродо', 'Сэм', 'Горлум']
try:
    with ListTransaction(items) as working:
        # working = 'l-i-s-t-'
        working.append('Кольцо')
        working.append('Мордор')
        raise(ValueError('oop'))

except ValueError:
    print("Кто-то!")

print(items) 





