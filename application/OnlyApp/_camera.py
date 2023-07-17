from PyQt5.QtGui import QImage
from PyQt5.QtCore import QThread
from PyQt5 import QtCore, QtWidgets


class RunThread(QtCore.QThread):
    changePixmap = QtCore.pyqtSignal(QImage)

    def __init__(self, sock, parent=None):
        super(RunThread, self).__init__(parent)
        self.sock = sock

    def run(self):
        import cv2  # Import the cv2 module here
        import numpy as np  # Import numpy module here

        print(self.sock)
        while True:
            # Receive the frame size
            data_size = int.from_bytes(self.sock.recv(4), byteorder="big")

            # Receive the frame data
            data = b""
            while len(data) < data_size:
                packet = self.sock.recv(data_size - len(data))
                if not packet:
                    break
                data += packet

            # Decode and display the frame in the PyQt5 window
            frame = cv2.imdecode(np.frombuffer(data, np.uint8), cv2.IMREAD_COLOR)
            height, width, _ = frame.shape
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

            # l_h = cv2.getTrackbarPos("L-H", "Trackbars")
            # l_s = cv2.getTrackbarPos("L-S", "Trackbars")
            # l_v = cv2.getTrackbarPos("L-V", "Trackbars")
            # u_h = cv2.getTrackbarPos("U-H", "Trackbars")
            # u_s = cv2.getTrackbarPos("U-S", "Trackbars")
            # u_v = cv2.getTrackbarPos("U-V", "Trackbars")

            # lower_red = np.array([l_h, l_s, l_v])
            # upper_red = np.array([u_h, u_s, u_v])

            # mask = cv2.inRange(hsv, lower_red, upper_red)
            # kernel = np.ones((5, 5), np.uint8)
            # mask = cv2.erode(mask, kernel)

            # # Contours detection
            # if int(cv2.__version__[0]) > 3:
            #     # Opencv 4.x.x
            #     contours, hierarchy = cv2.findContours(
            #         mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE
            #     )
            # else:
            #     # Opencv 3.x.x
            #     _, contours, hierarchy = cv2.findContours(
            #         mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE
            #     )

            # if hierarchy is not None:
            #     hierarchy = hierarchy[0]  # get the first contour

            #     for component in zip(contours, hierarchy):
            #         current_contour = component[0]
            #         current_hierarchy = component[1]
            #         x, y, w, h = cv2.boundingRect(current_contour)
            #         area = cv2.contourArea(current_contour)
            #         if current_hierarchy[3] < 0 and area > 10000:
            #             # these are the outermost parent components
            #             cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
            # else:
            #     print("No contours found")

            image = QImage(frame.data, width, height, QImage.Format_RGB888)
            self.changePixmap.emit(image)
