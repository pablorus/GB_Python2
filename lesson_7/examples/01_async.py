
import asyncio
import time
import logging

# Для удобства отладки асинхронных задач следует использовать логгирование с уровнем DEBUG
logging.basicConfig(filename="async.log",
    format="%(levelname)-10s %(asctime)s %(message)s",
    level = logging.DEBUG)

logger = logging.getLogger('async')


# Определим асинхронную сопрограмму
async def _task(name, sec):
    logger.info('Enter _task {}'.format(name))
    print(name, 'Task was started')

    # Обёртка try..except нужна для того,
    # чтобы корректно обработать прерывание задачи методом  .cancel()
    try:
        await asyncio.sleep(sec)
    except asyncio.CancelledError:
        print('I was killed') 

    print(name, 'Task was finished')    
    logger.info('End _task {}'.format(name))
    return 'task {} finished'.format(name)


# Определим "менеджера" задач
async def manager():
    # task1 = asyncio.ensure_future(_task('task1', 7))         
    # task2 = asyncio.ensure_future(_task('task2', 5))    

    # "Менеджер" будет ожидать завершения всех запущенных задач
    await asyncio.wait([_task('task2', 5), _task('task1', 7)])


if __name__ == '__main__':
    # Асинхронные сопрограммы не работают сами по себе. 
    # Они запускаются циклом событий (Event Loop)
    loop = asyncio.get_event_loop()
    try:
        print('Старт цикла событий')
        # task1 = loop.create_task(_task('Seven', 7))         # ensure_future(_task(5))
        # task2 = loop.create_task(_task('Fives', 5))         # ensure_future(_task(5))

        # Обратите внимание, системное время и время цикла событий - разные величины
        # t = loop.time()
        # tt = time.time()
        # print(t, tt)

        # loop.call_soon(task1)
        # loop.call_at(t + 1, task1)

        loop.run_until_complete(manager())
    finally:
        loop.close() 

    # print('Task1: {}'.format(task1.result()))    
    # print('Task2: {}'.format(task2.result()))    



