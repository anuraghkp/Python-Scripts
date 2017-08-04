import socket

host="127.0.0.1"
port=80
client=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
client.connect((host,port))
client.sendto("aaaaaaaaaaaacccccccccvvvvvvvvvv",(host,port));
data , responce=client.recvfrom(4096)
print responce
