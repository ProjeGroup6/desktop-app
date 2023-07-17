# from Control import *
import threading
import fcntl
import math
import socket

# Create an object of Control
# control = Control()
myX = 0
myY = 0
goX = 0
goY = 0
angle = 0.0
forwardZone = False
turnLeft = False
turnRight = False
# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
server_address = ("localhost", 12345)
client_socket.connect(server_address)
print("Connected to {}:{}".format(*server_address))


# Write a function to control the robot dog according to distance value
def move_robot():
    while True:
        if forwardZone == True:
            # control.forWard()
            print("ileri git")
            # Get user input
            message = "1"
            # Send the message to the server
            client_socket.sendall(message.encode())
        elif turnLeft == True:
            # control.turnLeft()
            message = "5"
            # Send the message to the server
            client_socket.sendall(message.encode())
            print("sola git")
        elif turnRight == True:
            # control.turnRight()
            message = "7"
            # Send the message to the server
            client_socket.sendall(message.encode())
            print("saga git")


def get_values():
    global myX, myY, goX, goY, angle
    while True:
        with open("/home/yusuf/path.txt", "r") as file:
            fcntl.flock(file.fileno(), fcntl.LOCK_SH)
            lines = file.readlines()
            myLoc = lines[0]
            destLoc = lines[4]
            myX, myY, angle = parser(myLoc)
            angle = float(angle) + 240.0
            angle = (180 / math.pi) * angle
            goX, goY, _ = parser(destLoc)
            fcntl.flock(file.fileno(), fcntl.LOCK_UN)


def calculate_slope(x1, y1, x2, y2):
    try:
        slope = (y2 - y1) / (x2 - x1)
        # Calculate the angle using the arctan function and convert to degrees
        angle_degrees = math.degrees(math.atan(slope))

        return angle_degrees
    except ZeroDivisionError:
        return -1


def decideDirection(direction):
    global forwardZone, turnLeft, turnRight
    if direction >= 340 and direction <= 360 or direction >= 0 and direction <= 20:
        print("düz git")
        forwardZone = True
        turnLeft = False
        turnRight = False
    elif direction >= 160 and direction <= 200:
        print("geri git")
        forwardZone = False
        turnLeft = False
        turnRight = True
    elif direction > 200 and direction < 340:
        print("sola dön")
        forwardZone = False
        turnLeft = True
        turnRight = False
    else:
        print("sağa dön")
        forwardZone = False
        turnLeft = False
        turnRight = True


def findDirection():
    while True:
        dx = int(goX) - int(myX)
        dy = int(goY) - int(myY)
        print(dx, dy)
        target_angle = (180 / math.pi) * math.atan2(dy, dx)
        print(target_angle)
        direction = (angle - target_angle) % 360
        print(direction)
        decideDirection(direction)


def parser(receivedData):
    try:
        array = receivedData.split(",")
        # print(array)
        if len(array) == 5:
            first = array[0]
            second = array[1]
            third = array[2]
            fourth = array[3]
            fifth = array[4]
        return first, second, fifth
    except:
        pass


if __name__ == "__main__":
    print("Start")

    # Make a thread to listen to the port
    t = threading.Thread(target=move_robot, args=())
    t1 = threading.Thread(target=get_values, args=())
    t2 = threading.Thread(target=findDirection, args=())

    t.start()
    t1.start()
    t2.start()

    t.join()
    t1.join()
    t2.join()

    print("End")
