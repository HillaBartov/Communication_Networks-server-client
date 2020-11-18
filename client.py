import socket
import sys
server_ip, server_port = sys.argv[1], sys.argv[2]
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
while 1:
    url = input()
    s.sendto(url.encode(), (server_ip, int(server_port)))
    data, addr = s.recvfrom(1024)
    line = data.decode("utf-8")
    index = line.find(',') + 1
    line = line[index:]
    index = line.find(',')
    line = line[:index]
    print(line)

