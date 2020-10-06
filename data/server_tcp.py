import socket
import sys
import os.path
import operator
import os

serverControlPort = int(sys.argv[1])
serverDataPort = int(sys.argv[2])


serverSocket_Control = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
serverSocket_Data = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

serverSocket_Control.bind(('',serverControlPort))
serverSocket_Control.listen(10)
print('SERVER SOCKET LISTENING FOR CONTROL....')

serverSocket_Data.bind(('',serverDataPort))
serverSocket_Data.listen(10)
print('SERVER SOCKET LISTENING FOR DATA....')

socketNAME = socket.gethostname()
print(socket.gethostbyname(socketNAME))

while True:
    
    connectionSocket_Control, addr1 = serverSocket_Control.accept()
    print('ACCEPTED CONTROL CONNECTION....')
    connectionSocket_Data, addr2 = serverSocket_Data.accept()
    print('ACCEPTED DATA CONNECTION....')
    
    print ('CONNECTED TO : ', addr1)

    print ('WAITING FOR CLIENT COMMAND....')
    
    client_request = connectionSocket_Control.recv(1024)
    print('request received')
    request_str = client_request.decode("utf-8")
     
    req_str = request_str.split(" ")


    if req_str[0] == 'get':
        
        print('GETTING FILE')
        f = open(req_str[1], "rb")
        l = f.read(1024)
        while(l):
            print('Sending')
            connectionSocket_Data.send(l)
            l = f.read(1024)
        f.close()
        print('Sent')
       

    elif req_str[0] == 'cd':
        os.chdir(req_str[1])
        data = os.getcwd()
        print("Data : ", data)
        connectionSocket_Data.send(data.encode('utf-8'))
        
    elif req_str[0] == 'ls':
        data = os.popen(request_str).read()
        connectionSocket_Data.send(data.encode('utf-8'))
   
    elif req_str[0] == 'put':
        
        f = open(req_str[1], "wb")
        l = connectionSocket_Data.recv(1024)
        while(l):
            f.write(l)
            l = connectionSocket_Data.recv(1024)
        f.close()
        
    connectionSocket_Control.close()
    connectionSocket_Data.close()
    serverSocket_Control.close()
    serverSocket_Data.close()
    