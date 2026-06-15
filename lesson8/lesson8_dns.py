import socket

addr = socket.getaddrinfo("huggingface.co", 443, socket.AF_INET)
print(addr[0][4][0])