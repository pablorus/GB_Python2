
import asyncio
import itertools
import time
import sys

import logging

logging.basicConfig(filename="async_spin.log",
    format="%(levelname)-10s %(asctime)s %(message)s",
    level = logging.DEBUG)
logger = logging.getLogger('async')


# Создадим сопрограмму, которая будет выводить ASCII-прогресс (крутящаяся палочка)
async def spin(msg):
    # Воспользуемся средствами стандратного вывода (print не очень подойдёт)
    write, flush = sys.stdout.write, sys.stdout.flush
    for char in itertools.cycle('|/-\\'):
        status = char + ' ' + msg
        write(status)
        flush()
        write('\x08' * len(status))
        try:
            # Делаем асинхронный sleep, чтобы немного затормозить "крутяшку"
            await asyncio.sleep(.1)
        except asyncio.CancelledError:
            break
    write(' ' * len(status) + '\x08' * len(status))


# Создадим сопрограмму, ожидающую операции ввода/вывода
async def slow_function():
    # Эмуляция ожидания операции ввода/вывода
    await asyncio.sleep(5)
    return 42


# Супервизов ("менеджер") управляет запуском других сопрограмм, 
# сам являясь сопрограммой.
async def supervisor():
    spinner = asyncio.ensure_future(spin('думаю, не мешай!'))
    print('Объект прогресс-бар:', spinner)
    
    # Ожидаем завершения slow_function
    result = await slow_function() 

    # Как только slow_function будет завершена, отменим прогресс-бар
    spinner.cancel()
    return result


def main():
    loop = asyncio.get_event_loop()
    try:
        result = loop.run_until_complete(supervisor())
    finally:    
        loop.close()

    print('Answer:', result)


if __name__ == '__main__':
    main()    