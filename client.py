# Echo client program
import socket

HOST = 'IP '                # The remote host
PORT = 50007              # The same port as used by the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
s.sendall('Hello, world')
data = s.recv(1024)
s.close()
print 'Received', repr(data)

출처: http://pydjango.tistory.com/entry/CODE-파이썬-소켓-프로그래밍 [PYTHON & DJANGO]
