# Урок №7. Асинхронное программирование. Часть 2.

# Материалы урока (examples)
1. 01_async.py - небольшой пример по asyncio
2. 02_async_spin.py - пример с созданием асинхронной прогресс-строки
3. 03_async_download.py - пример асинхронной загрузки файлов с сайта

# Домашнее задание (директория homework)
## asyncio
1. Добавить в асинхронный сервер возможность принимать файлы от клиентов.
2. Модернизировать TCP-клиент. Реализовать функционал через async-сопрограммы:
* клиент скачивает несколько файлов из интернета (список файлов задать простым списком строк с url) по расписанию (AbstractEventLoop.call_at);
* передает скачанные файлы на внутрений TCP-сервер из п.1.

# Ссылки
1. [Шпаргалка по asyncio](https://github.com/crazyguitar/pysheeet/blob/master/docs/notes/python-asyncio.rst)
2. [What Asynchronous is All About?](http://djangostars.com/blog/asynchronous-programming-in-python-asyncio/)
3. [The set of asyncio-based libraries built with high quality for humans](https://github.com/aio-libs)
4. [asyncio — Asynchronous I/O, event loop, and concurrency tools](https://pymotw.com/3/asyncio/index.html)
5. [Abu Ashraf Masnun. Python asyncio: Future, Task and the Event Loop](http://masnun.com/2015/11/20/python-asyncio-future-task-and-the-event-loop.html)
6. [Немного фактов о python asyncio](https://habrahabr.ru/post/314606/)
7. [How the heck does async/await work in Python 3.5?](https://snarky.ca/how-the-heck-does-async-await-work-in-python-3-5/)