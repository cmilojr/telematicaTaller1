# Python TCP Client B
import socket
import threading

host = socket.gethostname()
port = 2004
BUFFER_SIZE = 2000

MESSAGE = ""
tcpClientB = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
def work():
    try: 
        tcpClientB.connect((host, port))
        while True:#MESSAGE != 'exit':
            MESSAGE = input("Client: Enter code / Enter exit: ")
            if MESSAGE == 'SD':
                try:
                    nameOfFile = input("Enter name of file with extension: ")
                    #sendData(nameOfFile)
                    tcpClientB.send((MESSAGE+" "+nameOfFile).encode())
                    print("--------------sending...--------------")
                    #tcpClientB.send(nameOfFile.encode())
                    filename = nameOfFile

                    f = open(filename, 'rb')
                    while True:
                        l = f.read(BUFFER_SIZE)
                        print(f"value of L is: {l}")
                        while (l):
                            tcpClientB.send(l)
                            print('Sent ',repr(l))
                            l = f.read(BUFFER_SIZE)
                        if not l:
                            f.close()
                            tcpClientB.close()
                            break
                    print("Finished sending data")
                except:
                    print("Error sending data")
                    
            #MESSAGE = input("Enter code / Enter exit: ")
            #tcpClientB.send(MESSAGE.encode())

        tcpClientB.close()
    except:
        print("Connection error to the server.")

def sendData(nameOfFile):
    print("----------------------------")
    tcpClientB.send(MESSAGE.encode())
    filename = nameOfFile

    f = open(filename, 'rb')
    while True:
        l = f.read(BUFFER_SIZE)
        while (l):
            tcpClientB.send(l)
            print('Sent ',repr(l))
            l = f.read(BUFFER_SIZE)
        if not l:
            f.close()
            tcpClientB.close()
            break

n = threading.Thread(target=work)
n.start()