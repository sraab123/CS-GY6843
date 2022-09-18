# import socket module
from socket import *
# In order to terminate the program
import sys


def webServer(port=13331):
    serverSocket = socket(AF_INET, SOCK_STREAM)

    # Prepare a server socket
    serverSocket.bind(("", port))

    # Fill in start
    serverSocket.listen()
    # Fill in end

    while True:
        # Establish the connection

        print('Ready to serve...')
        connectionSocket, addr = serverSocket.accept()  # Fill in start -are you accepting connections?     #Fill in end

        try:
            message = connectionSocket.recv(1024)
            #print(message)
            filename = message.split()[1]
            #print(filename[1:])

            # opens the client requested file.
            # Plenty of guidance online on how to open and read a file in python. How should you read it though if you plan on sending it through a socket?
            f = open(filename[1:].decode())
            outputfile = f.read()
            f.close()

            outputdata = "HTTP/1.1 200 OK\r\n" \
                         + "Content-Type: text/html; charset=UTF-8\r\n\n" \
                         + outputfile

            # for i in f:  # for line in file

        except Exception as e:
            outputdata = "HTTP/1.1 404 Not Found\r\n"
            #print(e)

        finally:
            #print(outputdata)
            connectionSocket.send(outputdata.encode(encoding="UTF-8"))
            connectionSocket.close()  # closing the connection socket

    # Close client socket
    serverSocket.close()
    sys.exit()  # Terminate the program after sending the corresponding data


if __name__ == "__main__":
    webServer(13331)
