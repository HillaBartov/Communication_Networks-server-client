import socket

file = open("ips.txt", "r")
ips = file.readlines()

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('', 54321))

while True:
    data, addr = s.recvfrom(1024)
    url = data
    for line in ips:
        if line.find(data.decode("utf-8")) != -1:
            s.sendto(line.encode(), addr)
