# coding: utf-8

# ------- GIL  (Global interpreter lock) -------------------------------

import time
from threading import Thread
import multiprocessing as mp


print('Hello, Process!')

# Посмотрите на простую функцию:
def count(n):
    ''' Данная функция зависит от CPU-вычисления
    '''
    while n > 0:
        n -= 1




if __name__ == '__main__':

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

    while t1.is_alive() or t2.is_alive():
        pass

    print('Выполнение в 2 потока: {} сек.'.format(time.time()-start))

    print('В-Ж-У-Х-?')
    print('В этом весь GIL...')    

    start = time.time()    
    
    p1 = mp.Process(target=count, args=(100000000, ))
    p2 = mp.Process(target=count, args=(100000000, ))
    p1.start()
    p2.start()

    while p1.is_alive() or p2.is_alive():
        pass

    print('Выполнение в 2 процесса: {} сек.'.format(time.time()-start))    
