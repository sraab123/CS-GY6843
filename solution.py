from socket import *
import os
import sys
import struct
import time
import select
import binascii
import pandas as pd

ICMP_ECHO_REQUEST = 8
MAX_HOPS = 30
TIMEOUT = 2.0
TRIES = 1
pd.options.display.width = 0

# The packet that we shall send to each router along the path is the ICMP echo
# request packet, which is exactly what we had used in the ICMP ping exercise.
# We shall use the same packet that we built in the Ping exercise

def checksum(string):
    csum = 0
    countTo = (len(string) // 2) * 2
    count = 0

    while count < countTo:
        thisVal = (string[count + 1]) * 256 + (string[count])
        csum += thisVal
        csum &= 0xffffffff
        count += 2

    if countTo < len(string):
        csum += (string[len(string) - 1])
        csum &= 0xffffffff

    csum = (csum >> 16) + (csum & 0xffff)
    csum = csum + (csum >> 16)
    answer = ~csum
    answer = answer & 0xffff
    answer = answer >> 8 | (answer << 8 & 0xff00)
    return answer


def build_packet():
    # Header is type (8), code (8), checksum (16), id (16), sequence (16)

    myChecksum = 0
    id = os.getpid() & 0xFFFF  # Return the current process i
    # Make a dummy header with a 0 checksum
    # struct -- Interpret strings as packed binary data
    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, id, 1)
    data = struct.pack("d", time.time())
    # Calculate the checksum on the data and the dummy header.
    myChecksum = checksum(header + data)

    # Get the right checksum, and put in the header

    if sys.platform == 'darwin':
        # Convert 16-bit integers from host to network  byte order
        myChecksum = htons(myChecksum) & 0xffff
    else:
        myChecksum = htons(myChecksum)

    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, id, 1)
    packet = header + data

    return packet

def get_route(hostname):
    timeLeft = TIMEOUT
    df = pd.DataFrame(columns=['Hop Count', 'Try', 'IP', 'Hostname', 'Response Code'])
    #print(df)
    for ttl in range(1,MAX_HOPS):
        for tries in range(TRIES):
            #print(hostname)
            #destAddr = gethostbyname(hostname)

            #Fill in start
            icmp = getprotobyname("icmp")
            mySocket = socket(AF_INET, SOCK_RAW, icmp)
            #Fill in end

            mySocket.setsockopt(IPPROTO_IP, IP_TTL, struct.pack('I', ttl))
            mySocket.settimeout(TIMEOUT)
            try:
                d = build_packet()
                mySocket.sendto(d, (hostname, 0))
                #t= time.time()
                startedSelect = time.time()
                whatReady = select.select([mySocket], [], [], timeLeft)
                howLongInSelect = (time.time() - startedSelect)
                if whatReady[0] == []: # Timeout
                    #Fill in start

                    #append response to your dataframe including hop #, try #, and "Timeout" responses as required by the acceptance criteria
                    row = {'Hop Count': str(ttl), 'Try': str(tries + 1), 'IP': 'timeout', 'Hostname': 'timeout', 'Response Code': 'timeout'}
                    new_df = pd.DataFrame([row])
                    df = pd.concat([df, new_df], axis=0, ignore_index=True)
                    #print(df)

                    #Fill in end
                recvPacket, addr = mySocket.recvfrom(1024)
                #timeReceived = time.time()
                timeLeft = timeLeft - howLongInSelect
                if timeLeft <= 0:
                    #Fill in start
                    row = {'Hop Count': str(ttl), 'Try': str(tries + 1), 'IP': 'timeout', 'Hostname': 'timeout', 'Response Code': 'timeout'}
                    new_df = pd.DataFrame([row])
                    df = pd.concat([df, new_df], axis=0, ignore_index=True)
                    #print (df)

                    #Fill in end
            except Exception as e:
                #print (e) # uncomment to view exceptions
                continue

            else:
                #Fill in start
                #Fetch the icmp type from the IP packet
                #TTL = struct.unpack_from("B", recvPacket, offset=8)
                #IP_numeric = struct.unpack_from("L", recvPacket, offset=12)
                bytes = struct.calcsize("L")
                #IP_numeric = struct.unpack("L", recvPacket[12:12 + bytes])[0]
                #print(recvPacket>>8)

                #IP_bytes = int.to_bytes(IP_numeric,4,"little")
                #print(len(IP_bytes))
                #IPAddr = inet_ntoa(IP_bytes)
                IPAddr = inet_ntoa(recvPacket[12:12 + bytes])
                #         ipBytes = len(recPacket)
                #         # Fetch the ICMP header from the IP packet
                icmpHeader = struct.unpack_from("bbHHh", recvPacket, offset=20)
                #         #b = char -> int Type, Code
                #         #H = unsigned short -> int Checksum, ID
                #         #h = short -> int Sequence
                icmpType = icmpHeader[0]
                #icmpCode = icmpHeader[1]
                #icmpChecksum = icmpHeader[2]
                #icmpID = icmpHeader[3]
                #icmpSeq = icmpHeader[4]
                #print("IP TTL: " + str(TTL[0]))
                #print("IP Addr: " + IPAddr)
                #print("ICMP Type: " + str(icmpType))
                #print("ICMP Code: " + str(icmpCode))
                #print("ICMP Checksum: " + str(icmpChecksum))
                #print("ICMP ID: " + str(icmpID))
                #print("ICMP Seq: " + str(icmpSeq))
                #print("RTT: " + str(round(timeReceived - startedSelect, 6)))

                #Fill in end
                try: #try to fetch the hostname
                    #Fill in start
                    hostname_ret = gethostbyaddr(IPAddr)
                    #Fill in end
                except herror:   #if the host does not provide a hostname
                    #Fill in start
                    hostname_ret = ['hostname not returnable',[],[]]
                    #Fill in end

                if icmpType == 11:
                    #bytes = struct.calcsize("d")
                    #timeSent = struct.unpack("d", recvPacket[28:28 + bytes])[0]
                    #Fill in start
                    #print('Hop Count:' + str(ttl))
                    #print('Try:' + str(tries))
                    #print('IP: ' + IPAddr)
                    #print('Hostname: ' + str(hostname_ret))
                    #print('Response: ' + str(icmpType))
                    row = {'Hop Count': str(ttl), 'Try': str(tries + 1), 'IP': IPAddr, 'Hostname': hostname_ret[0], 'Response Code':str(icmpType)}
                    new_df = pd.DataFrame([row])
                    df = pd.concat([df, new_df], axis=0, ignore_index=True)
                    #print(df)
                    #Fill in end
                elif icmpType == 3:
                    #bytes = struct.calcsize("d")
                    #timeSent = struct.unpack("d", recvPacket[28:28 + bytes])[0]
                    #Fill in start
                    #You should update your dataframe with the required column field responses here
                    row = {'Hop Count': str(ttl), 'Try': str(tries + 1), 'IP': IPAddr, 'Hostname': hostname_ret[0], 'Response Code': str(icmpType)}
                    new_df = pd.DataFrame([row])
                    df = pd.concat([df, new_df], axis=0, ignore_index=True)
                    #print(df)
                    #Fill in end
                elif icmpType == 0:
                    #bytes = struct.calcsize("d")
                    #timeSent = struct.unpack("d", recvPacket[28:28 + bytes])[0]
                    #Fill in start
                    #You should update your dataframe with the required column field responses here
                    row = {'Hop Count': str(ttl), 'Try': str(tries + 1), 'IP': IPAddr, 'Hostname': hostname_ret[0], 'Response Code': str(icmpType)}
                    new_df = pd.DataFrame([row])
                    df = pd.concat([df, new_df], axis=0, ignore_index=True)
                    #print(df)
                    return df
                     #Fill in end
                else:
                    #Fill in start
                    row = {'Hop Count': str(ttl), 'Try': str(tries + 1), 'IP': 'error', 'Hostname': 'error', 'Response Code': 'error'}
                    new_df = pd.DataFrame([row])
                    df = pd.concat([df, new_df], axis=0, ignore_index=True)
                    #Fill in end
                break
    return df

if __name__ == '__main__':
    get_route("google.co.il")