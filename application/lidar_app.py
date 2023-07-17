import sys
import socket
import numpy as np
import pyqtgraph as pg
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from pyqtgraph import ScatterPlotItem
import fcntl

port = 8080
added_points = set()
scatter = None
plot_widget = None
mapfile = "map.txt"
transfile = "transform.txt"
goal = "goal.txt"


def read_points():
    global mapfile, transfile
    # the map file is in following format
    # x1,y1
    # x2, y2
    # ....
    # xn, yn

    # read file
    # data = np.loadtxt(mapfile, dtype=np.uint8)
    with open(mapfile, "r") as file:
        fcntl.flock(file, fcntl.LOCK_SH)
        mapdata = file.read()
        fcntl.flock(file, fcntl.LOCK_UN)

    mapdata = mapdata.replace("\n", ",").split(",")
    mapdata = [float(i) for i in mapdata if i]
    mapdata = np.array(mapdata)
    mapdata = mapdata.reshape(int(len(mapdata) / 2), 2)

    # map data is in following format and it is a single line
    # x, y, z, roll, pitch, yaw
    # read file
    with open(transfile, "r") as file:
        fcntl.flock(file, fcntl.LOCK_SH)
        transdata = file.read()
        fcntl.flock(file, fcntl.LOCK_UN)

    transdata = transdata.replace("\n", ",").split(",")
    # set x, y, z, roll, pitch and yaw
    x = float(transdata[0]) + 1024
    y = float(transdata[1]) + 1024
    # yaw = float(transdata[5])

    brush = pg.mkBrush(0, 255, 0, 120)  # Green color for self-tracking
    added_points.add((x, y))
    scatter.addPoints([x], [y], brush=brush)
    scatter.addPoints([x - 1], [y], brush=brush)
    scatter.addPoints([x + 1], [y], brush=brush)
    scatter.addPoints([x], [y + 1], brush=brush)
    scatter.addPoints([x], [y - 1], brush=brush)

    # traverse the data
    for i in range(len(mapdata)):
        x = mapdata[i][0]
        y = mapdata[i][1]

        if (x, y) not in added_points:
            # Add the point to the scatter plot item
            brush = pg.mkBrush(255, 0, 0, 120)  # Red color for map
            scatter.addPoints([x], [y], brush=brush)
            added_points.add((x, y))
            # Update the plot range to fit all points
            plot_widget.autoRange()


def plot_clicked(event):
    # Get the coordinates of the clicked point
    point = plot_widget.plotItem.vb.mapSceneToView(event.scenePos())
    x, y = point.x(), point.y()
    # cast x and y to the int and write them to the goal.txt in that format: x,y
    x = int(x)
    y = int(y)
    coordinate = f"{x},{y}"

    with open("goal.txt", "w") as file:
        file.write(coordinate)


def start_process():
    global scatter, plot_widget, filename
    # socket_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # socket_conn.connect(("192.168.43.165", port))

    app = QApplication(sys.argv)
    main_window = QMainWindow()

    # Create scatter plot item
    scatter = ScatterPlotItem(
        size=2, pen=pg.mkPen(None), brush=pg.mkBrush(255, 0, 0, 120)
    )

    # Create a plot widget and add the scatter plot item to it
    plot_widget = pg.PlotWidget()
    plot_widget.addItem(scatter)

    # Set up the main window
    central_widget = QWidget()
    layout = QVBoxLayout()
    layout.addWidget(plot_widget)
    central_widget.setLayout(layout)
    main_window.setCentralWidget(central_widget)

    # Connect the signal to the slot for mouse clicks on the plot
    plot_widget.scene().sigMouseClicked.connect(plot_clicked)

    # Generate points in a loop
    timer = QTimer()
    timer.timeout.connect(lambda: read_points())
    timer.start(1)  # Add a new point every second

    main_window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    start_process()
