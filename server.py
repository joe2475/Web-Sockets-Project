import socket 
import socketserver

#####################
# Cache is a list of lists
# The first element of the inner list is the URL and the second is the data
#####################
cache = []
def cacheObject(destAddr, data): # - No.7 MS
    # v parsed before (or in the function - change params)
    temp = [destAddr, data]
    cache.append(temp)

host = 'localhost'
#AF_INET is what corresponds with IPV4 and SOCK_STREAM is for TCP
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
    
    # Check if destAddr is cashed ... - No.5 MS 
    addrCached = False
    for index in range(len(cache)): 
        if cache[index][0]:
            # The address is cashed!
            # TODO: Return info to client (No. 4?)
            addrCached = True
            break
    if addrCached == False: # Not in GET - No. 6
        # Not Cashed
        break # TODO: Request webpage from webserver, receive webdata, parse and add to cache. Also remove break
        # Then send data to client. This is a big part

    exit()
    # clientSocket.close()


#   s.close()