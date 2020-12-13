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
            #accepting a connection from a new client
            client_socket, client_address = s.accept()
            #handling the request of the client
            clientHandler.handleRequest(client_socket)

class clienthandler:

    __buffer_size = 1024

    def handleRequest(self, client_socket):

        keep_connected = True
        while keep_connected:
            #setting a 1 second timeout for the connection
            client_socket.settimeout(1)
            try:
                #getting the message from the client
                data = client_socket.recv(self.__buffer_size)
                #if the message is empty, then closing the connection
                if not data:
                    break
            #if the timeout limit has been over, then closing the connection
            # (if the timeout limit is over, then the client socket will be blocked, so calling to recv will throw an exception)
            except:
                break
            
            #getting the decoded message and printing it
            message = data.decode()
            print(message)

            #getting the file name
            file_name = message.split('GET /')[1].split(' HTTP')[0]
            if file_name == '':
                file_name = 'index.html'

            #getting the connection status
            tmp = message.find('Connection: ') + len('Connection: ')
            connection_status = message[tmp:message.find('\r\n', tmp)]

            #if the file name is 'redirect', the error code will be 301
            if file_name == 'redirect':
                #creating a log with error code 301
                log = clienthandler.create_log(301, '‫‪Moved‬‬ ‫‪Permanently‬‬', 'close', '')
                #in this case, the connection will be closed
                keep_connected = False
            #else, trying to open the file
            else:
                try:
                    #getting the correct open mode and opening the file
                    open_mode = 'rb' if file_name.endswith('ico') or file_name.endswith('jpg') else 'r'
                    f = open(file_name, open_mode)
                    #creating a log with error code 200, which contains the file content
                    log = clienthandler.create_log(200, 'OK', connection_status, f.read())
                    # in this case, the continue of the connection will be according to the connection status which appears in the message 
                    if connection_status == 'close':
                        keep_connected = False
                #if the file was not found, the error code will be 404
                except FileNotFoundError:
                    #creating a log with status 404
                    log = clienthandler.create_log(404, 'Not Found', 'close', '')
                    #in this case, the connection will be closed
                    keep_connected = False

            #sending the log to the client
            client_socket.send(log)

        #closing the connection with the client
        client_socket.close()

    @staticmethod
    def create_log(error_code, status, connection_status, content):

        log = 'HTTP/1.1‬‬ ' + str(error_code) + ' ' + status + '\r\n' + 'Connection: ' + connection_status + '\r\n'

        if error_code == 301:
            log += '‫‪Location:‬‬ ‫‪/result.html‬‬' + '\r\n'
        if error_code == 200 and content:
            log += '‫‪Content-Length:‬‬ ' + str(len(content)) + '\r\n'

        log += '\r\n'
        log = log.encode()

        if error_code == 200 and content:
            try:
                log += content.encode()
            except:
                log += content
                
        return log

#creating the server and the client handler with the command line arguments
server = server(int(sys.argv[1]))
clientHandler = clienthandler()
#opening the server with the client handler
server.open(clientHandler)