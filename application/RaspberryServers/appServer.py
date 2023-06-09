import socket
import threading
import time
import cv2
import numpy as np
import ydlidar
import pickle
from Control import *
from Buzzer import *

is_send_lidar = False


def start_message(port):
    global is_send_lidar

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

    control = Control()
    buzzer = Buzzer()

    while True:
        # Accept a client connection
        client_socket, client_address = server_socket.accept()
        print(f"Accepted connection from: {client_address}")

        battery = [1]

        # Start new threads to continuously send battery status updates and decrement battery value
        threading.Thread(
            target=send_battery_status, args=(client_socket, battery)
        ).start()
        threading.Thread(target=get_battery, args=(battery,)).start()

        while True:
            message = receive_message(client_socket)
            if message is None:
                break

            if message == "1":
                control.forWard()
            elif message == "3":
                control.backWard()
            elif message == "4":
                control.setpLeft()
            elif message == "6":
                control.setpRight()
            elif message == "5":
                control.turnLeft()
            elif message == "7":
                control.turnRight()
            elif message == "2":
                buzzer.run("1")
                time.sleep(0.5)
                buzzer.run("0")
            elif message == "8":
                is_send_lidar = not is_send_lidar
            elif message == "9":
                print("balance")

        client_socket.close()


def send_camera(port):
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


def send_lidar(port):
    # Create a TCP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to a specific address and port
    server_socket.bind(("0.0.0.0", port))

    # Listen for incoming connections
    server_socket.listen(1)
    print(f"Server listening on port {port}")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Accepted connection from: {client_address}")
        while True:
            if is_send_lidar:
                ydlidar.os_init()
                ports = ydlidar.lidarPortList()
                port = "/dev/ydlidar"
                for key, value in ports.items():
                    port = value
                laser = ydlidar.CYdLidar()
                laser.setlidaropt(ydlidar.LidarPropSerialPort, port)
                laser.setlidaropt(ydlidar.LidarPropSerialBaudrate, 115200)
                laser.setlidaropt(ydlidar.LidarPropLidarType, ydlidar.TYPE_TRIANGLE)
                laser.setlidaropt(
                    ydlidar.LidarPropDeviceType, ydlidar.YDLIDAR_TYPE_SERIAL
                )
                laser.setlidaropt(ydlidar.LidarPropScanFrequency, 4.0)
                laser.setlidaropt(ydlidar.LidarPropSampleRate, 3)
                laser.setlidaropt(ydlidar.LidarPropSingleChannel, True)
                points = [None] * 360
                ret = laser.initialize()
                if ret:
                    ret = laser.turnOn()
                    scan = ydlidar.LaserScan()
                    while ret and ydlidar.os_isOk():
                        r = laser.doProcessSimple(scan)
                        if r:
                            for point in scan.points:
                                angle = int((point.angle * 180 / 3.14 + 360) % 360)
                                distance = point.range
                                print("angle:", angle, " range: ", point.range)
                                points[angle] = distance
                            print(points)
                            client_socket.sendall(pickle.dumps(points))
                        else:
                            print("Failed to get Lidar Data")
                        time.sleep(0.05)
                        if not is_send_lidar:
                            break
                    laser.turnOff()
                laser.disconnecting()
            else:
                time.sleep(1)


# Start servers on two different ports
server_port = 8000
camera_port = 9000
lidar_port = 8080

print(f"Address: {socket.gethostbyname(socket.gethostname())}")

start_message = threading.Thread(target=start_message, args=(server_port,))
start_message.start()

send_camera = threading.Thread(target=send_camera, args=(camera_port,))
send_camera.start()

send_lidar = threading.Thread(target=send_lidar, args=(lidar_port,))
send_lidar.start()

start_message.join()
send_camera.join()
send_lidar.join()
