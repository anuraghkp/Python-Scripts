import socket

host="127.0.0.1"
port=80
client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect((host,port))
client.send("GET /  HTTP/1.1\r\nHost:127.0.0.1\r\n\r\n");
responce=client.recv(4096)
print(responce)
