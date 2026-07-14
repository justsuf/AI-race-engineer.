import socket

PORT = 9996

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("0.0.0.0", PORT))

print("Listening on port", PORT)

while True:
    data, addr = sock.recvfrom(65535)

    print("Packet received!")
    print("From:", addr)
    print(data[:200])