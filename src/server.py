import socket
import sys
import os
class server:
    
    def __init__(self, port):
        self.__port = port

    def open(self, clientHandler):
        
        # opening the server socket that will listen to messages from the client
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
        # binding the socket to the server port
        s.bind(('', self.__port))

        # Listening to 5 clients
        s.listen(5)

        while True:
            clientHandler.handleRequest(s)

class clienthandler:

    def handleRequest(self, sock):
         # getting the message from the client
        client_socket, client_address = sock.accept()
        data = client_socket.recv(100).decode()
        print('Received: ', data)

        # sending message to client
        client_socket.send(data.upper())        
        client_socket.close()