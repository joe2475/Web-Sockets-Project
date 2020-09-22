#Client side 
import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect((socket.gethostname(), 1234))
while True:
    #1024 is a buffer for how much data you want at a time. This will change when headers are implemented.   
    msg = s.recv(1024)
    print(msg.decode("utf-8"))
