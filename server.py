import socket
import sys
import datetime

class server:
    
    def __init__(self, port):
        self.__port = port

    def open(self, clientHandler):
        #initializing the client handler
        clientHandler.initializeDomainsMap()
        
        #opening the server socket that will listen to messages from the client
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
        #binding the socket to the server port
        s.bind(('', self.__port))

        while True:
            clientHandler.handleRequest(s)

class clienthandler:

    def __init__(self, fileHandler, parentServerIP, parentServerPort):
        self.__domainsMap = {}
        self.__fileHandler = fileHandler
        self.__parentServerIP = parentServerIP
        self.__parentServerPort = parentServerPort

    def handleRequest(self, sock):
         #getting the message from the client
        data, addr = sock.recvfrom(1024)
        data = data.decode()
        
        #trying to remove domains that their ttl has expired
        remove = []
        for d in self.__domainsMap:
            startTime = self.__domainsMap[d][2] 
            ttl = self.__domainsMap[d][1]
            if ((datetime.datetime.now() - datetime.datetime(2020, 11, 11)).total_seconds() - startTime > ttl):
                remove.append(d)
                self.__fileHandler.removeLine(d)
        for rem in remove:
            del self.__domainsMap[rem]
        
        result = ''
        #checking if the given domain exists in the server
        if data in self.__domainsMap:
            result = data + ','
            for prop in self.__domainsMap[data][0:-1]:
                result += str(prop) + ','
            result = result[0:-1]
        #if the given domain doesn't exist in the server, then sending the request to the parent server
        elif self.__parentServerIP != '-1' and self.__parentServerPort != -1:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.sendto(data.encode(), (self.__parentServerIP, self.__parentServerPort))
            result2, addr2 = s.recvfrom(1024)
            resList = result2.decode().split(',')
            self.__domainsMap[data] = [resList[1], float(resList[2]), (datetime.datetime.now() - datetime.datetime(2020, 11, 11)).total_seconds()]
            self.__fileHandler.addLine(data + ',' + resList[1] + ',' + resList[2] + ',' + str(self.__domainsMap[data][2]))
            result = result2.decode()
        #sending the result to the client
        sock.sendto(result.encode(), addr)

    def initializeDomainsMap(self):
        updatedLines = []
        lines = self.__fileHandler.getLines()
        #for every domain, checking if its line contains the time when the domain was added to the server.
        #if it doesn't, then initializing this time to the current time
        for line in lines:
            properties = line.split(',')
            properties.append((datetime.datetime.now() - datetime.datetime(2020, 11, 11)).total_seconds())
            properties = (properties[0], properties[1], int(properties[2]), float(properties[3]))
            self.__domainsMap[properties[0]] = properties[1:]
            updatedLines.append(properties[0] + ',' + properties[1] + ',' + str(properties[2]) + ',' + str(properties[3]))

        self.__fileHandler.replaceAllLines(updatedLines)
        
class filehandler:

    def __init__(self, fileName):
        self.__fileName = fileName

    def addLine(self, line):
        with open(self.__fileName, "a+") as f:
            f.write(line + "\n")

    def removeLine(self, prefix):
        lines = self.getLines()
        with open(self.__fileName, 'w') as file:
            for line in lines:
                if (line.startswith(prefix) == False):
                    file.write(line)

    def getLines(self):
        try:
            f = open(self.__fileName, "r")
        except:
            f = open(self.__fileName, "w+")

        lines = f.readlines()
        f.close()
        return lines

    def replaceAllLines(self, newLines):
        with open(self.__fileName, "w+") as f:
            for line in newLines:
                f.write(line + '\n')

#creating the server and the client handler with the command line arguments
server = server(int(sys.argv[1]))
clientHandler = clienthandler(filehandler(sys.argv[4]), sys.argv[2], int(sys.argv[3]))
#opening the server with the client handler
server.open(clientHandler)
