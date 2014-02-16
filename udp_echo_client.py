import sys
import time
import socket

def usage():
    print('Usage: python udp_echo_client.py [-s <packetSize>] [-c <packetCount>] [-w <timeout>] [-l <localHost>] [-p <localPort>] <remoteHost> [<remotePort>]')

remoteHost = None
remotePort = None
packetSize = 56
packetCount = 4
timeout = 3000
localHost = '0.0.0.0'
localPort = 0

skipArg = False
for i in range(1, len(sys.argv)):
    if skipArg:
        skipArg = False
        continue
    if sys.argv[i] == '-s':
        packetSize = int(sys.argv[i + 1])
        skipArg = True
        continue
    if sys.argv[i] == '-c':
        packetCount = int(sys.argv[i + 1])
        skipArg = True
        continue
    if sys.argv[i] == '-w':
        timeout = int(sys.argv[i + 1])
        skipArg = True
        continue
    if sys.argv[i] == '-l':
        localHost = sys.argv[i + 1]
        skipArg = True
        continue
    if sys.argv[i] == '-p':
        localPort = int(sys.argv[i + 1])
        skipArg = True
        continue
    if remoteHost == None:
        remoteHost = sys.argv[i]
        continue
    if remotePort == None:
        remotePort = int(sys.argv[i])
        continue
    usage()
    raise Exception('Unknown parameter %s' % sys.argv[i])

if remoteHost == None:
    usage()
    sys.exit(1)
if remotePort == None:
    remotePort = 7

print('Ping %s:%d with %d bytes for %d count:' % (remoteHost, remotePort, packetSize, packetCount))

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)

s.bind((localHost, localPort))

s.settimeout(timeout / 1000.0)

buf = bytearray([b % 0x100 for b in range(0, packetSize)])

minLatency = 0x7fffffff
maxLatency = 0
allElapsedTime = 0
sentCount = 0
receivedCount = 0

try:
    for i in range(0, packetCount):
        beginTime = time.time()
        s.sendto(buf, 0, (remoteHost, remotePort))
        sentCount += 1
        try:
            data, addr = s.recvfrom(65536)
            elapsedTime = (time.time() - beginTime) * 1000
            if minLatency > elapsedTime:
                minLatency = elapsedTime
            if maxLatency < elapsedTime:
                maxLatency = elapsedTime
            allElapsedTime += elapsedTime
            receivedCount += 1
            print('Response from %s:%d: %d bytes, elapsedTime is %d' % (str(addr[0]), addr[1], len(data), int(elapsedTime)) + 'ms.')
            time.sleep(1 - elapsedTime / 1000)
        except socket.timeout:
            print('Request timed out.')
except KeyboardInterrupt:
    pass

print('')
if sentCount != 0:
    print('All sent: %d count, received: %d count, lost: %d count, lost rate: %d%%.' % (sentCount, receivedCount, sentCount - receivedCount, (sentCount - receivedCount) * 100 / sentCount))
if receivedCount != 0:
    print('min latency: ' + str(int(minLatency)) + 'ms, max latency: ' + str(int(maxLatency)) + 'ms, average lagenty: ' + str(int(allElapsedTime / receivedCount)) + 'ms.')
