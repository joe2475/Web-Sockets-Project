import socket 
#import socketserver
import urllib.request
import ssl
host = 'localhost'
#AF_INET is what corrosponds with IPV4 and SOCK_STREAM is for TCP
#This socket will be used for connection between the client and the proxy
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#Host name will be localhost and 1234 is the port number. Port will change just used it for testing purposes. 
s.bind((host, 50000))
#Que of 5 listens in case traffic becomes full
s.listen(5)
#Second socket that is used to connect to the web server. 
context = ssl.create_default_context()
while True:
    print("WEB PROXY SERVER IS LISTENING")
    clientSocket, address = s.accept()
    inData = clientSocket.recv(10000)
    #print(data)
    print("MESSAGE RECEIVED FROM CLIENT:")
    #Parses and decodes the incoming http request 
    data = inData.decode('utf-8')
    getRequest = data.split('\n')[0]
    method = getRequest.split(' ')[0]
    destAddr = (getRequest.split(' ')[1])[1:]
    version = getRequest.split(' ')[2]
    data = data.split('\n')
    upinsecure = data[4]
    userAgent = data[5]
    accept = data[6]
    aceceptInc = data[11]
    acceptLang = data[12]
    for x in range(len(data)):
        print(data[x])
    print("END OF MESSAGE RECEIVED FROM CLIENT")
    print("[PARSE MESSAGE HEADER]")
    print(f'METHOD = {method}, DESTADDRESS = {destAddr}, HTTPVersion = {version}')
    print("Dest:" + destAddr)
    print("REQUEST MESSAGE SENT TO ORIGINAL SERVER:")
    print('Host ' + destAddr)
    print('Connection: close')
    print(upinsecure)
    print(userAgent)
    print(accept)
    print(aceceptInc)
    print(acceptLang)
    
    dest = 'Host: ' + destAddr + ':80\r\n'
    server_address = (destAddr, 80)
    destination = ('Host: ' + destAddr + ':80\r\n')
    message  = b'GET / HTTP/1.1\r\n'
    message += bytes(dest, encoding='utf-8')
    message += b'Connection: close\r\n'
    message += b'\r\n'
    print("END OF MESSAGE SENT TO ORIGINAL SERVER")
    #Uses a second socket to connect to the destination server
    s2 = context.wrap_socket(socket.socket(socket.AF_INET), server_hostname=destAddr)
    s2.connect((destAddr, 443))
    s2.sendall(message)

    #Parses response header
    respdata = b''
    while True: 
        buf = s2.recv(1024)
        if not buf:
            break
        respdata += buf
    response = respdata.decode('utf-8', 'ignore')
    #Prints the reponse
    print("REPSONSE HEADER FROM ORIGINAL SERVER")
    #Range is 10 as to not print the html data
    for x in range(10):
        print(response.split('\n')[x])
    print("END OF HEADER")
   # print(temp)
    s2.close()
    clientSocket.sendall(respdata)
    clientSocket.close()
    #exit()
    #s.close()
    break
s.close()