# Desktop application
# To test on your own computer:
#   1 - run app.py
#   2 - Run server.py in ../app-socket
#   3- Enter the IP that server.py prints on the screen.

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QThread
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer
import socket
import time
import cv2  # Import the cv2 module here
import numpy as np  # Import numpy module here

globalVar = 0
globalFlag = False

delay = 100  # delay for sending messages serial

cameraPort = 9000
serverPort = 8000


# For camera
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
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            

            l_h = cv2.getTrackbarPos("L-H", "Trackbars")
            l_s = cv2.getTrackbarPos("L-S", "Trackbars")
            l_v = cv2.getTrackbarPos("L-V", "Trackbars")
            u_h = cv2.getTrackbarPos("U-H", "Trackbars")
            u_s = cv2.getTrackbarPos("U-S", "Trackbars")
            u_v = cv2.getTrackbarPos("U-V", "Trackbars")

            lower_red = np.array([l_h, l_s, l_v])
            upper_red = np.array([u_h, u_s, u_v])

            mask = cv2.inRange(hsv, lower_red, upper_red)
            kernel = np.ones((5, 5), np.uint8)
            mask = cv2.erode(mask, kernel)

            # Contours detection
            if int(cv2.__version__[0]) > 3:
                # Opencv 4.x.x
                contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            else:
                # Opencv 3.x.x
                _, contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

            if hierarchy is not None:
                hierarchy = hierarchy[0]  # get the first contour

                for component in zip(contours, hierarchy):
                    current_contour = component[0]
                    current_hierarchy = component[1]
                    x, y, w, h = cv2.boundingRect(current_contour)
                    area = cv2.contourArea(current_contour)
                    if current_hierarchy[3] < 0 and area > 10000:
                        # these are the outermost parent components
                        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
            else:
                print("No contours found")
            image = QImage(frame.data, width, height, QImage.Format_RGB888)
            self.changePixmap.emit(image)


class ServerThread(QtCore.QThread):
    messageReceived = QtCore.pyqtSignal(str)

    def __init__(self, sock, parent=None):
        super(ServerThread, self).__init__(parent)
        self.sock = sock

    def run(self):
        while True:
            data = self.sock.recv(1024)
            if not data:
                break
            self.messageReceived.emit(data.decode())


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
        self.progressBar.setProperty("value", 0)
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
        self.speedlabel.setStyleSheet(
            "color:white;background: #1E2128;\n" "border: none;"
        )
        self.speedlabel.setObjectName("speedlabel")
        self.speedValuelabel = QtWidgets.QLabel(self.centralwidget)
        self.speedValuelabel.setGeometry(QtCore.QRect(500, 470, 47, 13))
        self.speedValuelabel.setStyleSheet(
            "color:white;background: #1E2128;\n" "border: none;"
        )
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
        self.remoteControlBackgroundlabel.setStyleSheet(
            "background: #262932;\n" "border: none;"
        )
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
        self.remoterControllabel.setStyleSheet(
            "color:white;background: #262932;\n" "border: none;"
        )
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
        self.stepleftButton.setStyleSheet("background: #59737A;\n" "color:white;")
        self.stepleftButton.setObjectName("stepleftButton")
        self.forwardButton = QtWidgets.QPushButton(self.centralwidget)
        self.forwardButton.setGeometry(QtCore.QRect(120, 270, 81, 31))
        self.forwardButton.setStyleSheet("background: #59737A;\n" "color:white;")
        self.forwardButton.setObjectName("forwardButton")
        self.turnleftButton = QtWidgets.QPushButton(self.centralwidget)
        self.turnleftButton.setGeometry(QtCore.QRect(30, 330, 81, 31))
        self.turnleftButton.setStyleSheet("background: #59737A;color:white;")
        self.turnleftButton.setObjectName("turnleftButton")
        self.autonomousbackgroundlabel = QtWidgets.QLabel(self.centralwidget)
        self.autonomousbackgroundlabel.setGeometry(QtCore.QRect(340, 220, 121, 241))
        self.autonomousbackgroundlabel.setStyleSheet(
            "background: #262932;\n" "border: none;"
        )
        self.autonomousbackgroundlabel.setText("")
        self.autonomousbackgroundlabel.setObjectName("autonomousbackgroundlabel")
        self.stopButton = QtWidgets.QPushButton(self.centralwidget)
        self.stopButton.setGeometry(QtCore.QRect(360, 330, 81, 31))
        self.stopButton.setStyleSheet("color:white;background: #59737A;")
        self.stopButton.setObjectName("stopButton")
        self.startButton = QtWidgets.QPushButton(self.centralwidget)
        self.startButton.setGeometry(QtCore.QRect(360, 290, 81, 31))
        self.startButton.setStyleSheet("color:white;background: #59737A;")
        self.startButton.setObjectName("startButton")
        self.autonomouslabel = QtWidgets.QLabel(self.centralwidget)
        self.autonomouslabel.setGeometry(QtCore.QRect(370, 230, 91, 31))
        self.autonomouslabel.setStyleSheet(
            "color:white;background: #262932;\n" "border: none;"
        )
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
        self.image_label.setGeometry(
            QtCore.QRect(0, 0, 451, 391)
        )  # Use same geometry as cameraframe
        self.image_label.setScaledContents(True)

        # Initialize video stream thread

        # print("cameraSock: "self.cameraSock)

        # Functions of the buttons
        self.connectButton.clicked.connect(self.connect_to_server)

        self.forwardButton.clicked.connect(lambda: self.send_message_to_server("1"))
        self.buzzerButton.clicked.connect(lambda: self.send_message_to_server("2"))
        self.backwardButton.clicked.connect(lambda: self.send_message_to_server("3"))
        self.stepleftButton.clicked.connect(lambda: self.send_message_to_server("4"))
        self.turnleftButton.clicked.connect(lambda: self.send_message_to_server("5"))
        self.steprightButton.clicked.connect(lambda: self.send_message_to_server("6"))
        self.turnrightButton.clicked.connect(lambda: self.send_message_to_server("7"))
        self.relaxButton.clicked.connect(lambda: self.send_message_to_server("8"))
        self.balanceButton.clicked.connect(lambda: self.send_message_to_server("9"))
        self.startButton.clicked.connect(lambda: self.send_message_to_server("10"))
        self.stopButton.clicked.connect(lambda: self.send_message_to_server("11"))
        self.openCameraButton.clicked.connect(lambda: self.send_message_to_server("12"))

        # When the button is pressed, start the timer and set the flag
        self.forwardButton.pressed.connect(self.forwardButton_pressed)
        self.backwardButton.pressed.connect(self.backwardButton_pressed)
        self.stepleftButton.pressed.connect(self.stepleftButton_pressed)
        self.turnleftButton.pressed.connect(self.turnleftButton_pressed)
        self.steprightButton.pressed.connect(self.steprightButton_pressed)
        self.turnrightButton.pressed.connect(self.turnrightButton_pressed)

        # When the button is released, stop the timer and unset the flag
        self.forwardButton.released.connect(self.forwardButton_released)
        self.backwardButton.released.connect(self.backwardButton_released)
        self.stepleftButton.released.connect(self.stepleftButton_released)
        self.turnleftButton.released.connect(self.turnleftButton_released)
        self.steprightButton.released.connect(self.steprightButton_released)
        self.turnrightButton.released.connect(self.turnrightButton_released)

    def update_progress(self):
        global globalVar
        self.progressBar.setValue(globalVar)

    def forwardButton_pressed(self):
        self.is_forwardButton_pressed = True
        self.forwardButtonTimer.start()

    def forwardButton_released(self):
        self.is_forwardButton_pressed = False
        self.forwardButtonTimer.stop()

    def backwardButton_pressed(self):
        self.is_backwardButton_pressed = True
        self.backwardButtonTimer.start()

    def backwardButton_released(self):
        self.is_backwardButton_pressed = False
        self.backwardButtonTimer.stop()

    def stepleftButton_pressed(self):
        self.is_stepleftButton_pressed = True
        self.stepleftButtonTimer.start()

    def stepleftButton_released(self):
        self.is_stepleftButton_pressed = False
        self.stepleftButtonTimer.stop()

    def turnleftButton_pressed(self):
        self.is_turnleftButton_pressed = True
        self.turnleftButtonTimer.start()

    def turnleftButton_released(self):
        self.is_turnleftButton_pressed = False
        self.turnleftButtonTimer.stop()

    def steprightButton_pressed(self):
        self.is_steprightButton_pressed = True
        self.steprightButtonTimer.start()

    def steprightButton_released(self):
        self.is_steprightButton_pressed = False
        self.steprightButtonTimer.stop()

    def turnrightButton_pressed(self):
        self.is_turnrightButton_pressed = True
        self.turnrightButtonTimer.start()

    def turnrightButton_released(self):
        self.is_turnrightButton_pressed = False
        self.turnrightButtonTimer.stop()

    # Slot for handling the valueChanged signal
    def updateSpeedValue(self, value):
        self.speedValuelabel.setText(str(value))
        # Send the new value to the server
        self.send_message(str(value))

    # Modify this function to prepend 'S' to the message
    def send_message(self, message):
        if self.sock is None:
            print("Not connected to a server")
            return
        self.sock.sendall(("S" + message).encode())

    # Required for camera
    def start_video_stream(self):
        self.video_stream_thread.start()

    def set_camera_image(self, image):
        pixmap = QPixmap.fromImage(image)
        self.image_label.setPixmap(pixmap)

    def __init__(self):
        self.sock = None
        self.cameraSock = None
        self.server_thread = None
        self.isConnected = False

        # Create a thread that will listen for incoming messages
        self.listen_thread = QThread()
        self.listen_thread.run = (
            self.listen_to_server
        )  # The run method is the entry point into the thread
        self.listen_thread.start()

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_progress)
        self.timer.start(1000)  # update every second

        # Create a timer for each button
        self.forwardButtonTimer = QTimer()
        self.backwardButtonTimer = QTimer()
        self.stepleftButtonTimer = QTimer()
        self.turnleftButtonTimer = QTimer()
        self.steprightButtonTimer = QTimer()
        self.turnrightButtonTimer = QTimer()

        # Add a flag for each action
        self.is_forwardButton_pressed = False
        self.is_backwardButton_pressed = False
        self.is_stepleftButton_pressed = False
        self.is_turnleftButton_pressed = False
        self.is_steprightButton_pressed = False
        self.is_turnrightButton_pressed = False

        # Connect the timer timeout signal to the send method
        self.forwardButtonTimer.timeout.connect(
            lambda: self.send_message_to_server("1")
            if self.is_forwardButton_pressed
            else None
        )
        self.backwardButtonTimer.timeout.connect(
            lambda: self.send_message_to_server("3")
            if self.is_backwardButton_pressed
            else None
        )
        self.stepleftButtonTimer.timeout.connect(
            lambda: self.send_message_to_server("4")
            if self.is_stepleftButton_pressed
            else None
        )
        self.turnleftButtonTimer.timeout.connect(
            lambda: self.send_message_to_server("5")
            if self.is_turnleftButton_pressed
            else None
        )
        self.steprightButtonTimer.timeout.connect(
            lambda: self.send_message_to_server("6")
            if self.is_steprightButton_pressed
            else None
        )
        self.turnrightButtonTimer.timeout.connect(
            lambda: self.send_message_to_server("7")
            if self.is_turnrightButton_pressed
            else None
        )

        # Set the timer interval (in milliseconds)
        self.forwardButtonTimer.setInterval(delay)  # Modify this as needed
        self.backwardButtonTimer.setInterval(delay)  # Modify this as needed
        self.stepleftButtonTimer.setInterval(delay)  # Modify this as needed
        self.turnleftButtonTimer.setInterval(delay)  # Modify this as needed
        self.steprightButtonTimer.setInterval(delay)  # Modify this as needed
        self.turnrightButtonTimer.setInterval(delay)  # Modify this as needed

    def listen_to_server(self):
        while self.isConnected:
            while True:  # Keep running indefinitely
                # Check if the socket is initialized and connected
                if self.sock is None:
                    print("Socket is not connected")
                    time.sleep(1)  # Wait for a bit before checking again
                    continue  # Skip the rest of the loop

                # Wait for a message from the server
                try:
                    data = self.sock.recv(1024)
                except Exception as e:
                    print(f"Error receiving data from socket: {e}")
                    self.sock = None  # Mark the socket as closed
                    continue  # Skip the rest of the loop

                if (
                    not data
                ):  # If there is no data, the server has closed the connection
                    print("Server closed the connection")
                    self.sock = None  # Mark the socket as closed
                    break

                # The rest of your code...

    def update_progress(self):
        global globalVar
        self.progressBar.setValue(globalVar)

    # Required for server
    def send_message_to_server(self, message):
        if self.sock is None:
            print("Not connected to a server")
            return
        self.sock.sendall(message.encode())

    def start_server_thread(self):
        if self.sock is not None:
            self.server_thread = ServerThread(self.sock)
            self.server_thread.messageReceived.connect(self.handle_server_message)
            self.server_thread.start()

    def start_camera_thread(self):
        if self.cameraSock is not None:
            self.video_stream_thread = RunThread(self.cameraSock)

            # Connect button and video stream thread
            self.openCameraButton.clicked.connect(self.start_video_stream)
            self.video_stream_thread.changePixmap.connect(self.set_camera_image)

    def handle_server_message(self, message):
        print(f"Message from server: {message}")
        global globalVar
        # assuming your battery value message is prefixed with 'B'
        if message.startswith("B"):
            try:
                battery_value = int(message[1:])  # skip the 'B' prefix
                globalVar = battery_value  # update the global battery value
            except ValueError:
                print("Received invalid battery value")

    def connect_to_server(self):
        global globalFlag
        if self.sock is not None:
            self.sock.close()

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print(self.sock)
        server_ip = self.connectAddresInput.toPlainText()
        server_port = 8000  # Change this to your server's port
        self.sock.connect((server_ip, server_port))
        print(f"Connected to server at {server_ip}:{server_port}")

        self.cameraSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_ip = self.connectAddresInput.toPlainText()
        camera_port = 9000  # Change this to your server's port
        self.cameraSock.connect((server_ip, camera_port))
        print(f"Connected to server at {server_ip}:{camera_port}")
        self.isConnected = True  # Set connected to true
        globalFlag = True
        print("sock: ")
        print(self.sock)
        print("cameraSock: ")
        print(self.cameraSock)
        # Start the server thread after connecting
        self.start_server_thread()
        self.start_camera_thread()

        # Start listening to server after connecting
        self.listen_thread.start()

    def disconnect_from_server(self):  # Add a disconnect function
        if self.sock is not None:
            self.sock.close()
            self.isConnected = False  # Set connected to false
        print("Disconnected from server")

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
        self.stopButton.setText(_translate("MainWindow", "Stop"))
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
