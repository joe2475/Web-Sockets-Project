import socket 
import socketserver

host = 'localhost'
#AF_INET is what corrosponds with IPV4 and SOCK_STREAM is for TCP
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#Host name will be localhost and 1234 is the port number. Port will change just used it for testing purposes. 
s.bind((host, 50000))
#Que of 5 listens in case traffic becomes full
s.listen(5)
#print(socket.gethostname())

while True:
    print("WEB PROXY SERVER IS LISTENING")
    clientSocket, address = s.accept()
    data = clientSocket.recv(10000)
    #print(data)
    print("MESSAGE RECEIVED FROM CLIENT:")
    #Parses and decodes the incoming http request 
    data = data.decode('utf-8')
    getRequest = data.split('\n')[0]
    method = getRequest.split(' ')[0]
    destAddr = (getRequest.split(' ')[1])[1:]
    version = getRequest.split(' ')[2]
    data = data.split('\n')
    for x in range(len(data)):
        print(data[x])
    print("END OF MESSAGE RECEIVED FROM CLIENT")
    print("[PARSE MESSAGE HEADER]")
    print(f'METHOD = {method}, DESTADDRESS = {destAddr}, HTTPVersion = {version}')
    
    exit()
   # clientSocket.close()
 #   s.close()