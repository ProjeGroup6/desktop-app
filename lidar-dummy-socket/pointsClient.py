# Read random points from socket and prints them

import socket
import threading
import pickle
import time


def receive_points(sock):
    while True:
        # read array
        data = sock.recv(1024)
        if not data:
            break
        point = pickle.loads(data)
        print(f"angle: {point[0]}")
        print(f"distance: {point[1]}")
        time.sleep(0.01)


def start_client(address, port_points):
    points_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    points_socket.connect((address, port_points))
    print("Connected to server for points.")

    # Start a separate thread to receive points
    receive_points_thread = threading.Thread(
        target=receive_points, args=(points_socket,)
    )

    receive_points_thread.start()

    # Wait for the threads to finish
    receive_points_thread.join()

    print("Client connection closed.")
    points_socket.close()


server_address = input("Enter server address: ")
points_port = 8080
start_client(server_address, points_port)
