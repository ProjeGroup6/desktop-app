import cv2
import numpy as np
import socket
import time

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
