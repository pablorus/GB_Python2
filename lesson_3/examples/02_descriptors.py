

# Дескрипторы


class TypedProperty:
    def __init__(self, name, type_, default=None):
        self.name = "_" + name
        self.type = type_
        self.default = default if default else type_()

    def __get__(self, instance, cls):
        print(self, instance, cls)
        return getattr(instance, self.name, self.default)

    def __set__(self, instance, value):
        if not isinstance(value, self.type):
            raise TypeError("Значение должно быть типа {}".format(self.type))
        setattr(instance, self.name, value)

    def __delete__(self, instance):
        raise AttributeError("Невозможно удалить атрибут")


class Simple:
    name = TypedProperty("name", str)
    num = TypedProperty("num", int, 42)



f = Simple()
print(f.name)                  # Неявно вызовет Foo.name.__get__(f, Simple)
f.name = "Саша Белый"       # Вызовет Foo.name.__set__(f, "Саша Белый")
# f.name = 333       # Вызовет Foo.name.__set__(f, "Саша Белый")
# del f.name                  # Вызовет Foo.name.__delete__(f)
print(f.name)

f1 = Simple()
print(f1.name)                  # Неявно вызовет Foo.name.__get__(f, Simple)
f1.name = "Фродо"       # Вызовет Foo.name.__set__(f, "Саша Белый")
# del f1.name                  # Вызовет Foo.name.__delete__(f)
print(f1.name, f.name)



