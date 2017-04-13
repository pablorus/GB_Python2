
import multiprocessing as mp
import time

print('Hello, Process!')

def countdown(n):
    while n > -1:
        print(n, 'left')
        time.sleep(1)
        n -= 1

if __name__ == '__main__':
    p1 = mp.Process(target=countdown, args=(50, ))
    p2 = mp.Process(target=countdown, args=(100, ))
    p3 = mp.Process(target=countdown, args=(1000, ))
    p1.start()
    p2.start()
    p3.start()

    while any((p1.is_alive(), p2.is_alive(), p3.is_alive)):
        pass
