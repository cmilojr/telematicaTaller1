# Python TCP Client B
import os
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
            if MESSAGE.lower() == 'sd':
                try:
                    nameOfFile = input("Enter name of file with extension: ")
                    tcpClientB.send((MESSAGE+"<separator>"+nameOfFile).encode())
                    sendData(nameOfFile)
                except:
                    print("Error sending data")
            #MESSAGE = input("Enter code / Enter exit: ")
            #tcpClientB.send(MESSAGE.encode())
            elif MESSAGE.lower() == "rma":
                while True:
                    deleteName = input("enter name of file to delete or enter  \" back \" to back: ")
                    if deleteName.lower() == "back":
                        break
                    else:
                        tcpClientB.send((MESSAGE+"<separator>"+deleteName).encode())
                        msg = tcpClientB.recv(2000)
                        print(msg.decode())
            elif MESSAGE.lower() == "rmf":
                while True:
                    deleteName = input("enter name of file to delete or enter  \" back \" to  back: ")
                    if deleteName.lower() == "back":
                        break
                    else:
                        tcpClientB.send((MESSAGE+"<separator>"+deleteName).encode())
                        msg = tcpClientB.recv(2000)
                        print(msg.decode())
            elif MESSAGE.lower() == "list":
                tcpClientB.send(("basepath"+ "<separator>").encode())
                msg = tcpClientB.recv(80000)
                basePath = msg.decode()
                while True:
                    print("\n* current path = "+basePath)
                    pathName = input("* enter name of the folder\n* enter \".\" to list the files of the current folder\n* use \"..\" to exit the folder\n* enter  \"back\" to exit list\n-> ")
                    if pathName.lower() == "back":
                        break
                    else:
                        tcpClientB.send((MESSAGE  + "<separator>" + basePath + "<separator>" + pathName).encode())
                        path = tcpClientB.recv(80000).decode().split("@")
                        if (path[0].lower() == "error in the path, try again"):
                            print(f"\n{path[0]}".upper())
                            basePath = basePath
                        else:
                            msg = path[1]
                            basePath = path[0]
                            print(f"\nfiles: {msg}\n")
            elif MESSAGE.lower() == "nf":
                while True:
                    deleteName = input("enter name of folder to create  or enter  \" back \" to  back: ")
                    if deleteName.lower() == "back":
                        break
                    else:
                        tcpClientB.send((MESSAGE+"<separator>"+deleteName).encode())
                        msg = tcpClientB.recv(2000)
                        print(msg.decode())
            else:
                print("invalid code in list")
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
            #tcpClientB.close()
            break
    print("-----------Finished sending data-----------")

n = threading.Thread(target=work)
n.start()