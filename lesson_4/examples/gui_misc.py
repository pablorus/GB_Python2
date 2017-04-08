
# -------  Модуль для создания дополнительных классов виджетов -----------

import os

from tkinter import *

class ManageButtons(Frame):
    ''' Класс-контейнер для кнопок "Создать, Изменить, Удалить и т.д."
    '''
    def __init__(self, parent=None, btns_dict=None, *args):
        ''' Для инициализации кнопок нужно передать словарь в формате
        {'имя_кнопки1' : callback-функция, ...}
        '''
        super().__init__(parent, *args)
        self.pack()        
        
        self.buttons = []
        if btns_dict:    
            for btn, callback in btns_dict.items():
                # Кнопки будут создаваться с изображениями
                img_file=os.path.join("img", "{}.gif".format(btn))
                img = PhotoImage(file=img_file)
                attr = "btn_{}".format(btn)
                btn = Button(self, image=img, command=callback)
                btn.pack(side=LEFT)

                # Важно сохранить ссылку на картинку, иначе кнопки останутся без изображений
                btn.img = img

                # Все кнопки будут являться атрибутами объекта-контейнера
                setattr(self, attr, btn)
                self.buttons.append(getattr(self, attr))

    def base_callback(self):
        pass        
     

class TableGrid(Frame):
    ''' Заготовка для создания табличного вида
    '''
    def __init__(self, parent=None, titles=None, rows=0, *args, **kwargs):
        w = kwargs.get('w', 300)
        h = kwargs.get('h', 300)
        super().__init__(parent, relief=GROOVE, width=w, height=h, bd=1)
        self.w = w
        self.h = h

        # Создаем возможность вертикальной прокрутки таблицы:
        self._create_scroll()

        # Размещаем заголовки
        for index, title in enumerate(titles):
            Label(self.frame, text=title).grid(row=0, column=index)

        # Создаём пустые строки (для наглядности, что это таблица)
        self.rebuild(len(titles), rows)

        # Размещаем текущий объект self в родительском виджете parent
        self.pack()            

    def _create_scroll(self):
        ''' Обёртка для создания прокрутки внутри Frame.
        Дело в том, что элемент Scrollbar можно привязать
        только к "прокручиваемым" виджетам (Canvas, Listbox, Text),
        в то время как наша "таблица" создана на основе Frame.

        Чтобы решить эту задачу, нужно внутри нашего фрейма создать дополнительные 
        виджеты: Canvas и Frame.
        '''
        self.canvas = Canvas(self)
        self.frame = Frame(self.canvas)

        # Сам по себе Scrollbar - хитрый...
        # Нужно сделать связь не только в Scrollbar, но и в привязанном Canvas'е:
        self.scrollbar = Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # "Упаковываем" Canvas и Scrollbar - один слева, другой справа:
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left")

        # Отрисовываем новый фрейм на Canvas'е
        self.canvas.create_window((0,0), window=self.frame, anchor='nw')

        # При событии <Configure> будет происходить перерисовывание Canvas'а.
        # Событие <Configure> - базовое событие для виджетов;
        # происходит, когда виджет меняет свой размер или местоположение.
        self.frame.bind("<Configure>", lambda e: self._scroll())        


    def _scroll(self):
        """
            Перерисовка канвы и области прокрутки
        """
        self.canvas.config(scrollregion=self.canvas.bbox("all"))
        self.canvas.config(width=self.w, height=self.h)


    def rebuild(self, rows=0, columns=0):
        ''' 
            Пересоздание таблицы полей ввода.
        '''
        self.vars = []
        self.cells = []

        for i in range(1, rows+1):
            self.vars.append([])
            for j in range(columns):
                # Создаём связанную переменную, которая будет "передавать" данные в виджет
                var = StringVar()
                # Внутри нашего виджета будет таблица связанных переменных  (почти MVC шаблон)
                self.vars[i-1].append(var)

                # Создаём ячейку таблицы - это простое текстовое поле Entry с привязанной переменной
                cell = Entry(self.frame, textvariable=var)
                cell.grid(row=i, column=j)

                # Все ячейки тоже "запомним" внутри нашего виджета (чтобы можно было их удалять)
                self.cells.append(cell)
        

    def update_data(self, data_func):
        """ Заполнение таблицы данными.
        Заполнение производится через связанные переменные.
        """
        sql_data = data_func()

        self.rebuild(len(sql_data), len(sql_data[0]))

        for index, data in enumerate(sql_data):
            for i, d in enumerate(data):
                self.vars[index][i].set(d)    


def main():

    def test_callback():
        print('Универсальный пустой callback')

    def sql_get_data():
        ''' Заглушка для табличных данных
        '''
        ls = []
        for i in range(100):
            ls.append((i, 'Терминал_{}'.format(i)))
        return ls    

    main_window = Tk()
    main_window.title('Тест менеджера кнопок')
    grid = TableGrid(main_window, ('id', 'Название'), 2)

    buttons = ManageButtons(main_window, 
                            {'insert':test_callback,
                             'select':lambda :grid.update_data(sql_get_data),
                             'magic':test_callback,
                            }
                           )

    mainloop()


if __name__ == '__main__':
    main()    