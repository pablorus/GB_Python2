
# ------------------- Взаимодействие потоков. Мьютексы (Locks) -------------------

import time
from threading import Thread, Lock

import logging


# Воспользуемся модулем logging для удобства отслеживания работы с мьютексом и без него
# Этот модуль является потоко-безопасным, поэтому при работе с потоками
# лучше использовать его для фиксирования событий
logger = logging.getLogger('db_admin_gui')
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s ")
fh = logging.FileHandler("lock.log", encoding='utf-8')
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)
logger.addHandler(fh)
logger.setLevel(logging.DEBUG)

# Создадим отдельный флаг, чтобы гарантировать одновременный запуск потоков
START = False

gold_resource = ['золото', 'серебро', 'бриллианты', 'платина', 'изумруды',
                'аматисты', 'алмазы', 'консервная банка', ]


# Создадим класс, который будет в потоке работать с неким ресурсом
class GnomeMiner:

    # Создадим мьютекс, являющийся атрибутом класса
    lock = Lock()

    def __init__(self, name):
        self.name = name

    def start(self):
        t = Thread(target=self.run)
        t.daemon = True
        t.start()

    def run(self):
        logger.info('{} ждёт команду на старт...'.format(self.name))
        while not START:
            # ждём общий старт
            pass

        while gold_resource:
            # Некая полезная работа, пока есть ресурсы

            # Код, который заключен между вызовами acquire-release является критической секцией
            logger.info('{} ждёт ресурсы...'.format(self.name))
            GnomeMiner.lock.acquire()       # <-- Попробуйте закомментировать строки acquire, release
                                            # и посмотрите на результат в лог-файле

            # После того, как кто-то захватил мьютекс, никто другой не может его 
            # захватить и будет ожидать освобождения мьютекса.
            # Проверьте по лог-файлу, что будет, если работать без мьютекса...
            res = gold_resource[-1]
            logger.info('Гном {} меняет {}'.format(self.name, res))
            gold_resource[-1] = res + '***'
            res = gold_resource.pop()
            logger.info('Гном {} забрал {}'.format(self.name, res))

            GnomeMiner.lock.release()
            logger.info('{} освободил ресурсы и немного отдыхает...'.format(self.name))
            # time.sleep(1)


gnome_1 = GnomeMiner('1-Tratun')        
gnome_2 = GnomeMiner('2-Gudoon')    
gnome_3 = GnomeMiner('3-Zorkos')    
gnome_4 = GnomeMiner('4-Kikolka')    

gnome_1.start()
gnome_2.start()   
gnome_3.start()   
gnome_4.start()  


print('Небольшой таймаут перед запуском гномов...')
logger.info('Небольшой таймаут перед запуском гномов...')
time.sleep(1)
print('Запуск гномов!')
START = True

while gold_resource:
    time.sleep(2)
    logger.info('Гномы работают...')

logger.info('Работа окончена!')
logger.info('-'*80)
print('Ресурсы исчерпаны. Рабочий день закончен!')
