from __future__ import print_function
from socket import *
from select import select

timeout = 5

#start the server with a certain behavior
def runServer(behavior,serverPort):

    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    serverSocket.bind(('', serverPort))
    serverSocket.listen(1)
    print ('The server is ready to receive')
    eventSourceList = [serverSocket]

    try:
        while 1:
#to do: set time out message
            (readList, writeList, errorList)   = select(eventSourceList, [], [], timeout)
            for descriptor in readList:
                # if the event was generated by a new connection
                if descriptor == serverSocket:
                    connectionSocket, addr = serverSocket.accept()
                    eventSourceList.append(connectionSocket)
                    print ('New connection ',addr)
                    
                #data received on an existing connection
                else:
                    connectionSocket = descriptor
                    print(connectionSocket.getpeername())
                    data = connectionSocket.recv(1024)
                    
                    # if the event was generated by data received
                    if data != '':
                        response = behavior(data)
                        connectionSocket.send(response)
                        
                    # if the event was generated by connection closed
                    else:
                        print ('Closing connection socket')
                        #another print to make it look nicer in the Shell
                        print ()
                        connectionSocket.close()
                        eventSourceList.remove(connectionSocket)
    finally:
        serverSocket.close()
