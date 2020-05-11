UDP_IP = 10.0.0.21
UDP_PORT = 8998
MESSAGE = './ITGManager 10.0.0.21 -a 10.0.0.11 -W 100 4500 -w 1 900 -t 10000 -d 5000 -T tcp
print("UDP target IP:", UDP_IP)
print("UDP target port:", UDP_PORT)
print("message:", MESSAGE)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
sock.sendto(bytes(MESSAGE, "utf-8"), (UDP_IP, UDP_PORT))
