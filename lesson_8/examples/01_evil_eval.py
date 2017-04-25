
# ------------- Примеры работы с функцией eval --------------

# Будьте осторожны с функцией eval:
eval("__import__('os').system('echo evil_eval BU-ga-ga')")


# Можно попробовать обезопасить себя почистив __builtins__: 
eval("__import__('os').system('echo evil_eval coming again')", {'__builtins__':{}})


# Но это тоже можно обойти... 
# Будьте аккуратны, код ниже 
# приведёт к некорректному завершению работы интерпретатора
s = """
(lambda fc=(
    lambda n: [
        c for c in 
            ().__class__.__bases__[0].__subclasses__() 
            if c.__name__ == n
        ][0]
    ):
    fc("function")(
        fc("code")(
            0,0,0,0,0,b"BO00OM",(),(),(),"","",0,b""
        ),{}
    )()
)()
"""
eval(s, {'__builtins__':{}})
