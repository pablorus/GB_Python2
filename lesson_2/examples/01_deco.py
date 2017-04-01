
# -------------- Декораторы ----------------------------------
# Декораторы - это фукнции, которые дополняют/модернизируют
# поведение других классов/функций/методов

# Реализуем функцию-декоратор для логгирования аргументов и результата функции,
# к которой он будет применён:
def log(func):

    def decorated(*args, **kwargs):
        res = func(*args, **kwargs)
        print('{}({}, {}) = {}'.format(func.__name__, args, kwargs, res))
        return res

    return decorated    


# Декоратор также может быть реализован в виде класса:
class Log():
    def __init__(self):
        pass

# Магический метод __call__ позволяет обращаться к объекту класса, как к функции
    def __call__(self, func):
        # print("Call---")
        def decorated(*args, **kwargs):
            res = func(*args, **kwargs)
            print('log2: {}({}, {}) = {}'.format(func.__name__, args, kwargs, res))
            return res

        return decorated


log2 = Log()        # <- нужно создать объект, чтобы использоваться его как функцию

# Чтобы применить декоратор к функции нужно воспользоваться синтаксисом
# @имя_декоратора:

@log                # <- такая запись будет аналогична записи  func = log(func) 
def func(a, b):
    return a * b

@log2
def func2(a, b):
    return a ** b

# func = log(func)    
# func2 = log2(func2)    

# Теперь функции имеют дополнительный функционал:
func(14, 15)        
func2(4, 5)
