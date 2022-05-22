from socket import *
host = '127.0.0.1'
port = 8088
addr = (host, port)
cSocket = socket(AF_INET, SOCK_STREAM)
cSocket.connect(addr)
print('서버연결성공')

filename = 'jdh.jpg'
file = open(filename, 'rb')
file_data = file.read(110000)
cSocket.send(file_data)

data = cSocket.recv(1024)
ret = data.decode()
print(ret)
