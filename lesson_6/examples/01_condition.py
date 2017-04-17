
import time
from random import randint
from collections import deque
from threading import Thread, Condition

from app_log import get_logger


logger = get_logger('condition','condition.log')
q = deque()

# Переменная состояния (condition variable) – это механизм синхронизации,
# надстроенный на уже имеющейся блокировке, который используется потоками,
# когда требуется дождаться наступления определенного состояния или появления события.
# Переменные состояния обычно используются в схемах поставщик-потребитель,
# когда один поток производит данные, а другой обрабатывает их.

flag = Condition()

# Решим схему "Производитель-Потребитель" через использование Condition

def producer():
    i = 0
    while True:
        flag.acquire()

        while len(q) < 100:
            logger.info('Мороженщик. Мороженого мало ({}). Произвожу!'.format(len(q)))
            q.append('Мороженое-{}'.format(i))
            i += 1

        # Метод  .notify() извещает ожидающие потоки, что значение переменной состояния изменилось.
        flag.notify()
        flag.release()
        logger.info('Сейчас в тележке: {}'.format(len(q)))


def consumer():
    while True:
        logger.info('Лакомка. Жду мороженое...')
        flag.acquire()

        while not q:    # Поток может разблокироваться,
                        # даже если не был вызван notify().
                        # Поэтому в пополнение к .wait() 
                        # делаем цикл проверки имеющихся ресурсов

            # Метод .wait() ожидает получения извещения или истечения времени ожидания
            flag.wait()

        logger.info('Лакомка. Дождался, теперь съем...')
        for i in range(randint(1, 100)):
            logger.info('Лакомка. Ням-ням...')
            good = q.popleft()

        flag.release()        
        time.sleep(2)


pt = Thread(target=producer, daemon=True)        
ct = Thread(target=consumer, daemon=True)        

print('Запускаем пищевую цепочку, а сами подождём...')
pt.start()
time.sleep(1)
ct.start()

time.sleep(5)
print('Время вышло!')
