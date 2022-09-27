from socket import *


def smtp_client(port=1025, mailserver='127.0.0.1'):
    msg = {}
    msg[0] = "From: Alice <alice@xxx.org>"
    msg[1] = "\r\n To: Bob <bob@zzz.org>"
    msg[2] = "\r\n Date: Tue, 27 Sep 2022 18:02:43 -0500"
    msg[3] = "\r\n Subject: Hello World"
    msg[4] = "\r\n"
    msg[5] = "\r\n Dear Bob, "
    msg[6] = "\r\n    Hope all is well!"
    msg[7] = "\r\n         Regards, "
    msg[8] = "\r\n          Alice"
    endmsg = "\r\n.\r\n"

    # Choose a mail server (e.g. Google mail server) if you want to verify the script beyond GradeScope
    # mailserver=some.other.server.com
    try:
        # Create socket called clientSocket and establish a TCP connection with mailserver and port
        clientSocket = socket(AF_INET, SOCK_STREAM)
        clientSocket.connect((mailserver, port))
        recv = clientSocket.recv(1024).decode()

        # response from mail server to our connection request should be 220
        # print(recv)
        if recv[:3] != '220':
            #print('220 reply not received from server on socket open.')
            raise Exception("Mail Server Not Available")

        # Send HELO command and print server response.
        heloCommand = 'HELO mail.xxx.org\r\n'
        clientSocket.send(heloCommand.encode())
        recv1 = clientSocket.recv(1024).decode()

        #print(recv1)
        if recv1[:3] != '250':
            #print('250 reply not received from server.')
            raise Exception("Mail server did not reply to HELO with 250 response")

        # Send MAIL FROM command and handle server response.
        mailFrom = 'MAIL FROM: <alice@xxx.org>\r\n'
        clientSocket.send(mailFrom.encode())
        recv1 = clientSocket.recv(1024).decode()

        #print(recv1)
        if recv1[:3] != '250':
            #print('250 reply not received from server.')
            raise Exception("Mail server did not reply to MAIL FROM with 250 response")

        # Send RCPT TO command and handle server response.
        rcptTo = 'RCPT TO: <bob@zzz.org>\r\n'
        clientSocket.send(rcptTo.encode())
        recv1 = clientSocket.recv(1024).decode()

        #print(recv1)
        if recv1[:3] != '250':
            #print('250 reply not received from server.')
            raise Exception("Mail server did not reply to RCPT TO with 250 response")

        # Send DATA command and handle server response.
        dataMsg = 'DATA\r\n'
        clientSocket.send(dataMsg.encode())
        recv1 = clientSocket.recv(1024).decode()

        #print(recv1)
        if recv1[:3] != '354':
            #print('354 reply not received from server.')
            raise Exception("Mail server did not reply to DATA with 354 response")

        # Send main message body. Loop through each line in the msg array
        for i in msg:
            clientSocket.send(msg[i].encode())

        # Message ends with a single period, send message end and handle server response.
        clientSocket.send(endmsg.encode())
        recv1 = clientSocket.recv(1024).decode()

        #print(recv1)
        if recv1[:3] != '250':
            #print('250 reply not received from server.')
            raise Exception("Mail server did not reply to end of message body with 250 response")

        # Send QUIT command and handle server response.
        quitMsg = 'QUIT\r\n'
        clientSocket.send(quitMsg.encode())
        recv1 = clientSocket.recv(1024).decode()

        #print(recv1)
        if recv1[:3] != '221':
            #print('221 reply not received from server.')
            raise Exception("Mail server did not reply to QUIT with 221 response")

    except Exception as e:
        #print("Message Transmission stopped due to exception")
        #print(e.args)

if __name__ == '__main__':
    smtp_client(1025, '127.0.0.1')