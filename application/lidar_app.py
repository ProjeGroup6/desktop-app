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


class MainWindow(QMainWindow):
    point_num = 360
    socket_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    port = 8080

    def __init__(self):
        self.socket_conn.connect(("192.168.43.254", self.port))

        super(MainWindow, self).__init__()

        # Create scatter plot item
        self.scatter = ScatterPlotItem(
            size=10, pen=pg.mkPen(None), brush=pg.mkBrush(255, 0, 0, 120)
        )

        # Create a plot widget and add the scatter plot item to it
        self.plot_widget = pg.PlotWidget()
        self.plot_widget.addItem(self.scatter)

        # Set up the main window
        central_widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(self.plot_widget)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Set to store added points
        self.added_points = set()

        # Connect the signal to the slot for mouse clicks on the plot
        self.plot_widget.scene().sigMouseClicked.connect(self.plot_clicked)

        # Generate points in a loop
        self.timer = QTimer()
        self.timer.timeout.connect(self.generate_point)
        self.timer.start(1)  # Add a new point every second

    def generate_point(self):
        data = self.socket_conn.recv(4096)
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
            if (x, y) not in self.added_points:
                # Add the point to the scatter plot item
                if x > 0 and y > 0:
                    brush = pg.mkBrush(
                        0, 255, 0, 120
                    )  # Green color for points in the positive quadrant
                else:
                    brush = pg.mkBrush(
                        (255, 0, 0, 120)
                    )  # Red color for points in the other quadrants

                self.scatter.addPoints([x], [y], brush=brush)
                self.added_points.add((x, y))

                # Update the plot range to fit all points
                self.plot_widget.autoRange()

    def plot_clicked(self, event):
        # Get the coordinates of the clicked point
        point = self.plot_widget.plotItem.vb.mapSceneToView(event.scenePos())
        x, y = point.x(), point.y()
        print("Clicked at coordinates:", x, y)


def startProcess():
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    # process = Process(target=startProcess)
    # process.start()
    # process.join()
    # create a thread
    thread = threading.Thread(target=startProcess)
    thread.start()
    thread.join()
