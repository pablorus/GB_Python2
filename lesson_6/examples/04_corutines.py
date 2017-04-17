
# ---------------- Сопрограммы (corutines/корутины) --------------------------

# * Примеры из книги: Дэвид Бизли. "Python. Подробный справочник"


# Внутри функций инструкция yield может использоваться
# справа от оператора присваивания. Например:
def receiver():
    print("Готов к приему значений")
    while True:
        n = yield
        print("Получено {}".format(n))


# Функция, которая так использует инструкцию yield, 
# называется сопрограммой и выполняется в ответ на попытку передать ей значение.
# Своим поведением такие функции очень похожи на генераторы. Например:
r = receiver()
# Для работы с сопрограммой необходимо выполнить инициализирующий вызов next
next(r)         # Выполнить до первой инструкции yield

# Но в сопрограмму можно передавать значения:
r.send(1)
r.send(2)
r.send("Привет")


# Создадим сопрограмму, которая разбивает передаваемую строку
# по заданному ранее разделителю
def line_splitter(delimiter=None):
    print("Все готово к разбиению строки")
    result = None
    while True:
        line = yield result
        result = line.split(delimiter)

# Сначала инициализируем генератор
s = line_splitter(",")
# Теперь "пройдёмся" до первого yield
next(s)
# Всё готово к разбиению строки
print(s.send("A,B,C"))
print(s.send("100,200,300"))


# ------------ Сопрограммы как альтернатива потокам --------------------------

# Рассмотрим две простых функции:

def countdown(n):
    while n > 0:
        print('Потихоньку теряем ресурсы... ', n)
        yield
        n -= 1
    print('Банкрот!')


def countup(n):
    x = 0
    while x < n:
        print('Прибыль растёт! ', x)
        yield
        x += 1


from collections import deque

# Теперь реализуем класс "Планировщик"
class TaskScheduler:
    def __init__(self):
        self._task_queue = deque()

    def new_task(self, task):
        '''
            Добавляем новое задание в планировщик
        '''
        self._task_queue.append(task)

    def run(self):
        '''
            Работаем, пока есть задачи
        '''
        while self._task_queue:
            task = self._task_queue.popleft()
            try:
                # "Прокручиваем"" задачу до yield
                next(task)
                self._task_queue.append(task)
            except StopIteration:
                # Когда генератор завершён, получим исключение
                pass

# Посмотрим планировщик заданий в работе:
sched = TaskScheduler()
sched.new_task(countdown(10))
sched.new_task(countdown(5))
sched.new_task(countup(15))
sched.run()