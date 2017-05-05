
# ------------- Модуль PyCrypto для криптографических функций в Питоне --------
# --------------- Создание и проверка цифровых подписей сообщений -------------

# Библиотека PyCrypto реализует криптографические примитивы и функции на Питоне.
# Однако данная библиотека не обновляется с 2014 года. 
# PyCryptodome (PyCryptoDomeEx) - это fork библиотеки PyCrypto, развивается.
# Код проекта: https://github.com/Legrandin/pycryptodome

# Установка:  pip install pycryptodome

# PyCryptodome совместима по API с PyCrypto, 
# PyCryptoDomeEx - дополняет/изменяет исходный API.

import os
from binascii import hexlify
from Cryptodome.Hash import SHA256
from Cryptodome.PublicKey import RSA, DSA
from Cryptodome.Signature import pkcs1_15, DSS

# Существует несколько стандартов для формирования цифровой подписи сообщений.

# DSA (Digital Signature Algorithm - алгоритм цифровой подписи) - криптографический алгоритм
# с использованием открытого ключа для создания электронной подписи, но не для шифрования 
# Подпись создается секретно, но может быть публично проверена. 
# Это означает, что только один субъект может создать подпись сообщения, 
# но любой может проверить её корректность. 
# DSA является частью DSS (Digital Signature Standard - стандарт цифровой подписи).

# Стандарт PKCS относится к группе Public Key Cryptography Standards
# (Стандарты криптографии с открытым ключом) разработанным и опубликованным RSA Laboratories.
# PKCS #1 описывает базовые принципы работы с ключами в алгоритме RSA.
# RSA - криптографический алгоритм с открытым ключом, основывающийся 
# на вычислительной сложности задачи факторизации больших целых чисел.


# Общая последовательность формирования цифровой подписи сообщения:
# 1. Вычиление хэш-образа для сообщения (например, семейством алгоритмов SHA).
# 2. Получение подписи: хэш-образ шифруется закрытым ключом автора сообщения (DSA, RSA, ElGamal).
# 3. Передача по сети исходного сообщения и сформированной подписи.

# Общая последовательность проверки цифровой подписи сообщения:
# 1. Получение сообщения, содержащего открытый текст сообщения и его цифровую подпись.
# 2. Вычиление хэш-образа открытого текста сообщения (H1).
# 3. Вычисление контрольного хэш-образа (H2) через расшифровку 
#    цифровой подписи открытым (публичным) ключом.
# 4. Сравнение H1 и H2.


plaintext = b'The rain in Spain falls mainly on the Plain'


def DSA_sign(plaintext, key):
    ''' Создание цифровой подписи для сообщения plaintext закрытым ключом key
        по стандарту DSS (алгоритм DSA).
        Обратите внимание, что для одного и того же сообщения 
        с одним и тем же ключом алгоритм DSA будет создавать отличающиеся 
        байтовые строки подписи - это особенность алгоритма.
    '''
    hash_obj = SHA256.new(plaintext)
    signer = DSS.new(key, 'fips-186-3')
    signature = signer.sign(hash_obj)
    return signature


def DSA_check_sign(plaintext, signature, pub_key):
    ''' Проверка цифровой подписи signature для соообщения plaintext
        открытым ключом pub_key по стандарту DSS
    '''
    hash_obj = SHA256.new(plaintext)
    verifier = DSS.new(pub_key, 'fips-186-3')
    try:
        verifier.verify(hash_obj, signature)
        print("DSS. Сообщение достоверно")
        return True
    except ValueError:
        print("DSS. Сообщение недостоверно")
        return False


def RSA_sign(plaintext, key):
    ''' Создание цифровой подписи для сообщения plaintext закрытым ключом key
        по стандарту PKCS#1 v1.5 (алгоритм RSA)
    '''
    hash_obj = SHA256.new(plaintext)
    signer = pkcs1_15.new(key)
    signature = signer.sign(hash_obj)
    return signature


def RSA_check_sign(plaintext, signature, key):
    ''' Проверка цифровой подписи signature для соообщения plaintext
        открытым ключом pub_key по стандарту PKCS#1 v1.5
    '''    
    hash_obj = SHA256.new(plaintext)
    signer = pkcs1_15.new(key)
    try:
        signer.verify(hash_obj, signature)
        print("PKCS#1. Сообщение достоверно")
        return True
    except (ValueError, TypeError):
        print("PKCS#1. Сообщение недостоверно")
        return False    


# Осуществим подпись и проверку подписи по алгоритму RSA
key_RSA = RSA.generate(1024, os.urandom)
signature = RSA_sign(plaintext, key_RSA)
print(hexlify(signature))
print(RSA_check_sign(plaintext, signature, key_RSA.publickey()))


# Осуществим подпись и проверку подписи по алгоритму DSA
key_DSA = DSA.generate(1024, os.urandom)
signature = DSA_sign(plaintext, key_DSA)
print(hexlify(signature))
print(DSA_check_sign(plaintext, signature, key_DSA.publickey()))

