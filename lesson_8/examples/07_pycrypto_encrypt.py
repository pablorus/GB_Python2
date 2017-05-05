
# ------------- Модуль PyCrypto для криптографических функций в Питоне --------
# ------------------------- Шифрование сообщений ------------------------------


# Библиотека PyCrypto реализует криптографические примитивы и функции на Питоне.
# Однако данная библиотека не обновляется с 2014 года. 
# PyCryptodome (PyCryptoDomeEx) - это fork библиотеки PyCrypto, развивается.
# Код проекта: https://github.com/Legrandin/pycryptodome

# Установка:  pip install pycryptodome

# PyCryptodome совместима по API с PyCrypto, 
# PyCryptoDomeEx - дополняет/изменяет исходный API.

import os
from binascii import hexlify
from Cryptodome.Cipher import AES

# Для шифрования данных в PyCryptodome есть поддержка нескольких алгоритмов:
#  - блочные шифры: AES, DES, 3DES, Blowfish
#  - поточные шифры: Salsa20, ChaCha20


plaintext = b'The rain in Spain'


def padding_text(text):
    ''' Выравнивание сообщения до длины кратной 16 байтам.
        В данном случае исходное сообщение дополняется пробелами.
    '''
    pad_len = (16 - len(text) % 16) % 16
    return text + b' ' * pad_len


def _encrypt(plaintext, key):
    ''' Шифрование сообщения plaintext ключом key.

        Атрибут iv - вектор инициализации для алгоритма шифрования.
        Если не задаётся явно при создании объекта-шифра, то генерируется случайно.
        Его следует добавить в качестве префикса к финальному шифру, 
        чтобы была возможность правильно расшифровать сообщение.
    '''
    cipher = AES.new(key, AES.MODE_CBC)
    ciphertext = cipher.iv + cipher.encrypt(plaintext)
    return ciphertext


def _decrypt(ciphertext, key):
    ''' Расшифровка шифра ciphertext ключом key

        Вектор инициализации берётся из исходного шифра. 
        Его длина для большинства режимов шифрования всегда 16 байт.
        Расшифровываться будет оставшаяся часть шифра.
    '''
    cipher = AES.new(key, AES.MODE_CBC, iv=ciphertext[:16])
    msg = cipher.decrypt(ciphertext[16:])
    return msg


# Осуществим шифрование сообщения алгоритмом AES
# key (строка байтов) - секретный ключ для симметричного шифрования.
# Ключ должен быть длиной 16 (AES-128), 24 (AES-192) или 32 (AES-256) байта.
key = b'Super Secret Key'

# Длина сообщения должна быть кратна 16, поэтому выполним выравнивание.
plaintext = padding_text(plaintext)

# Выполним шифрование
cipher = _encrypt(plaintext, key)
print(hexlify(cipher))

# Выполним расшифрование
msg = _decrypt(cipher, key)
print(msg)


