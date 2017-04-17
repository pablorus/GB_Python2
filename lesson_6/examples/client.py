
import socket

HOST, PORT = 'localhost', 8888

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))

sock.sendall(b'hello, a?')

sock.close()

