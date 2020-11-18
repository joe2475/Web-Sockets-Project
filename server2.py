import socket 
import socketserver
import ssl
import os

###############################
# Host server
###############################
host = 'localhost'
#AF_INET is what corresponds with IPV4 and SOCK_STREAM is for TCP
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#Host name will be localhost and 1234 is the port number. Port will change just used it for testing purposes. 
s.bind((host, 50000))
#Que of 5 listens in case traffic becomes full
s.listen(5)
#print(socket.gethostname())

###############################
# getWebpage
# Connects to webpage, gets webdata and stores in current directory. 
# Will overwrite files
# TODO: Clean up, error handling, 
# TODO: GET images and ect.
# TODO: Possibly handle other requests other than GET
###############################
def getWebpage(hostName): #hostName is the address of the server
    # Creates SSL context with recommended security settings. Includes cert. verification
    context = ssl.create_default_context()

    # Connect to a server
    hostname='www.google.com'
    conn = context.wrap_socket(socket.socket(socket.AF_INET), server_hostname=hostname)
    conn.connect((hostname, 443))

    request=bytes("GET / HTTP/1.1\nHost: % s\r\n\r\n" % (hostname), 'utf-8')
    #request=bytes("HEAD / HTTP/1.1\nHost: % s\r\n\r\n" % (hostname), 'utf-8')

    conn.sendall(request)

    try:
        if os.path.exists(hostname+".webdoc"):
            os.remove(hostname+".webdoc")
        f = open(hostname+".webdoc",'a')
        conn.settimeout(1)#idk 100 seemed like a good number
        while True:
            data = conn.recv(1000)#.split(b"\r\n")
            if data:
                print(data) 
                f.write(data.decode('utf-8'))
            else:
                break
        conn.close()
        f.close()
        
    except:
        conn.close()
        print('hi')
        f.close()

    # This gets rid of the header
    try:
        if os.path.exists(hostname+".html"):
            os.remove(hostname+".html")
        f = open(hostname+".webdoc",'r')
        f2 = open(hostname+".html",'a')
        webline = f.readline()
        while webline:
            if webline.upper().find('<!DOCTYPE HTML>')>-1:
                break
            webline = f.readline()
        print (webline)
        while webline:
            f2.write(webline)
            webline = f.readline() 
        f.close()
        f2.close()
        os.remove(hostname+".webdoc")
    except:
        print('file error')
        f.close()
        f2.close()
    
    return

###############################
# Running Proxy
###############################
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
    
    getWebpage(destAddr)

    exit()
   # clientSocket.close()
 #   s.close()