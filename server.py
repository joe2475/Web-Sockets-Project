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
    GET = data.split('\n')[0]
    hostName = data.split('\n')[1]
    connection = data.split('\n')[2]
    upgrade = data.split('\n')[4]
    user_agent = data.split('\n')[5]
    accept = data.split('\n')[6]
    print(GET)
    print(hostName)
    print(connection)
    print(upgrade)
    print(user_agent)
    print(accept)
    print("END OF MESSAGE RECEIVED FROM CLIENT")
    
    exit()
   # clientSocket.close()
 #   s.close()