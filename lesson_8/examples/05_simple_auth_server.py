
# ------------- Простая аутентификация клиента. Реализация сервера -------------

import hmac
import os

# HMAC - Keyed-Hashing for Message Authentication.
# Модуль hmac служит для вычисления хэш-функции с ключом от сообщения. 
# Такой подход используется для аутентификации сообщений.
# Подробное описание алгоритма содержится в RFC 2104 (https://tools.ietf.org/html/rfc2104.html).

# Возможности данного модуля могут применены для аутентификации клиента.

#                            Общая схема работы
#                 СЕКРЕТ известен только клиенту и серверу (ключ)
# ----------------------                           ----------------------------                                         
# |       Клиент        |                         |           Сервер           |
# |-------------------- |  запрос_аутентификации  |----------------------------|                      
# |                     | ----------------------> |      Генерация rnd_msg     | 
# |                     |         rnd_msg         |                            |       
# |                     | <---------------------  |                            |        
# |     Вычисление      |                         |         Вычисление         |    
# |HMAC(СЕКРЕТ, rnd_msg)|                         |    HMAC(СЕКРЕТ, rnd_msg)   |      
# |                     |                         |                            |       
# |                     |       HMAC_клиент       |                            |     
# |                     | ----------------------> |         Сравнение          |     
# |                     |                         | HMAC_клиент == HMAC_сервер |   
# |                     |                         |            |  |            |       
# |                     |       свой (доверие) <--------------да   нет         |      
# |                     | <====================== |                 |--> чужой |           
# -----------------------                          ----------------------------


# hmac.new(key, msg=None, digestmod=None)
# key - byte-строка, представляющая ключ
# msg - сообщение, для которого нужно вычислить хэш
# digestmod - имя хэш-фукнции, которая будет применена для вычисления (sha-1, sha-256, ...)


# -------------- Функция аутентификации клиента на сервере --------------------
def server_authenticate(connection, secret_key):
    ''' Запрос аутентификаии клиента.
        сonnection - сетевое соединение (сокет);
        secret_key - ключ шифрования, известный клиенту и серверу
    '''
    # 1. Создаётся случайное послание и отсылается клиентв
    message = os.urandom(32)
    connection.send(message)

    # 2. Вычисляется HMAC-функция от послания с использованием секретного ключа
    hash = hmac.new(secret_key, message)
    digest = hash.digest()

    # 3. Пришедший ответ от клиента сравнивается с локальным результатом HMAC
    response = connection.recv(len(digest))
    return hmac.compare_digest(digest, response)


# Выдержка из официальной документации, которая советует для сравнения хэш-сумм
# использовать крипто-безопасную функцию hmac.compare_digest, а не оператор ==
# ---------------------------------------------------------------------
# Warning:
# When comparing the output of digest() to an externally-supplied digest
# during a verification routine, it is recommended to use 
# the compare_digest() function instead of the == operator 
# to reduce the vulnerability to timing attacks. 
# ---------------------------------------------------------------------


# ---------------------- Эхо-сервер -----------------------------------------
from socket import socket, AF_INET, SOCK_STREAM

secret_key = b'our_secret_key'

def echo_handler(client_sock):
    ''' Эхо-обработка.
        Проводит аутентификацию клиента и отсылает его же запрос обратно (эхо).
    '''
    if not server_authenticate(client_sock, secret_key):
        client_sock.close()
        return
    while True:
        msg = client_sock.recv(8192)
        if not msg:
            break
        client_sock.sendall(msg)


def echo_server(address):
    ''' Эхо-сервер.
        "Слушает" указанный адрес и общается с клиентом через echo_handler. 
    '''
    sock = socket(AF_INET, SOCK_STREAM)
    sock.bind(address)
    sock.listen(5)
    while True:
        conn, addr = s.accept()
        echo_handler(conn)


echo_server(('', 9999))        
