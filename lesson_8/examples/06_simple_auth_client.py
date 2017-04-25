
# ------------- Простая аутентификация клиента. Реализация клиента -------------

import hmac
import os

def client_authenticate(connection, secret_key):
    ''' Аутентификация клиента на удаленном сервисе.
        Параметр connection - сетевое соединение (сокет);
        secret_key - ключ шифрования, известный клиенту и серверу
    '''
    message = connection.recv(32)
    hash = hmac.new(secret_key, message)
    digest = hash.digest()
    connection.send(digest)


# ------------- Клиент -------------------------------------------

from socket import socket, AF_INET, SOCK_STREAM

secret_key = b'our_secret_key'

sock = socket(AF_INET, SOCK_STREAM)
sock.connect(('localhost', 9999))

client_authenticate(sock, secret_key)

sock.send(b'Hello, my secure server!')
resp = sock.recv(1024)
print('Сервер ответил: ', resp.decode())