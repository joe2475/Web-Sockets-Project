import socket 

#AF_INET is what corrosponds with IPV4 and SOCK_STREAM is for TCP
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostname(), 1234))
#Que of 5 listens in case traffic becomes full
s.listen(5)

while True:
    print("WEB PROXY SERVER IS LISTENING")
    clientSocket, address = s.accept()

    #Sends data to the client socket
    clientSocket.send()