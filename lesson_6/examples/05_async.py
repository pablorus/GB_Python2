# --------  asyncio ------------

# Модуль asyncio появился в Python версии 3.4.
# В Python 3.5 был добавлен async/await синтаксис. 
# asyncio предоставляет инфраструктуру для написания однопоточного конкурентного кода
# при помощи сопрограмм (corutines), мультиплексирования ввода/вывода данных
# через сокеты и другие ресурсы, запуска сетевых клиентов и серверов, и другие подобные примитивы.

import asyncio

# Сопрограмма - специальная функция, которая возвращает управление объекту, 
# вызвавшему её, сохраняя при этом своё состояние.

# Пример сопрограммы на Python 3.4
@asyncio.coroutine
def my_coro():
    yield from func()

# Cопрограмма на Python 3.5
async def my_coro():
    await func()    



# Рассмотрим пример сопрограммы эхо-сервера
async def handle_echo(reader, writer):
    # Данная функция будет параметром для функции start_server, поэтому она принимает два параметра:
    #  - reader - объект класса StreamReader,
    #  - writer - объект класса StreamWriter ("обёртка" над Транспортом).

    # Ожидаем данные из сопрограммы read()
    data = await reader.read(100)
    message = data.decode()

    # get_extra_info(name, default=None) - возвращает информацию о транспорте
    addr = writer.get_extra_info('peername')
    print("Получено {} от {}".format(message, addr))
    print("Отправлено: {}".format(message))

    # Отправляем данные обратно клиенту.
    # .write(data) - записывает данные в транспорт объекта.
    # При этом WriteTransport.write() - неблокирующая функция, выполняет запись асинхронно.
    writer.write(data)
    # Ожидание ответа от метода drain() даёт возможность циклу событий
    # планировать операцию записи и сбросить буфер в конце. 
    await writer.drain()

    print("Закрываем сокет клиента")
    writer.close()


# Основной функционал модуля asyncio основан на понятии цикл событий (event loop).
# Главная функция цикла событий - ожидание какого-либо события и определенная реакция на него. 

# get_event_loop() возвращает объект цикла событий (AbstractEventLoop) для текущего контекста. 
loop = asyncio.get_event_loop()

# start_server(client_connected_cb, host=None, port=None, *, loop=None, limit=None, **kwds)
# Функция start_server() запускает сокет-сервер,
# создавая фукнцию-callback для каждого подключенного клиента.
# Фукнция-callback client_connected_cb вызывается с двумя параметрами: client_reader, client_writer.
# client_reader - объект класса StreamReader,
# client_writer - объект класса StreamWriter.
coro = asyncio.start_server(handle_echo, 'localhost', 8888, loop=loop)

# Чтобы запустить выполнение сопрограммы, её необходимо добавить в цикл событий.
# Это происходит в самом конце, после определения самого цикла и вызова его метода run_until_complete

# AbstractEventLoop.run_until_complete(future)
# run_until_complete будет выполняться, пока  future  не будет выполнен
server = loop.run_until_complete(coro)


# Запускаем сервер
print('Сервер запущен: {}'.format(server.sockets[0].getsockname()))
try:
    # AbstractEventLoop.run_forever()    
    # Запускает цикл событий, пока явно не будет вызвана функция stop()
    loop.run_forever()
except KeyboardInterrupt:
    pass

# Корректное завершение цикла событий.
# 1. Выключаем сервер
server.close()
# 2. Дожидаемся выключения сервера
loop.run_until_complete(server.wait_closed())
# 3. Закрываем цикл событий
loop.close()
