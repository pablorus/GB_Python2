# Базы данных


# Импортируем библиотеку, соответствующую типу нашей базы данных 
import sqlite3

# Создаем соединение с нашей базой данных
# В нашем примере у нас это просто файл базы
with sqlite3.connect('company.db3') as conn:

    # Создаем курсор - это специальный объект который делает запросы и получает их результаты
    cursor = conn.cursor()

    # ТУТ БУДЕТ НАШ КОД РАБОТЫ С БАЗОЙ ДАННЫХ
    # КОД ДАЛЬНЕЙШИХ ПРИМЕРОВ ВСТАВЛЯТЬ В ЭТО МЕСТО

    # cursor.execute("""
    #                 create table if not exists Terminal (
    #                     id  INTEGER primary key, 
    #                     title TEXT, 
    #                     configuration TEXT
    #                 );
    #     """)

    # cursor.execute("""
    #                 insert into Terminal (id, title, configuration)
    #                 VALUES (?, ?, ?);""",
    #      (13, 'Terminal Bingo', '{"simle":"nothing"}'))

    cursor.execute('SELECT * FROM Terminal where id = ?', '13')

    z = cursor.fetchone()
    while z:
        print(z)
        z = cursor.fetchone()

# Не забываем закрыть соединение с базой данных
# conn.close()



