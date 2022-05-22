from socket import *
sSocket = socket(AF_INET, SOCK_STREAM)
host = ''
port = 8088
sSocket.bind((host,port))
sSocket.listen(1)
print("접속대기...")
cSocket, addr = sSocket.accept()
print(addr, "에서 접속성공")

filename = 'test.jpg'
file = open(filename, 'wb')
file_data = cSocket.recv(110000)
file.write(file_data)
file.close()
print('받기성공')

ret='success'
cSocket.send(ret.encode())

