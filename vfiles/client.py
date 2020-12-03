import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect(('192.168.68.107', 12345))

s.send(b'ilan prais yonatan ehrenriech')

data = s.recv(100)
print("Server sent: ", data)

s.close()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect(('192.168.68.107', 12345))

s.send(b'329034557 213192875')

data = s.recv(100)
print("Server sent: ", data)

s.close()
