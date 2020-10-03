import socket 
import socketserver

host = 'localhost'
#AF_INET is what corrosponds with IPV4 and SOCK_STREAM is for TCP
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#Host name will be localhost and 1234 is the port number. Port will change just used it for testing purposes. 
s.bind((host, 1234))
#Que of 5 listens in case traffic becomes full
s.listen(5)
#print(socket.gethostname())

while True:
    print("WEB PROXY SERVER IS LISTENING")
    clientSocket, address = s.accept()
    data = clientSocket.recv(10000)
    #print(data)
    print("MESSAGE RECEIVED FROM CLIENT:")
    data = data.decode('utf-8')
    data = data.split('\n')
    for x in range(len(data)):
        print(data[x])
    print("END OF MESSAGE RECEIVED FROM CLIENT")
    
    exit()
   # clientSocket.close()
 #   s.close()