
# ---- Обзор возможностей модуля subprocess ----------------------------------
# Модуль subprocess содержит функции и классы, обеспечивающие
# универсальный интерфейс для выполнения таких задач, как создание новых процессов,
# управление потоками ввода и вывода и обработка кодов возврата.

import os
from subprocess import run, Popen, CREATE_NEW_CONSOLE

# Popen(args, **parms)
# Выполняет команду, запуская новый дочерний процесс,
# и возвращает объект класса Popen, представляющий новый процесс.
# Команда определяется в аргументе args либо как строка, такая как 'ls -l',
# либо как список строк, такой как ['ls', '-l'].

# Создаем кортеж расширений файлов, которые будут нужны
EXT = ('.py', '.PY')

# Создаем список файлов с нужным расширением в текущей директории
files = [f.name for f in os.scandir() if f.is_file() and f.name.endswith(EXT)]
print('Файлы для упаковки:', files)

# Для создания процесса используем класс Popen
# Будет создан процесс архиватора. 
# Для Windows флаг CREATE_NEW_CONSOLE укажет создать новую консоль для процесса

# packer = Popen(['7z','a','test.zip', *files],
#                 creationflags=CREATE_NEW_CONSOLE)
# Ждём завершения процесса, чтобы что-то делать дальше...
# packer.wait()

# Можно упростить, т.к. Popen поддерживает менеджер контекста:
with Popen(['7z','a','test.zip', *files],
           creationflags=CREATE_NEW_CONSOLE) as packer:
    print(packer.args)
    print("Ждём упаковку...")

print("Файлы упакованы, можно переименовывать")

# Переименовываем файл, созданный архиватором
os.rename('test.zip', 'kolbasa.zzz')


# В Python 3.5 добавлен упрощенный способ создания процессов - функция run.
# run запускает процесс, ждёт его завершания, возвращает объект CompletedProcess.
# subprocess.run(args, *, stdin=None, input=None, stdout=None, stderr=None, 
#                shell=False, timeout=None, check=False, encoding=None, errors=None)
py_proc = run(['python', '-V'])
print(py_proc)
