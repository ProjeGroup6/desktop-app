# The code that we inspired while writing controlServer.

import socket
import threading
import time
import cv2
import numpy as np
import random
import pickle


def start_message(port):
    def receive_message(sock):
        buffer_size = 4096
        data = sock.recv(buffer_size)
        if not data:
            return None
        return data.decode()

    def send_battery_status(new_sock, battery):
        while True:
            new_sock.send(f"B{battery[0]}".encode())
            time.sleep(1)

    def get_battery(battery):
        # burada kutuphaneden batarya okunup array seklinde yollanacak
        while True:
            if battery[0] > 10:
                battery[0] -= 1
            if battery[0] <= 10:
                battery[0] = 100
            time.sleep(1)

    # Create a TCP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to a specific address and port
    server_socket.bind(("0.0.0.0", port))

    # Listen for incoming connections
    server_socket.listen(1)
    print(f"Server listening on port {port}")

    while True:
        # Accept a client connection
        client_socket, client_address = server_socket.accept()
        print(f"Accepted connection from: {client_address}")

        battery = [100]

        # Start new threads to continuously send battery status updates and decrement battery value
        threading.Thread(
            target=send_battery_status, args=(client_socket, battery)
        ).start()
        threading.Thread(target=get_battery, args=(battery,)).start()

        while True:
            message = receive_message(client_socket)
            if message is None:
                break

            print("MESSAGE:", message)

        client_socket.close()


def send_camera(port):
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

        # reads frame from the camera and send frames over port
        camera = cv2.VideoCapture(0)
        desired_fps = 10
        delay = 1 / desired_fps

        while True:
            # Read a frame from the camera
            ret, frame = camera.read()

            # Encode the frame as JPEG
            _, encoded_frame = cv2.imencode(".jpg", frame)
            data = np.array(encoded_frame).tobytes()

            # Send the frame size and data
            client_socket.sendall(len(data).to_bytes(4, byteorder="big"))
            client_socket.sendall(data)

            # Pause for the desired amount of time to achieve the desired FPS
            time.sleep(delay)

            # Press 'q' to exit the program
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        # Cleanup
        camera.release()
        cv2.destroyAllWindows()

        # Close the client socket
        client_socket.close()


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
            time.sleep(0.01)
        # close the socket
        client_socket.close()


# Start servers on two different ports
server_port = 8000
camera_port = 9000
map_port = 9595

print(f"Address: {socket.gethostbyname(socket.gethostname())}")

start_message = threading.Thread(target=start_message, args=(server_port,))
start_message.start()

send_camera = threading.Thread(target=send_camera, args=(camera_port,))
send_camera.start()

send_points = threading.Thread(target=send_points, args=(map_port,))
send_points.start()
