import socket
import threading
import time


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


def decrement_battery(battery):
    while True:
        if battery[0] > 10:
            battery[0] -= 1
        if battery[0] <= 10:
            battery[0] = 100
        time.sleep(1)


import cv2
import numpy as np
import socket
import time


def cameraSender():
    # Initialize the camera
    camera = cv2.VideoCapture(0)
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    # Create a socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = "127.0.0.1"  # Replace with the IP address of the receiver computer
    port = 9000  # Choose a suitable port number
    sock.connect((host, port))

    # Define the desired FPS (e.g., 10)
    desired_fps = 10
    delay = 1 / desired_fps

    while True:
        # Read a frame from the camera
        ret, frame = camera.read()

        # Encode the frame as JPEG
        _, encoded_frame = cv2.imencode(".jpg", frame)
        data = np.array(encoded_frame).tobytes()

        # Send the frame size and data
        sock.sendall(len(data).to_bytes(4, byteorder="big"))
        sock.sendall(data)

        # Pause for the desired amount of time to achieve the desired FPS
        time.sleep(delay)

        # Press 'q' to exit the program
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    # Cleanup
    camera.release()
    cv2.destroyAllWindows()
    sock.close()


def main():
    listen_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listen_sock.bind(("0.0.0.0", 8080))
    listen_sock.listen(3)

    battery = [100]

    while True:
        print("\nWaiting for a connection...\n")
        new_sock, address = listen_sock.accept()

        host, port = address
        print(f"Connected with {host}:{port}")

        # Start new threads to continuously send battery status updates and decrement battery value
        threading.Thread(target=send_battery_status, args=(new_sock, battery)).start()
        threading.Thread(target=decrement_battery, args=(battery,)).start()

        while True:
            message = receive_message(new_sock)
            if message is None:
                break

            print("MESSAGE:", message)
            if message == "12":
                threading.Thread(target=cameraSender).start()

        new_sock.close()

    listen_sock.close()


if __name__ == "__main__":
    main()
