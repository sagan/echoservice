import sys
import socket

def usage():
    print('Usage: python udp_echo_client.py [-l <localHost>] [-p <localPort>]')

localHost = '0.0.0.0'
localPort = 7

skipArg = False
for i in range(1, len(sys.argv)):
    if skipArg:
        skipArg = False
        continue
    if sys.argv[i] == '-l':
        localHost = sys.argv[i + 1]
        skipArg = True
        continue
    if sys.argv[i] == '-p':
        localPort = int(sys.argv[i + 1])
        skipArg = True
        continue
    usage()
    raise Exception('Unknown parameter %s' % sys.argv[i])

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)

s.bind((localHost, localPort))

while True:
    data, addr = s.recvfrom(65536)
    s.sendto(data, 0, addr)
