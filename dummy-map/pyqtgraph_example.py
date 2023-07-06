import sys
import numpy as np
import pyqtgraph as pg
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from pyqtgraph import ScatterPlotItem


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
        self.plot_widget.scene().sigMouseClicked.connect(
            self.onclick
        )  # Connect the onclick event

        # Set up the main window
        central_widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(self.plot_widget)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Generate points in a loop
        self.timer = QTimer()
        self.timer.timeout.connect(self.generate_point)
        self.timer.start(1)  # Add a new point every second

    def generate_point(self):
        points = {}

        # Generate a random point
        x = round(np.random.normal())
        y = round(np.random.normal())

        # print size of the points dictionary
        # print(len(points))

        if (x, y) not in points:
            print("aaa")
            points[(x, y)] = True
            # Add the point to the scatter plot item
            self.scatter.addPoints([x], [y])
            # Update the plot range to fit all points
            self.plot_widget.autoRange()
        else:
            print("bbbbb")

    def onclick(self, event):
        # Get the position of the clicked point
        pos = event.scenePos()
        x, y = pos.x(), pos.y()

        # Print the coordinates
        print(f"Clicked at ({x}, {y})")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
