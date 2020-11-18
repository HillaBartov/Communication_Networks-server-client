import socket
import sys
from datetime import datetime as clock, timedelta


def ttl_check():
    lines_to_keep = []
    ips_file = open(ips_path, "r")
    address = ips_file.readlines()
    ips_file.close()

    for l in address:
        # cut time to die from line
        index = l.rfind('#') + 1
        if index > 0:
            ttl_to_check = l[index:]
            ttl_time_object = clock.strptime(ttl_to_check, '%H:%M:%S').time()
            now = clock.now().replace(microsecond=0).time()
            if now < ttl_time_object:
                # Add line to keep list- time not passed
                lines_to_keep.append(l)
        else:
            lines_to_keep.append(l)

    ips_file = open(ips_path, "w")
    for lin in lines_to_keep:
        ips_file.write(lin)
    ips_file.close()


# start_time = clock.now().time()
my_port, parent_ip, parent_port, ips_path = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('', int(my_port)))
# In case of program shutdown- check for existing dynamic records
ttl_check()
file = open(ips_path, "a")
file.write("\n")
file.close()

while True:
    # Checks for expired TTLs
    data_client, addr_client = s.recvfrom(1024)
    ttl_check()
    file = open(ips_path, "r")
    ips = file.readlines()
    file.close()
    answer = 0
    # Search url in ips file
    for line in ips:
        # Found in ips
        if line.find(data_client.decode("utf-8")) != -1:
            # remove trailing time stamp
            time_index = line.find("#")
            if time_index != -1:
                line = line[:time_index]
            # encode answer txt to byte
            answer = line.encode()
            break
    # Forward client request to parent server
    if not answer:
        s.sendto(data_client, (parent_ip, int(parent_port)))
        answer, addr = s.recvfrom(1024)
        answer_as_string = answer.decode("utf-8")
        file = open(ips_path, "a")
        file.write(answer_as_string)
        ttl_index = answer_as_string.rfind(',') + 1
        ttl = answer_as_string[ttl_index:]
        current_time = clock.now().replace(microsecond=0)
        time_to_die = (current_time + timedelta(seconds=float(ttl))).time()
        # Add time stamp
        file.write("#" + str(time_to_die))
        file.close()
    # Send answer to client (servers or parents servers)
    s.sendto(answer, addr_client)
