from PyQt5.QtGui import QImage
from PyQt5.QtCore import QThread
from PyQt5 import QtCore, QtWidgets
import os
import cv2
import numpy as np
import socket


class RunThread(QtCore.QThread):
    changePixmap = QtCore.pyqtSignal(QImage)

    def __init__(self, sock, parent=None):
        super(RunThread, self).__init__(parent)
        self.sock = sock

    def run(self):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        count = 0
        img_num = 1
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

            if count % 25 == 0:
                cv2.imwrite(f"imgs/image_{img_num}.jpg", frame)
                img_num += 1

            count += 1
            image = QImage(frame.data, width, height, QImage.Format_RGB888)
            self.changePixmap.emit(image)

        client_socket.close()
