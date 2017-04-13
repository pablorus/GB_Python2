
# --------- TCP-сервер, обрабатывающий каждого клиента в отдельном потоке ------
# https://docs.python.org/3.6/library/socketserver.html

import socket
import threading
import socketserver

# Создаем класс-обработчик сообщений пользователя
class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):

    def handle(self):
        data = str(self.request.recv(1024), 'utf-8')
        cur_thread = threading.current_thread()
        response = bytes("{}: {}".format(cur_thread.name, data), 'utf-8')
        self.request.sendall(response)


# Обратите внимание на использование класса-примеси ThreadingMixIn
class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    """ 
        Потоковый сервер. Достаточно создать класс без "внутренностей"
    """
    pass


# Создадим простого "клиента"
def client(ip, port, message):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((ip, port))
        sock.sendall(bytes(message, 'utf-8'))
        response = str(sock.recv(1024), 'utf-8')
        print("Сервер ответил: {}".format(response))


if __name__ == "__main__":
    # Порт 0 позволяет выбрать незанятый порт автоматически
    HOST, PORT = "localhost", 0

    server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
    with server:
        ip, port = server.server_address
        
        # Запускаем поток для цикла сервера.
        # Этот поток будет создавать поток для каждого клиента
        server_thread = threading.Thread(target=server.serve_forever,
                                         name='thread.server')

        # Ставим флаг daemon, чтобы сервер завершился, когда завершится основная программа
        server_thread.daemon = True
        server_thread.start()
        print("Сервер запущен в потоке: {} по адресу {}:{}".format(server_thread.name, ip, port))

        client(ip, port, "Терминал-1 приветствует Вас!")
        client(ip, port, "Привет от терминала-2!")
        client(ip, port, "А третий терминал не будет здороваться...")

        server.shutdown()