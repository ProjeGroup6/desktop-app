import pickle
import sys
import socket
import struct
import numpy as np
import pyqtgraph as pg
from multiprocessing import Process
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from pyqtgraph import ScatterPlotItem


port = 8080
point_num = 360
socket_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


class MainWindow(QMainWindow):
    def __init__(self):
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
        # Generate a 360 sized data array and fill this array between 0 and 100
        global socket_conn
        data = socket_conn.recv(point_num * struct.calcsize("i"))
        data = pickle.loads(data)

        # traverse data in for loop
        for i in range(len(data)):
            # get x and y with angle and distance
            x = round(data[i] * np.cos(np.deg2rad(i)))
            y = round(data[i] * np.sin(np.deg2rad(i)))
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
    global socket_conn
    socket_conn.connect(("0.0.0.0", port))
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    process = Process(target=startProcess)
    process.start()
    process.join()
