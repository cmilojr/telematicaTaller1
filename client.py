# Python TCP Client A
import socket

host = socket.gethostname()
port = 2004
BUFFER_SIZE = 2000


tcpClientA = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpClientA.connect((host, port))

while True: #MESSAGE != 'exit':
    MESSAGE = input("tcpClientA: Enter message/ Enter exit:")
    tcpClientA.send(MESSAGE.encode())
    # data = tcpClientA.recv(BUFFER_SIZE)
    # print(" Client2 received data: "+data.decode(encoding="utf-8"))
    # MESSAGE = input("tcpClientA: Enter message to continue/ Enter exit:")

tcpClientA.close()
