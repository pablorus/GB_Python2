
# ----------------- Пример работы с очередью в процессах -----------------------

# Модуль multiprocessing поддерживает два основных способа взаимодействия процессов:
# каналы и очереди. Оба способа реализованы на основе механизма передачи сообщений.
# Интерфейс очередей очень близко имитирует интерфейс очередей в многопоточных программах.

import time
from random import choice, randint
from collections import Counter
import multiprocessing as mp

from app_log import get_logger


# Гном-производитель
def gnome(out_q, treasures):
    logger = get_logger('queue_proc', 'queue_proc.log')
    while True:
        # Гном-производитель откапывает случайное сокровище
        for i in range(randint(1,10)):
            data = choice(treasures)
            out_q.put(data)
        logger.info('Гном. Немного поработал, немного отдохну...')
        time.sleep(0.1)


# Потребитель гномьих трудов
def gnome_king(in_q):
    logger = get_logger('queue_proc', 'queue_proc.log')
    gnomes_cave = []
    while True:
        # Получаем данные из очереди
        data = in_q.get()
        if data is None:
            logger.info('Король. Упс, меня попросили выйти'.format(data))
            break
        logger.info('Король. Гном принёс мне {}'.format(data))
        # Кладём сокровища в... сберкассу
        gnomes_cave.append(data)
    return gnomes_cave
        


if __name__ == '__main__':    
    treasure = ('золото', 'серебро', 'алмазы', 'рубины')

    # Создаём очередь и запускаем оба процесса
    # Queue([maxsize])
    # Создает очередь для организации обмена сообщениями между процессами.
    # При вызове без аргумента размер очереди не ограничивается.
    # Внутренняя реализация очередей основана на использовании каналов и блокировок (Lock).
    q = mp.Queue()
    p1 = mp.Process(target=gnome_king, args=(q,), daemon=True)
    p2 = mp.Process(target=gnome, args=(q, treasure), daemon=True)

    print('Запускаем гномью работу')
    p1.start()
    p2.start()

    time.sleep(5)
    print('Проверим, сколько гномы накопили богатств...')

    p2.terminate()
    q.put(None)

    print(p1)
