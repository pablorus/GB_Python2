# coding: utf-8

# ------- GIL  (Global interpreter lock) -------------------------------

import time
from threading import Thread


# Посмотрите на простую функцию:
def count(n):
    ''' Данная функция зависит от CPU-вычисления
    '''
    while n > 0:
        n -= 1


# Произведём замеры времени.

# Последовательное выполнение:
start = time.time()

count(100000000)
count(100000000)

print('Последовательное выполнение: {} сек.'.format(time.time()-start))


# Выполнение в 2-х потоках:
start = time.time()

t1 = Thread(target=count, args=(100000000,))
t1.start()

t2 = Thread(target=count, args=(100000000,))
t2.start()

while t1.isAlive() or t2.isAlive():
    pass

print('Выполнение в 2 потока: {} сек.'.format(time.time()-start))

print('В-Ж-У-Х-?')
print('В этом весь GIL...')
