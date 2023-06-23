import socket
import threading
import time
import cv2
import numpy as np


def receive_battery_status(sock):
    while True:
        data = sock.recv(1024).decode()
        if data.startswith("B"):
            battery = int(data[1:])
            print("Battery status:", battery)
        else:
            print("Invalid message received.")


def receive_frames(sock):
    while True:
        # Receive the frame size
        size_bytes = sock.recv(4)
        if not size_bytes:
            break
        frame_size = int.from_bytes(size_bytes, byteorder="big")

        # Receive the frame data
        data = b""
        while len(data) < frame_size:
            packet = sock.recv(frame_size - len(data))
            if not packet:
                break
            data += packet

        # Convert the received data back to an image
        frame = np.frombuffer(data, dtype=np.uint8)
        frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)

        # Display the received frame
        cv2.imshow("Received Frame", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cv2.destroyAllWindows()


def start_client(address, port_message, port_camera):
    # Connect to the server for message exchange
    message_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    message_socket.connect((address, port_message))
    print("Connected to server for messages.")

    # Start a separate thread to receive battery status
    receive_battery_thread = threading.Thread(
        target=receive_battery_status, args=(message_socket,)
    )
    receive_battery_thread.start()

    # Connect to the server for receiving camera frames
    camera_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    camera_socket.connect((address, port_camera))
    print("Connected to server for camera frames.")

    # Start a separate thread to receive camera frames
    receive_frames_thread = threading.Thread(
        target=receive_frames, args=(camera_socket,)
    )
    receive_frames_thread.start()

    # Wait for the threads to finish
    receive_battery_thread.join()
    receive_frames_thread.join()

    print("Client connection closed.")


# Specify the server address and ports
server_address = "localhost"
message_port = 8001
camera_port = 9001

# Start the client
start_client(server_address, message_port, camera_port)
