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
        # Generate a random point
        x = round(np.random.normal())
        y = round(np.random.normal())

        # Check if the point already exists
        if (x, y) not in self.added_points:
            # Add the point to the scatter plot item
            self.scatter.addPoints([x], [y])
            self.added_points.add((x, y))

            # Update the plot range to fit all points
            self.plot_widget.autoRange()

    def plot_clicked(self, event):
        # Get the coordinates of the clicked point
        point = self.plot_widget.plotItem.vb.mapSceneToView(event.scenePos())
        x, y = point.x(), point.y()
        print("Clicked at coordinates:", x, y)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
