
# ----- Простой сокет-клиент для демонстрации работы с pickle-данными ---------

import pickle
import socket
 
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("localhost", 9999))
 
# Получаем опасное сообщение
message = sock.recv(1024)

# Распаковываем, "радуемся" - нас взломали...
pickle.loads(message)

sock.close()
