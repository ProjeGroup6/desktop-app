import os
import ydlidar
import time
import socket
import pickle

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# # Bind the socket to a specific address and port
server_address = ("0.0.0.0", 8888)
server_socket.bind(server_address)

# Listen for incoming connections
server_socket.listen(1)
print("Server is listening on {}:{}".format(*server_address))

# Accept a client connection
client_socket, client_address = server_socket.accept()
print("Connected to client:", client_address)

ydlidar.os_init()
ports = ydlidar.lidarPortList()
port = "/dev/ydlidar"
for key, value in ports.items():
    port = value
laser = ydlidar.CYdLidar()
laser.setlidaropt(ydlidar.LidarPropSerialPort, port)
laser.setlidaropt(ydlidar.LidarPropSerialBaudrate, 115200)
laser.setlidaropt(ydlidar.LidarPropLidarType, ydlidar.TYPE_TRIANGLE)
laser.setlidaropt(ydlidar.LidarPropDeviceType, ydlidar.YDLIDAR_TYPE_SERIAL)
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
    laser.turnOff()
laser.disconnecting()
