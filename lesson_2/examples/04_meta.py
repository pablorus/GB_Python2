
# ---------- Метаклассы ----------------------------
# Классы в Python - это тоже объекты. Созданием классов заведуют метаклассы.
# В обычном случае созданием классов занимается  type

# Используя функцию type можно вот так создать новый класс:
Spam = type("Spam", (A,), {"name":'Python', "age":25})


# ---------- Шаблон Одиночка (Singleton) -----------
# Используя возможности метаклассов можно интересно решить задачу
# по созданию шаблона Одиночка.

# Объявляем метакласс, который будет контролировать создание нового класса
class Singleton(type):

    def __init__(self, *args, **kwargs):
        self.__instance = None
        super().__init__(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        if self.__instance is None:
            self.__instance = super().__call__(*args, **kwargs)
            return self.__instance
        else:
            return self.__instance


class Space(metaclass=Singleton):
    def __init__(self):
        print('Я-одиночка Космос')


class Earth(metaclass=Singleton):
    def __init__(self):
        print('Я-одиночка Земля')


class Water(metaclass=Singleton):
    def __init__(self):
        print('Я-одиночка Вода')


x = Space()
xx = Space()
y = Earth()
z = Water()
yy = Earth()
zz = Water()
print(x is xx, x is y, x is z, y is yy, z is zz)