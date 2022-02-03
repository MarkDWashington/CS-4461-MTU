import socket, sys

if len(sys.argv) < 2:
    exit()

ip = sys.argv[1]

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.sendto("qotd".encode(), (ip, 9876))
data, addr = s.recvfrom(1024)
print(data)