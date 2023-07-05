import os
import ydlidar
import time
import sys
from matplotlib.patches import Arc
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import socket
import pickle
import math

RMAX = 32.0

fig = plt.figure()
# fig.canvas.set_window_title("YDLidar LIDAR Monitor")

coordinates = {}

address = sys.argv[1]
port = int(sys.argv[2])

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((address, port))
print("Connected to server for points.")


# Handle point clicks
def handle_click(event):
    if event.button == 1:  # Left mouse button
        clicked_point = (event.xdata, event.ydata)
        print("Clicked point:", clicked_point)


fig.canvas.mpl_connect("button_press_event", handle_click)


def animate(num):
    data = sock.recv(1024)
    if data:
        points = pickle.loads(data)

        angle = []
        x_coordinates = []
        y_coordinates = []

        ran = []
        for i in range(0, 360):
            # angle.append(i)
            # ran.append(points[i])
            x_coordinates.append(points[i] * math.cos(math.radians(i)))
            y_coordinates.append(points[i] * math.sin(math.radians(i)))
            # intensity.append(point.intensity)
        # lidar_polar.scatter(angle, ran, c=intensity, cmap="hsv", alpha=0.95)
        plt.scatter(x_coordinates, y_coordinates, alpha=0.95, color="red", s=10)


ani = animation.FuncAnimation(fig, animate, interval=50)
plt.show()
plt.close()
