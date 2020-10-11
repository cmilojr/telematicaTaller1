# Python TCP Client B
import socket
import tqdm


host = socket.gethostname()
port = 2004
BUFFER_SIZE = 2000
#MESSAGE = input("tcpClientB: Enter message/ Enter exit:")

tcpClientB = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try: 
    tcpClientB.connect((host, port))

    while True:#MESSAGE != 'exit':
        MESSAGE = input("tcpClientB: Enter message/ Enter exit:")
        tcpClientB.send(MESSAGE.encode())
        #data = tcpClientB.recv(BUFFER_SIZE)
        #print(" Client received data: "+data.decode(encoding="utf-8"))
        #MESSAGE = input("tcpClientB: Enter message to continue/ Enter exit:")

    tcpClientB.close()
except:
    print("Connection error to the server.")

