from socket import *
import http.client
serverName='192.168.219.110'
serverPort=80


clientSocket = socket(AF_INET,SOCK_STREAM)
clientSocket.connect((serverName,serverPort))

#5가지 경우의 케이스를 작성하였고, 이를 해제하면서 테스트 하였습니다.

#올바른 GET 케이스의 경우
# clientSocket.send(b"GET /form.html HTTP/1.0\r\nHost: 192.168.219.110\r\n\r\n")
# recieve_message = clientSocket.recv(65535) # Header 파일 받는 recv
# print(recieve_message.decode())
# recieve_message = clientSocket.recv(65535) # 실제 파일의 내용을 받는 recv
# print(recieve_message.decode())

#올바른 HEAD 케이스의 경우
# clientSocket.send(b"HEAD /form.html HTTP/1.0\r\nHost: 192.168.219.110\r\n\r\n")
# recieve_message = clientSocket.recv(65535)
# print(recieve_message.decode())

#올바른 POST 케이스의 경우
clientSocket.send(b"POST /form2.html HTTP/1.0\r\nHost: 192.168.219.110\r\n\r\n")
clientSocket.sendall("This is the file made by POST".encode()) # client 가 새로운 파일안에 넣고 싶은 TEXT
recieve_message = clientSocket.recv(65535)
print(recieve_message.decode())

# 올바르지 않은 GET 케이스의 경우
# clientSocket.send(b"GET /noform.html HTTP/1.0\r\nHost: 192.168.219.110\r\n\r\n")
# recieve_message = clientSocket.recv(65535)
# print(recieve_message.decode())


# 올바르지 않은 HEAD 케이스의 경우
# clientSocket.send(b"HEAD /noform.html HTTP/1.0\r\nHost: 192.168.219.110\r\n\r\n")
# recieve_message = clientSocket.recv(65535)
# print(recieve_message.decode())





clientSocket.close()

