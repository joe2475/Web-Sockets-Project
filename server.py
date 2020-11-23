import socket 
import socketserver
import urllib.request
import ssl
import os

# Cache is a list 
cache = []
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
    # Waits for client input, then accepts input
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
    for x in range(len(data)):
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
    
    dest = 'Host: ' + destAddr + ':80\r\n'
    server_address = (destAddr, 80)
    destination = ('Host: ' + destAddr + ':80\r\n')
    message  = b'GET / HTTP/1.1\r\n'
    message += bytes(dest, encoding='utf-8')
    message += b'Connection: close\r\n'
    message += b'\r\n'
    print("END OF MESSAGE SENT TO ORIGINAL SERVER")
    # End of request parsing

    # Check if destAddr is cashed ... - No.5 MS 
    addrCached = False
    for index in range(len(cache)): 
        if cache[index][0]:
            # The address is cashed!
            # TODO: Return info to client (No. 4?)
            # It will be stored in CD
            addrCached = True
            break
    if addrCached == False: # Not Cashed
        # Connecting to external server
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
        '''
        try: # Add to cache
            if os.path.exists(destAddr+".html"): # removes file is it exists
                os.remove(destAddr+".html")
            f = open(destAddr+".html",'w')
            cache.append(destAddr) # adding to the cache data structure
            print(respdata)
            f.write(respdata.decode('utf-8'))
            f.close()
        except:
            print('file error')
            f.close()

        '''
        '''
        print(response)
        if os.path.exists(destAddr+".html"): # removes file is it exists
            os.remove(destAddr+".html")
        f = open(destAddr+".html",'w')
        cache.append(destAddr) # adding to the cache data structure
        f.write(response) #.decode('windows-1252'))
        f.close()
        '''
        try: # writes webpage to file
            if os.path.exists(destAddr+".webdoc"):
                os.remove(destAddr+".webdoc")
            f = open(destAddr+".webdoc",'a')
            f.write(response)
            f.close()
        
        except:
            f.close()

        # This gets rid of the header
        try:
            if os.path.exists(destAddr+".html"):
                os.remove(destAddr+".html")
            f = open(destAddr+".webdoc",'r')
            f2 = open(destAddr+".html",'a')
            cache.append(destAddr) # adding to the cache
            webline = f.readline()
            while webline:
                if webline.upper().find('<!DOCTYPE HTML>')>-1: # TODO: add more HTML start tags
                    #print("HTML")
                    break
                webline = f.readline()
            #print (webline)
            htmlFlag=True
            while webline:
                if htmlFlag == True:
                    if webline.upper().find('<\HTML>')>-1: 
                        htmlFlag=False
                    #if TODO add getting images and ect? Recursion?? AAK
                f2.write(webline)
                webline = f.readline() 
            f.close()
            f2.close()
            #os.remove(hostname+".webdoc")
        except:
            print('file error')
            f.close()
            f2.close()

        # print(temp)
        s2.close()
        clientSocket.sendall(respdata)
        clientSocket.close()
        #exit()
        #s.close()
        break
s.close()