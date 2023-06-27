import socket
import math
import pickle
import time

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
server_address = ("192.168.43.68", 8889)
client_socket.connect(server_address)
print("Connected to server:", server_address)
while True:
    file = open("points.txt", "w")
    try:
        data = client_socket.recv(4096)
        if not data:
            continue

        points = pickle.loads(data)
        for angle, distance in enumerate(points):
            if distance is not None and distance != 0:
                print("Angle:", angle, "Range:", distance)
                x = distance * math.cos(math.radians(angle))
                y = distance * math.sin(math.radians(angle))
                file.write(f"{x} {y} 0.0\n")
                # file.write(f"{angle}, {distance} 0.0\n")
    except Exception:
        pass
