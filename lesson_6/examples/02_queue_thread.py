
# ----------------- Пример работы с очередью в потоках ------------------------

# Модуль queue реализует различные типы очередей,
# поддерживающих возможность доступа из множества потоков
# и обеспечивающих сохранность информации при обмене данными между разными потоками

import time
from random import choice, randint
from collections import Counter
from threading import Thread
from queue import Queue 

from app_log import get_logger

logger = get_logger('queue', 'queue.log')
treasure = ('золото', 'серебро', 'алмазы', 'рубины')
gnomes_cave = []


# Гном-производитель
def gnome(out_q):
    while True:
        # Гном-производитель откапывает случайное сокровище
        for i in range(randint(1,10)):
            data = choice(treasure)

            # .put(item) добавляет элемент item в очередь
            out_q.put(data)

        logger.info('Гном. Немного поработал, немного отдохну...')
        time.sleep(0.1)


# Потребитель гномьих трудов
def gnome_king(in_q):
    while True:
        # Получаем данные из очереди
        # .get() удаляет и возвращает элемент из очереди
        data = in_q.get()
        
        logger.info('Король. Гном принёс мне {}'.format(data))

        # Кладём сокровища в... сберкассу
        gnomes_cave.append(data)

        # .task_done() используется потребителем, чтобы сообщить,
        # что элемент очереди был обработан
        in_q.task_done()

        

# Создаём очередь и запускаем оба потока

# Queue([maxsize])
# Создает очередь типа FIFO – первым пришел, первым вышел.
# Аргумент maxsize определяет максимальное количество элементов в очереди.
# При вызове без аргумента или maxsize=0 размер очереди не ограничивается.

q = Queue()

t1 = Thread(target=gnome_king, args=(q,), daemon=True)
t2 = Thread(target=gnome, args=(q,), daemon=True)

print('Запускаем гномью работу')
t1.start()
t2.start()


time.sleep(5)
print('Проверим, сколько гномы накопили богатств...')
print(Counter(gnomes_cave))
