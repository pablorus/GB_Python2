
from tkinter import *
import threading

root = Tk()
root.title("Многопоточная программа")

e = Entry(root, width=17)
e.grid(row=1, column=1, padx=(1, 1))

def writer(filename, n):
    s = str(e.get())
    file = open(filename, "w")
    for i in range(n):
        file.write(s + "\n")
        print(i, filename, s)

def run():
    print('Ща запустим потоки...')
    t1 = threading.Thread(target=writer, args=('text1.txt', 1000,))
    t2 = threading.Thread(target=writer, args=('text2.txt', 1000,))
    t1.start()
    t2.start()
    print('Запустили')


b = Button(root, text="Записать символы в файл", bg="white", fg="black",
                 font="Arial", width=22, height=1, command=run)
b.grid(row=2,column=1,padx=(1, 1))

root.mainloop()