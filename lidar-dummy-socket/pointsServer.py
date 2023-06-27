# Creates random points and prints them to the socket

import random
import time
import socket
import pickle
import threading


# create a random point array, index is angle and points[index] is distance
def createRandomPoint():
    points = [None] * 360
    # loop for points
    for i in range(0, 360):
        # create random distance
        distance = random.randint(0, 100)
        # add distance to points
        points[i] = distance
    return points


def send_points(port):
    # Create a TCP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to a specific address and port
    server_socket.bind(("0.0.0.0", port))
    print(f"Server listening on port {port}")

    # Listen for incoming connections
    server_socket.listen(1)

    while True:
        # Accept a client connection
        client_socket, client_address = server_socket.accept()
        print(f"Accepted connection from: {client_address}")

        while True:
            # create random points and write them to the socket
            point = createRandomPoint()
            client_socket.sendall(pickle.dumps(point))
            time.sleep(0.05)
        # close the socket
        client_socket.close()


points_port = 8080

print(f"Address: {socket.gethostbyname(socket.gethostname())}")

send_points = threading.Thread(target=send_points, args=(points_port,))
send_points.start()
