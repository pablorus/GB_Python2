
# ------------- Заготовка для графического администрирования БД -------

import os
import time

from datetime import datetime

from tkinter import *
from tkinter.messagebox import *

# Обратите внимание на модуль app_log в директории с данным скриптом
from app_opt import log_it

# Обратите внимание на модуль gui_misc в директории с данным скриптом
from gui_misc import ManageButtons, TableGrid


def not_implemented(x='13'):
    print("Не реализовано", x)
    # showerror('Скоро', 'Будет функция!')


def z_callback(event):
    print("ZZZ")


@log_it
def sql_get_terminals():
    ''' SQL-заглушка
    '''
    ls = []
    for i in range(40):
        ls.append((i, 'Терминал_{}'.format(i), 'описание...'))
    return ls


@log_it
def main_callback(event):
    print("Заглушка. Не реализовано")


@log_it
def create_terminal():
    ''' Создание дочернего окна
    '''
    print('Создано доп. окно: {}'.format(datetime.today()))
    form = Toplevel(main_window)        
    form.title('Создать терминал')
    
    # Чтобы сделать дочернее окно модальным нужно выполнить 3 функции:
    # 1. form.transient(root) - создание дочернего окна для root;
    # 2. form.grab_set() - захват фокуса дочерним окном;
    # 3. root.wait_window(form) - главное окно будет ждать закрытия дочернего.
    form.transient(main_window)
    form.grab_set()
    main_window.wait_window(form)


@log_it
def mix_up(btns):
    prev = None
    for btn in btns:
        time.sleep(0.5)

        # Метод update производит перерисовку виджета.
        # Имеет смысл вызывать её в долгих циклах для обновления интерфейса.
        main_window.update()

        if prev is not None:
            btn.column, prev.column = prev.column, btn.column
            btn.grid(row=btn.row, column=btn.column)
            prev.grid(row=prev.row, column=prev.column)

        prev = btn    


# Можно создавать свои классы, унаследованные от стандартных классов tkinter:
class StatusBar(Frame):
    ''' Заготовка для статусной строки, отражающей информацию:
        - подключение к БД (имя БД, пользователь),
        - текущее время,
        - прочую информацию.
    '''
    def __init__(self, parent=None, *args):
        super().__init__(parent)
        self.pack(side=BOTTOM)

        self.clock = Label(self, text=datetime.today().strftime('%H:%M:%S'))
        self.clock.pack(side=RIGHT)
        self.after(1000, self.tik_tak)

    def tik_tak(self):
        ''' Выводит текущее время в Label, а потом делает отложенный вызов самой себя
        '''
        self.clock.config(text=datetime.today().strftime('%H:%M:%S'))
        self.after(1000, self.tik_tak)
        # print('exit')     # <- Раскомментируйте эту строку, чтобы увидеть, что это не рекурсия



# Кнопка может быть создана следующим образом:
# btn = Button(main_window,  # text='Создать БД',
#                  image=imgs[i], 
#                  command=lambda : not_implemented(13))

# Компоновщики pack, grid не совместимы друг с другом
# btn.pack(side=BOTTOM)         
# btn.grid(row=0, column=i)

# Виджет можно настроить уже после того, как он создан:
# btn.config(command=create_terminal)        


# Создаем основное окно программы
main_window = Tk()

# Можно произвести простые настройки окна.
# Задать минимальный размер окна:
# main_window.minsize(400, 400)

# Задать размеры и расположение окна:
# main_window.geometry('400x400+550+280') 

# Чуть посложнее - разместить окно по центру экрана.
# Для этого вычислим координаты середины экрана.
# Сначала определим ширину и высоту:
ws = main_window.winfo_screenwidth()       
hs = main_window.winfo_screenheight()      

w = 400
h = 400

# Затем вычислим координаты при выбранных ширине и высоте:
x = ws//2 - w//2
y = hs//2 - h//2

# Зададим размеры и расположение окна:
main_window.geometry('{}x{}+{}+{}'.format(w, h, x, y)) 

# Заблокируем возможность изменять размеры:
main_window.resizable(width=False, height=False)

# Установим заголовок окна и значок:
main_window.title('Звёздный администратор')
main_window.iconbitmap('favicon.ico')


# Создадим "наши" виджеты: таблицу и статусную строку:
grid = TableGrid(main_window, ('id', 'Название', 'Описание'), 3, w=w)
statusbar = StatusBar(main_window)

# Обратите внимание на класс ManageButtons из модуля gui_misc
buttons = ManageButtons(main_window, {'insert':not_implemented, 
                                      'update':not_implemented,
                                      'delete':not_implemented,
                                      'select':not_implemented,
                                      'magic':create_terminal,
                                     }
                        )

# Для создания меню сначала создаётся корневой элемент:
main_menu = Menu(main_window)

# Потом создаются дочерние элементы меню:
file_menu = Menu(main_menu)
file_menu.add_command(label='Терминалы',
                      command=lambda g=grid: g.update_data(sql_get_terminals))
file_menu.add_command(label='Транзакции', command=not_implemented)

# Дочерние элементы нужно явно добавить в родительское меню:
main_menu.add_cascade(label='База данных', menu=file_menu)


# Привязка события к функции.
# Функция main_callback будет вызвана при нажатии правой кнопки мыши:
main_window.bind('<Button-3>', main_callback)

# Функция z_callback будет вызвана при нажатии клавиши  z:
main_window.bind('z', z_callback)

# Добавление меню главному окну:
main_window.config(menu=main_menu)

# Отложенный вызов функции.
# Функция mix_up(btn_list) будет вызвана через 2000 мс от текущего момента:
# main_window.after(2000, mix_up, btn_list)

# Запуск основного цикла программы:
mainloop()
