import socket 
#import socketserver
import urllib.request
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
# Second Socket
context = ssl.create_default_context() # Socket that is used to connect to the web server. 
#########################



##################################################
# Running Server
while True:
    #########################
    # Waits for client input, then accepts input
    print("WEB PROXY SERVER IS LISTENING")
    clientSocket, address = s.accept()
    inData = clientSocket.recv(10000)
    print("MESSAGE RECEIVED FROM CLIENT:")
    # Parses and decodes the incoming http request
    data = inData.decode('utf-8')
    getRequest = data.split('\n')[0]
    method = getRequest.split(' ')[0]
    destAddr = (getRequest.split(' ')[1])[1:]
    version = getRequest.split(' ')[2]
    data = data.split('\n')
    for x in range(len(data)): # This prints the header
        print(data[x])
    print("END OF MESSAGE RECEIVED FROM CLIENT")
    print("[PARSE MESSAGE HEADER]")
    print(f'METHOD = {method}, DESTADDRESS = {destAddr}, HTTPVersion = {version}')
    print("Dest:" + destAddr)
    print("REQUEST MESSAGE SENT TO ORIGINAL SERVER:")
    print('GET / HTTP/1.1')
    print('Host ' + destAddr)
    for x in range(len(data)-2): 
        print(data[x+2])
    # Done with printing, more parsing
    dest = 'Host: ' + destAddr + ':80\r\n'
    server_address = (destAddr, 80)
    destination = ('Host: ' + destAddr + ':80\r\n')
    message  = b'GET / HTTP/1.1\r\n'
    message += bytes(dest, encoding='utf-8')
    message += b'Connection: close\r\n'
    message += b'\r\n'
    print("END OF MESSAGE SENT TO ORIGINAL SERVER")
    # End of request parsing from client
    ####################

    # TODO Probably remove this. 'stop' will stop server
    if destAddr=='stop':
        print('STOPPING SERVER')
        s.close()
        break

    #########################
    # Check if destAddr is cashed ... - No.5 MS 
    addrCached = False
    for index in range(len(cache)): 
        if (cache[index]).lower()==destAddr.lower(): # The address is cashed!
            addrCached = True
            try: # Take cashed page and send to client
                f = open(destAddr+".webdoc",'r')
                cachedPage=f.read().encode(encoding='utf_8')
                clientSocket.sendall(cachedPage)
                f.close()
            except:
                f.close()
                print("Error sending cashed page")
                #addrCached = False # Cashing didn't work. Just re-connect TODO 
            break
    #########################
    if addrCached == False: # Not Cashed
        try: # python sockets is broken, and this is how I kinda fixed it. kinda
            #########################
            # Connecting to external server
            # Uses socketwrapper to connect to the destination server
            s2 = context.wrap_socket(socket.socket(socket.AF_INET), server_hostname=destAddr)
            s2.connect((destAddr, 443))
            s2.sendall(message)
            
            # Parses response header
            respdata = b''
            while True: 
                buf = s2.recv(1024)
                if not buf:
                    break
                respdata += buf
            response = respdata.decode('utf-8', 'ignore')
            # Prints the response
            print("RESPONSE HEADER FROM ORIGINAL SERVER")
            #Range is 10 as to not print the html data
            for x in range(10):
                print(response.split('\n')[x])
            print("END OF HEADER")
            # Adding to cache        
            if os.path.exists(destAddr+".webdoc"):
                os.remove(destAddr+".webdoc")
            f = open(destAddr+".webdoc",'a')
            f.write(response)
            f.close()
            cache.append(destAddr) # Adds the cached list

            # Close connection to webserver
            # s2.close()
            # Send webpage to client
            clientSocket.sendall(respdata)
            clientSocket.close()
        except:
            pass
#s.close()