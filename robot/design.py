from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QImage, QPixmap

class RunThread(QtCore.QThread):
    changePixmap = QtCore.pyqtSignal(QImage)

    def run(self):
        import socket  # Import the socket module here
        import cv2  # Import the cv2 module here
        import numpy as np  # Import numpy module here
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = "0.0.0.0"  # Listen on all available network interfaces
        port = 8080  # Use the same port number as in the sender
        sock.bind((host, port))
        sock.listen(1)

        # Accept a connection
        conn, addr = sock.accept()
        print("Connected by", addr)

        while True:
            # Receive the frame size
            data_size = int.from_bytes(conn.recv(4), byteorder="big")

            # Receive the frame data
            data = b""
            while len(data) < data_size:
                packet = conn.recv(data_size - len(data))
                if not packet:
                    break
                data += packet

            # Decode and display the frame in the PyQt5 window
            frame = cv2.imdecode(np.frombuffer(data, np.uint8), cv2.IMREAD_COLOR)
            height, width, _ = frame.shape
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = QImage(frame.data, width, height, QImage.Format_RGB888)
            self.changePixmap.emit(image)





class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1060, 566)
        MainWindow.setStyleSheet("background: #1E2128;")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(20, 70, 241, 31))
        self.progressBar.setStyleSheet("color:white;")
        self.progressBar.setProperty("value", 24)
        self.progressBar.setTextDirection(QtWidgets.QProgressBar.BottomToTop)
        self.progressBar.setObjectName("progressBar")
        self.connectAddresInput = QtWidgets.QTextEdit(self.centralwidget)
        self.connectAddresInput.setGeometry(QtCore.QRect(280, 70, 191, 31))
        self.connectAddresInput.setStyleSheet("background: white;")
        self.connectAddresInput.setObjectName("connectAddresInput")
        self.connectButton = QtWidgets.QPushButton(self.centralwidget)
        self.connectButton.setGeometry(QtCore.QRect(480, 70, 81, 31))
        self.connectButton.setStyleSheet("color:white;background: #59737A;")
        self.connectButton.setObjectName("connectButton")
        self.verticalSlider = QtWidgets.QSlider(self.centralwidget)
        self.verticalSlider.setGeometry(QtCore.QRect(510, 210, 22, 251))
        self.verticalSlider.setOrientation(QtCore.Qt.Vertical)
        self.verticalSlider.setObjectName("verticalSlider")

        # Set the range and default value
        self.verticalSlider.setRange(0, 9)
        self.verticalSlider.setValue(6)
        self.verticalSlider.valueChanged.connect(self.updateSpeedValue)

        self.speedlabel = QtWidgets.QLabel(self.centralwidget)
        self.speedlabel.setGeometry(QtCore.QRect(500, 180, 47, 13))
        self.speedlabel.setStyleSheet("color:white;background: #1E2128;\n"
"border: none;")
        self.speedlabel.setObjectName("speedlabel")
        self.speedValuelabel = QtWidgets.QLabel(self.centralwidget)
        self.speedValuelabel.setGeometry(QtCore.QRect(500, 470, 47, 13))
        self.speedValuelabel.setStyleSheet("color:white;background: #1E2128;\n"
"border: none;")
        self.speedValuelabel.setText("")
        self.speedValuelabel.setObjectName("speedValuelabel")
        self.cameraframe = QtWidgets.QFrame(self.centralwidget)
        self.cameraframe.setGeometry(QtCore.QRect(580, 20, 451, 391))
        self.cameraframe.setStyleSheet("border:3px solid #262932;")
        self.cameraframe.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.cameraframe.setFrameShadow(QtWidgets.QFrame.Raised)
        self.cameraframe.setObjectName("cameraframe")
        self.openCameraButton = QtWidgets.QPushButton(self.centralwidget)
        self.openCameraButton.setGeometry(QtCore.QRect(760, 440, 81, 31))
        self.openCameraButton.setStyleSheet("color:white;background: #59737A;")
        self.openCameraButton.setObjectName("openCameraButton")
        self.remoteControlBackgroundlabel = QtWidgets.QLabel(self.centralwidget)
        self.remoteControlBackgroundlabel.setGeometry(QtCore.QRect(10, 220, 311, 241))
        self.remoteControlBackgroundlabel.setStyleSheet("background: #262932;\n"
"border: none;")
        self.remoteControlBackgroundlabel.setText("")
        self.remoteControlBackgroundlabel.setObjectName("remoteControlBackgroundlabel")
        self.balanceButton = QtWidgets.QPushButton(self.centralwidget)
        self.balanceButton.setGeometry(QtCore.QRect(190, 390, 81, 31))
        self.balanceButton.setStyleSheet("color:white;background: #59737A;")
        self.balanceButton.setObjectName("balanceButton")
        self.steprightButton = QtWidgets.QPushButton(self.centralwidget)
        self.steprightButton.setGeometry(QtCore.QRect(210, 290, 81, 31))
        self.steprightButton.setStyleSheet("color:white;background: #59737A;")
        self.steprightButton.setObjectName("steprightButton")
        self.remoterControllabel = QtWidgets.QLabel(self.centralwidget)
        self.remoterControllabel.setGeometry(QtCore.QRect(120, 230, 111, 31))
        self.remoterControllabel.setStyleSheet("color:white;background: #262932;\n"
"border: none;")
        self.remoterControllabel.setObjectName("remoterControllabel")
        self.turnrightButton = QtWidgets.QPushButton(self.centralwidget)
        self.turnrightButton.setGeometry(QtCore.QRect(210, 330, 81, 31))
        self.turnrightButton.setStyleSheet("color:white;background: #59737A;")
        self.turnrightButton.setObjectName("turnrightButton")
        self.backwardButton = QtWidgets.QPushButton(self.centralwidget)
        self.backwardButton.setGeometry(QtCore.QRect(120, 350, 81, 31))
        self.backwardButton.setStyleSheet("color:white;background: #59737A;")
        self.backwardButton.setObjectName("backwardButton")
        self.relaxButton = QtWidgets.QPushButton(self.centralwidget)
        self.relaxButton.setGeometry(QtCore.QRect(50, 390, 81, 31))
        self.relaxButton.setStyleSheet("color:white;background: #59737A;")
        self.relaxButton.setObjectName("relaxButton")
        self.buzzerButton = QtWidgets.QPushButton(self.centralwidget)
        self.buzzerButton.setGeometry(QtCore.QRect(120, 310, 81, 31))
        self.buzzerButton.setStyleSheet("color:white;background: #59737A;")
        self.buzzerButton.setObjectName("buzzerButton")
        self.stepleftButton = QtWidgets.QPushButton(self.centralwidget)
        self.stepleftButton.setGeometry(QtCore.QRect(30, 290, 81, 31))
        self.stepleftButton.setStyleSheet("background: #59737A;\n"
"color:white;")
        self.stepleftButton.setObjectName("stepleftButton")
        self.forwardButton = QtWidgets.QPushButton(self.centralwidget)
        self.forwardButton.setGeometry(QtCore.QRect(120, 270, 81, 31))
        self.forwardButton.setStyleSheet("background: #59737A;\n"
"color:white;")
        self.forwardButton.setObjectName("forwardButton")
        self.turnleftButton = QtWidgets.QPushButton(self.centralwidget)
        self.turnleftButton.setGeometry(QtCore.QRect(30, 330, 81, 31))
        self.turnleftButton.setStyleSheet("background: #59737A;color:white;")
        self.turnleftButton.setObjectName("turnleftButton")
        self.autonomousbackgroundlabel = QtWidgets.QLabel(self.centralwidget)
        self.autonomousbackgroundlabel.setGeometry(QtCore.QRect(340, 220, 121, 241))
        self.autonomousbackgroundlabel.setStyleSheet("background: #262932;\n"
"border: none;")
        self.autonomousbackgroundlabel.setText("")
        self.autonomousbackgroundlabel.setObjectName("autonomousbackgroundlabel")
        self.stopBUtton = QtWidgets.QPushButton(self.centralwidget)
        self.stopBUtton.setGeometry(QtCore.QRect(360, 330, 81, 31))
        self.stopBUtton.setStyleSheet("color:white;background: #59737A;")
        self.stopBUtton.setObjectName("stopBUtton")
        self.startButton = QtWidgets.QPushButton(self.centralwidget)
        self.startButton.setGeometry(QtCore.QRect(360, 290, 81, 31))
        self.startButton.setStyleSheet("color:white;background: #59737A;")
        self.startButton.setObjectName("startButton")
        self.autonomouslabel = QtWidgets.QLabel(self.centralwidget)
        self.autonomouslabel.setGeometry(QtCore.QRect(370, 230, 91, 31))
        self.autonomouslabel.setStyleSheet("color:white;background: #262932;\n"
"border: none;")
        self.autonomouslabel.setObjectName("autonomouslabel")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1060, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.verticalSlider.valueChanged.connect(self.updateSpeedValue)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
         # Set up the cameraframe to display images
        self.image_label = QtWidgets.QLabel(self.cameraframe)
        self.image_label.setGeometry(QtCore.QRect(0, 0, 451, 391))  # Use same geometry as cameraframe
        self.image_label.setScaledContents(True)

        # Initialize video stream thread
        self.video_stream_thread = RunThread()

        # Connect button and video stream thread
        self.openCameraButton.clicked.connect(self.start_video_stream)
        self.video_stream_thread.changePixmap.connect(self.set_camera_image)
        
     # Slot for handling the valueChanged signal
    def updateSpeedValue(self, value):
        self.speedValuelabel.setText(str(value)) 
    def start_video_stream(self):
        self.video_stream_thread.start()
    def set_camera_image(self, image):
        pixmap = QPixmap.fromImage(image)
        self.image_label.setPixmap(pixmap)


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.connectButton.setText(_translate("MainWindow", "Connect"))
        self.speedlabel.setText(_translate("MainWindow", "Speed"))
        self.openCameraButton.setText(_translate("MainWindow", "Open Camera"))
        self.balanceButton.setText(_translate("MainWindow", "Balance"))
        self.steprightButton.setText(_translate("MainWindow", "Step Right"))
        self.remoterControllabel.setText(_translate("MainWindow", "REMOTE CONTROL"))
        self.turnrightButton.setText(_translate("MainWindow", "Turn Right"))
        self.backwardButton.setText(_translate("MainWindow", "Backward"))
        self.relaxButton.setText(_translate("MainWindow", "Relax"))
        self.buzzerButton.setText(_translate("MainWindow", "Buzzer"))
        self.stepleftButton.setText(_translate("MainWindow", "Step Left"))
        self.forwardButton.setText(_translate("MainWindow", "Forward"))
        self.turnleftButton.setText(_translate("MainWindow", "Turn Left"))
        self.stopBUtton.setText(_translate("MainWindow", "Stop"))
        self.startButton.setText(_translate("MainWindow", "Start"))
        self.autonomouslabel.setText(_translate("MainWindow", "AUTONOMOUS"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
