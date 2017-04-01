
# Сервер игры "Запоминалка"

import socketserver
import random

class MemTCPHandler(socketserver.BaseRequestHandler):

    def handle(self):
        self.data = self.request.recv(1024).decode()
        print("Клиент {} сообщает {}".format(self.client_address[0], self.data))

        if self.data == "I_WANNA_PLAY":
            nums = random.sample(range(1,100), 18) * 2
            random.shuffle(nums)
            s_nums = [str(n) for n in nums]
            s_nums = ';'.join(s_nums)

            self.request.sendall(bytes('NUMS;'+s_nums, 'utf-8'))
        else:
            print('Неизвестный запрос')    

          
HOST, PORT = 'localhost', 9999

server = socketserver.TCPServer((HOST, PORT), MemTCPHandler)  
print('Сервер игры запущен')

server.serve_forever()

