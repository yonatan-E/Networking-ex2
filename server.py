import socket
import sys

class server:

    __backlog = 5
    
    def __init__(self, port):
        self.__port = port

    def open(self, clientHandler):
        #opening the server socket that will listen to messages from the client
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
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
            data = client_socket.recv(self.__buffer_size)
            message = data.decode()

            #getting the file name
            file_name = message.split('GET /')[1].split(' HTTP')[0]
            if file_name == '/':
                file_name = 'index.html'

            #getting the connection status
            tmp = message.find('Connection: ') + len('Connection: ')
            connection_status = message[tmp:message.find('\r\n', tmp)]

            #getting the correct log
            #if the file name is /redirect, the error code will be 301
            if file_name == '‫‪redirect‬‬':
                log = clientHandler.create_log(301, '‫‪Moved‬‬ ‫‪Permanently‬‬', 'close', '')
                is_client_connected = False
            #else, trying to open the file
            else:
                try:
                    #getting the correct open mode
                    open_mode = 'rb' if file_name.endswith('ico') or file_name.endswith('jpeg') else 'r'
                    f = open(file_name, open_mode)
                    content = f.read()

                    #if the message is empty, then closing the connection with the client
                    if not content:
                        break

                    log = clientHandler.create_log(200, 'OK', connection_status, content)
                #if the file was not found, the error code will be 404
                except FileNotFoundError:
                    log = clientHandler.create_log(404, 'Not Found', 'close', '')
                    is_client_connected = False

            client_socket.send(log.encode())

            if connection_status == 'close':
                is_client_connected = False

        client_socket.close()

    @staticmethod
    def create_log(error_code, status, connection_status, content):

        log = 'HTTP/1.1‬‬ ' + str(error_code) + ' ' + status + '\r\n' + 'Connection: ' + connection_status + '\r\n'

        if error_code == 301:
            log += '‫‪Location:‬‬ ‫‪/result.html‬‬'
        if error_code == 200 and content:
            log += '‫‪Content-Length:‬‬ ' + str(len(content))

        log += '\r\n\r\n'

        if error_code == 200 and content:
            log += str(content)

        return log

#creating the server and the client handler with the command line arguments
server = server(int(sys.argv[1]))
clientHandler = clienthandler()
#opening the server with the client handler
server.open(clientHandler)

