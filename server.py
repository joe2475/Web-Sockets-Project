import socket 
#import socketserver
import urllib.request
from urllib import parse
import ssl
import os # For deleting files
import sys # For CMDLN arguments

##################################################
# Setup
cache = [] # Helps keep track of cashed pages. Pages are actually stored in the directory of the server

##########
# Option to change proxy server port
portNumber=50000
if len(sys.argv)>1:
    if int(sys.argv[1])>=0:
        if int(sys.argv[1])<=65535:
            portNumber=int(sys.argv[1])

#########################
# Proxy server set up. This is what the client connects to
# AF_INET is what corresponds with IPV4 and SOCK_STREAM is for TCP
# This socket will be used for connection between the client and the proxy
host = 'localhost' # Proxy runs on localhost
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Host name will be localhost and portNumber is the port number. Port will change just used it for testing purposes. 
s.bind((host, portNumber)) #portNumber default is 50000
#Que of 5 listens in case traffic becomes full
s.listen(5)
#########################



##################################################
# Running Server
while True:
    #########################
    # Waits for client input, then accepts input
    print("WEB PROXY SERVER IS LISTENING")
    s3 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSocket, address = s.accept()
    inData = clientSocket.recv(10000)
    print("MESSAGE RECEIVED FROM CLIENT:")
    # Parses and decodes the incoming http request
    data = inData.decode('utf-8')
    getRequest = data.split('\n')[0]
    method = getRequest.split(' ')[0]
    destAddr = (getRequest.split(' ')[1])[1:]
    version = getRequest.split(' ')[2]
    url = destAddr.split('/')
    hostname = destAddr.split('/')[0]
    hostLen = len(hostname)
    path = destAddr[hostLen:]
    version = getRequest.split(' ')[2]
    urlLen = len(url)
    fileName = url[urlLen-1]
    print('FILENAME: ' + fileName)
    data = data.split('\n')
    for x in range(len(data)): # This prints the header
        print(data[x])
    print("END OF MESSAGE RECEIVED FROM CLIENT")
    print("[PARSE MESSAGE HEADER]")
    print(f'METHOD = {method}, DESTADDRESS = {destAddr}, HTTPVersion = {version}')
     #########################
    # Check if destAddr is cashed ... - No.5 MS 
    addrCached = False
    if os.path.isfile(fileName+".html") : 
        print(f'[LOOK UP THE CACHE]: FOUND IN THE CACHE: FILE = {fileName}')
        addrCached = True
        try: # Take cashed page and send to client
            f = open(fileName+".html",'rb')
            cachedPage=f.read()
            clientSocket.sendall(cachedPage)
            f.close()
            print('RESPONSE FROM HEADER FROM PROXY TO CLIENT:')
            print('HTTP/1.1 200 OK')
            print('Content-Type: text/html;')
            print('END HEADER')
        except:
            f.close()
            print("Error sending cashed page")
        continue
    print("REQUEST MESSAGE SENT TO ORIGINAL SERVER:")
    print('GET / HTTP/1.1')
    print('Host ' + destAddr)
    for x in range(len(data)-2): 
        print(data[x+2])
    # Done with printing, more parsing
    dest = 'Host: ' + hostname + ':80\r\n'
    server_address = (destAddr, 80)
    getMesg = 'GET /' + path + ' HTTP/1.1\r\n'
    destination = ('Host: ' + hostname+ ':80\r\n')
    message  =  bytes(getMesg, encoding='utf-8')    
    message += bytes(dest, encoding='utf-8')
    message += b'Connection: close\r\n'
    message += b'\r\n'
    print("END OF MESSAGE SENT TO ORIGINAL SERVER")
    # End of request parsing from client
    ####################

   
                
    #########################
    if addrCached == False: # Not Cashed
        print("[LOOK UP IN THE CACHE]: NOT FOUND, BUILD REQUEST TO SEND TO ORIGINAL SERVER")
        print(f"[PARSE REQUEST HEADER] HOSTNAME IS {hostname}")
        print(f'[PARSE REQUEST HEADER] URL IS {path}')
        print(f'[PARSE REQUEST HEADER] FILENAME IS {fileName}')
        try:
            s3.connect((hostname, 80))
            s3.sendall(message)
            # Parses response header
            respdata = b''
            while True: 
                buf = s3.recv(1024)
                if not buf:
                    break
                respdata += buf
            response = respdata.decode('utf-8', 'ignore')
            clientSocket.sendall(respdata)
            # Prints the response
            print("RESPONSE HEADER FROM ORIGINAL SERVER")
            #Range is 10 as to not print the html data
            for x in range(6):
                print(response.split('\n')[x])
            print("END OF HEADER\n")
            # Adding to cache        
            if os.path.exists(path[1:] +".html"):
                os.remove(path +".html")
            f = open(fileName + ".html",'a')
            f.write(response)
            f.close()
            cache.append(fileName) # Adds the cached list
            print("RESPONSE HEADER FROM PROXY TO CLIENT:")
            for x in range(10):
                print(response.split('\n')[x])
            print("END HEADER \n") 
            print(f'[WRITE FILE INTO CACHE]:  {fileName}')            
            # Close connection to webserver
            # Send webpage to client
            clientSocket.close()
            s3.close()
        except:
            clientSocket.close()
            s3.close()
            continue

s.close()
