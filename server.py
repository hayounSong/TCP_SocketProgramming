from socket import *
from datetime import datetime
import sys
from os.path import exists, getsize
serverPort=80

serverSocket=socket(AF_INET,SOCK_STREAM)

serverSocket.bind(('192.168.219.110',serverPort)) #서버 실행

serverSocket.listen()
print("The server start running..")

while True:

    connectionSocket,addr=serverSocket.accept()


    message=connectionSocket.recv(65535).decode() #client에게 요청된 메시지 수신

    request_data = message.split()
    request_method = request_data[0]


    print(message)

    filename = './' + message.split('\r\n')[0].split(' ')[1]  # 요청한 파일의 이름을 request message에서 추출

    content_type = message.split('\r\n')[0].split(' ')[1].split('.')[1]
    # content-Type이 어떤건지 알기 위해서 html인지,json인지 이런걸 알기 위해 split을 통해 파일명에서 type가져오기

    if request_method=="GET":
        if not exists(filename):  # 파일이 없는 경우
            print('Server Error : No File in server!')  # 오류 출력
            msg = "HTTP/1.0 404 NOT FOUND\r\nRequest: GET\r\nHost:192.168.219.110" # 본래 HTTP response문에서는 Request 출력이 없으나, 원활한 구분을 위해 사용
            connectionSocket.sendall(msg.encode())  # client에게 response message, 404에러 메시지 전송
            connectionSocket.close()  # 연결 종료

        else:  # 파일이 있는 경우
            size = getsize(filename)
            msg = "HTTP/1.0 200 OK\r\nRequest: GET\r\nHost:192.168.219.110\r\nContent-Type:"+content_type+"; charset=UTF-8\r\nContent-Length: %d\r\nConnection: close" % size # 본래 HTTP request문에서는 Request 출력이 없으나, 원활한 구분을 위해 사용
            with open(filename, 'r',encoding="UTF-8") as f:  #요청한 파일의 내용을 담기
                data = ''
                for line in f:
                    data += line  # data에 요청한 파일 내용 저장

            connectionSocket.send(msg.encode())  # client에게 200 성공 response message 전송
            connectionSocket.send(data.encode()) # client에게 요청한 파일의 내용 전송
            connectionSocket.close()  # 연결 종료


    if request_method=="HEAD":
        if not exists(filename):  # 파일이 없는 경우
            print('Server Error : No File!')  # 오류 출력
            msg = "HTTP/1.0 404 NOT FOUND\r\nRequest: HEAD\r\nHost:192.168.219.110\r\nContent-Type:"+content_type+"; charset=UTF-8\r\nConnection: close" # 본래 HTTP request문에서는 Request 출력이 없으나, 원활한 구분을 위해 사용
            connectionSocket.sendall(msg.encode())  # client에게 response message, HEAD문에 대한, 왜냐면 filename이 없기 때문 404에러 메시지 전송
            connectionSocket.close()  # 연결 종료
        else:
            size = getsize(filename)
            msg = "HTTP/1.0 200 OK\r\nRequest: HEAD\r\nHost:192.168.219.110\r\nContent-Type:"+content_type+"; charset=UTF-8\r\nContent-Length: %d\r\nConnection: close" % size  # 본래 HTTP request문에서는 Request 출력이 없으나, 원활한 구분을 위해 사용
            connectionSocket.send(msg.encode())  # client에게 HEAD문 처리 성공 200 성공 response message 전송
            connectionSocket.close()  # 연결 종료


    if request_method=="POST":

        inline=message.split('\r\n')[3] # 파일안에 들어갈 TEXT 내용
        nontype_filename=message.split('\r\n')[0].split(' ')[1].split('.')[0].split('/')[1]
        #content-Type을 제외한 파일의 순수이름 form.html이면 form만 저장하는 식.

        f = open(nontype_filename+'.'+content_type, 'w') #실제 요청에 맞추어 파일 생성
        f.write(inline) # TEXt 입력 새파일에
        f.close()

        size=getsize(nontype_filename+'.'+content_type)
        msg = "HTTP/1.0 201 OK\r\nRequest: POST\r\nHost:192.168.219.110\r\nContent-Type:"+content_type+"; charset=UTF-8\r\nContent-Length: %d\r\nConnection: close"% size
        # 본래 HTTP reqsponse문에서는 Request 출력이 없으나, 원활한 구분을 위해 사용
        # 추가로 POST에서 성공할 경우에 200을 출력하기도 하나, 최근에는 정확한 구분을 위해 201을 출력하는 경우가 늘어나고 있기에 201로 출력, 하지만 200으로 출력해도 가능.

        connectionSocket.send(msg.encode())  # client에게 POST문 처리 성공 201 성공 response message 전송
        connectionSocket.close()  # 연결 종료



