
# -------------- Множественное наследование ------------------------

# Для отслеживания работы множественного наследования 
# создадим несколько классов:

class BusinessLogic():
    def make_transaction(self):
        print('Транзакция бизнес-логики')    


class BaseProtocol():
    pass
    def make_connection(self):
        print('Базовое TCP-подключение')    


class MagicProtocol():
    def make_connection(self):
        print('Магическое подключение (курьер)')    


class FtpProtocol(BaseProtocol):
    pass
    def make_connection(self):
        print('FTP подключение')


class SftpProtocol(FtpProtocol):
    pass
    def make_connection(self):
        print('SFTP подключение')    


class HttpProtocol(BaseProtocol):
    pass
    def make_connection(self):
        print('HTTP подключение')


class HttpsProtocol(HttpProtocol):
    pass
    def make_connection(self):
        print('HTTPS подключение')

# Создадим общий класс, который унаследован от нескольких классов-протоколов
class BusinessExchange(BusinessLogic,  FtpProtocol, HttpsProtocol, 
                         MagicProtocol):
    pass
    def make_connection(self):
        print('Бизнес-сделка')


# Комментируя в разном порядке в каждом классе метод make_connection,
# можно посмотреть, как меняется поведение класса BusinessExchange:
business_exch = BusinessExchange()
business_exch.make_connection()
business_exch.make_transaction()

# Чтобы узнать порядок разрешения методов, который в данном случае принял Python,
# можно посмотреть значение атрибута __mro__ класса:
print(BusinessExchange.__mro__)

# В классах "нового стиля" (в Python 3 все классы - нового стиля) реализуется
# алгоритм C3-линеаризации для выстраивания "цепочки" классов-родителей:
# https://en.wikipedia.org/wiki/C3_linearization


# Существует, однако, ситуация, когда невозможно выстроить такую "цепочку".
# Неразрешимая ситуация множественного наследования в Python 3:
class XConnection(BaseProtocol):
    def make_connection(self):
        print('x-подключение')


class YConnection(BaseProtocol):
    def make_connection(self):
        print('y-подключение')


class ZConnection(XConnection, YConnection):
    def make_connection(self):
        print('Z-подключение')


class QConnection(XConnection, YConnection):
    def make_connection(self):
        print('Q-подключение')


class MixedConnection(ZConnection, QConnection):
    """docstring for MixedConnection"""
    def make_connection(self):
        print('MIX-подключение')


mixed_conn = MixedConnection()
mixed_conn.make_connection()

