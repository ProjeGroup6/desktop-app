import pickle
import sys
import socket
import struct
import threading
import numpy as np
import pyqtgraph as pg
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from pyqtgraph import ScatterPlotItem

point_num = 360
port = 8080
added_points = set()
scatter = None
plot_widget = None


def receive_points(socket_conn):
    data = socket_conn.recv(4096)
    if not data:
        return

    try:
        data = pickle.loads(data)
    except pickle.UnpicklingError as e:
        return  # or any other appropriate error handling

    # traverse data in for loop
    for i in range(len(data)):
        if data[i] == None:
            continue
        # get x and y with angle and distance
        x = int(data[i] * np.cos(np.deg2rad(i)) * 10) / 10
        y = int(data[i] * np.sin(np.deg2rad(i)) * 10) / 10
        # Check if the point already exists
        if (x, y) not in added_points:
            # Add the point to the scatter plot item
            if x > 0 and y > 0:
                brush = pg.mkBrush(
                    0, 255, 0, 120
                )  # Green color for points in the positive quadrant
            else:
                brush = pg.mkBrush(
                    (255, 0, 0, 120)
                )  # Red color for points in the other quadrants

            scatter.addPoints([x], [y], brush=brush)
            added_points.add((x, y))

            # Update the plot range to fit all points
            plot_widget.autoRange()


def plot_clicked(event):
    # Get the coordinates of the clicked point
    point = plot_widget.plotItem.vb.mapSceneToView(event.scenePos())
    x, y = point.x(), point.y()
    print("Clicked at coordinates:", x, y)


def start_process():
    global scatter, plot_widget
    socket_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_conn.connect(("172.17.0.1", port))

    app = QApplication(sys.argv)
    main_window = QMainWindow()

    # Create scatter plot item
    scatter = ScatterPlotItem(
        size=10, pen=pg.mkPen(None), brush=pg.mkBrush(255, 0, 0, 120)
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
    timer.timeout.connect(lambda: receive_points(socket_conn))
    timer.start(1)  # Add a new point every second

    main_window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    start_process()
