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
            if MESSAGE.lower() == "exit":
                break
            if MESSAGE == 'SD':
                try:
                    nameOfFile = input("Enter name of file with extension: ")
                    tcpClientB.send((MESSAGE+" "+nameOfFile).encode())
                    sendData(nameOfFile)
                except:
                    print("Error sending data")
            #MESSAGE = input("Enter code / Enter exit: ")
            #tcpClientB.send(MESSAGE.encode())
            elif MESSAGE.lower() == "rma":
                while True:
                    deleteName = input("enter name of file to delete or enter  \" exit \" of back: ")
                    if deleteName.lower() == "back":
                        break
                    else:
                        tcpClientB.send((MESSAGE+" "+deleteName).encode())
                        msg = tcpClientB.recv(2000)
                        print(msg.decode())
            elif MESSAGE.lower() == "rmf":
                while True:
                    deleteName = input("enter name of file to delete or enter  \" exit \" of back: ")
                    if deleteName.lower() == "back":
                        break
                    else:
                        tcpClientB.send((MESSAGE+" "+deleteName).encode())
                        msg = tcpClientB.recv(2000)
                        print(msg.decode())
        tcpClientB.close()
        print("connection end")
    except:
        print("Connection error to the server.")

def sendData(nameOfFile):
    print("--------------Sending...--------------")
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
    print("-----------Finished sending data-----------")

n = threading.Thread(target=work)
n.start()