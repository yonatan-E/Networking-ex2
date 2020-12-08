import socket
import sys
import datetime

class server:

    __backlog = 5
    
    def __init__(self, port):
        self.__port = port

    def open(self, clientHandler):
        #opening the server socket that will listen to messages from the client
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
        #binding the socket to the server port
        s.bind(('', self.__port))
        #defining the backlog of the socket
        s.listen(self.__backlog)

        while True:
            client_socket, client_address = s.accept()
            print('Connection from: ', client_address)
            clientHandler.handleRequest(client_socket)

class clienthandler:

    __buffer_size = 1024

    def handleRequest(self, client_socket):

        is_client_connected = True
        while is_client_connected:
            #getting the message from the client
            message = sock.recv(self.__buffer_size)
            message = data.decode()

            #getting the file name
            tmp = message.find(' ') + 1
            file_name = message[tmp:message.find(' ', tmp)]
            if file_name == '/':
                file_name = 'index.html'

            #getting the connection status
            ‫‪tmp = message.find('Connection: ') + 12
            connection_status = message[tmp:message.find(' ', tmp)]

            #getting the correct log
            if file_name == '‫‪/redirect‬‬':
                log = create_log(404, 'Not Found', 'close', ' ')
                is_client_connected = False
            try:
                f = open(file_name, 'r')
                log = create_log(200, 'OK', connection, f.read())
            except FileNotFoundError:
                log = create_log(301, '‫‪Moved‬‬ ‫‪Permanently‬‬', 'close', ' ')
                is_client_connected = False

            client_socket.send(log)

            if connection_status = 'close':
                is_client_connected = False

    @staticmethod
    def create_log(error_code, status, connection_status, content):

        log = '‫‪HTTP/1.1‬‬ ' + str(error_code) + ' ' + status + '\n' + 'Connection: ' + connection_status + '\n'

        if error_code == 301:
            log += '‫‪Location:‬‬ ‫‪/result.html‬‬\n'
        if content:
            log += '‫‪Content-Length:‬‬ ' + str(content.length())

        log += '\n\n'

        if content:
            log += content

        return log


#creating the server and the client handler with the command line arguments
server = server(int(sys.argv[1]))
clientHandler = clienthandler(filehandler(sys.argv[4]), sys.argv[2], int(sys.argv[3]))
#opening the server with the client handler
server.open(clientHandler)
