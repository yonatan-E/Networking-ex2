import socket
import sys
import os
class server:
    
    def __init__(self, port):
        self.__port = port

    def open(self, clientHandler):
        
        # opening the server socket that will listen to messages from the client
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        # binding the socket to the server port
        s.bind(('', self.__port))

        # Listening to 5 clients
        s.listen(5)

        while True:
            clientHandler.handleRequest(s)

class clienthandler:

    def __init__(self, parser):
        self._parser = parser

    def handleRequest(self, sock):
         # getting the message from the client
        client_socket, client_address = sock.accept()
        data = client_socket.recv(100).decode()
        print('Received: ', data)

        name = self._parser.parse(data)[0]
        file = open(name, "r")
        print(name)
        lines = file.readlines()
        result = ""
        for line in lines:
            result += line + "\r\n"
        result = "HTTP/1.1 200 OK\r\nConnection: close\r\nContent-Length:" + str(len(result)) + "\r\n\r\n" + result

        # sending message to client
        client_socket.send(result.encode())        
        client_socket.close()

class requestParser:

    def parse(self, request):
        fileName = None
        connectionType = None
        lines = request.split("\r\n")
        fileName = lines[0].split("GET ")[1].split(" HTTP")[0]
        rest = lines[1:]
        for line in rest:
            if len(line.split(": ")) < 2:
                continue
            name = line.split(": ")[0]
            content = line.split(": ")[1]
            if name == "Connection":
                connectionType = content
        if fileName == "/":
            fileName = "index.html"
        return [fileName, connectionType]

#creating the server and the client handler with the command line arguments
server = server(int(sys.argv[1]))
parser = requestParser()
clientHandler = clienthandler(parser)
#opening the server with the client handler
server.open(clientHandler)