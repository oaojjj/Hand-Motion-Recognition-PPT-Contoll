import threading

import cv2
from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox, QHBoxLayout


# 웹캠 화면
class WebcamLayout(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("웹캠")
        self.resize(600, 600)

        webcamLayout = QVBoxLayout()

        controllerLayout = QHBoxLayout()

        # 뒤로가기
        self.backButton = QPushButton("뒤로가기")
        self.backButton.setFont(QtGui.QFont("맑음", 10))
        self.backButton.clicked.connect(self.back)

        # 웹캠 켜기
        self.camOpenButton = QPushButton("캠 켜기")
        self.camOpenButton.setFont(QtGui.QFont("맑음", 10))
        self.camOpenButton.clicked.connect(self.start)

        controllerLayout.addWidget(self.backButton)
        controllerLayout.addWidget(self.camOpenButton)

        self.camView = QLabel()
        webcamLayout.addLayout(controllerLayout)
        webcamLayout.addWidget(self.backButton)
        webcamLayout.addWidget(self.camView)

        self.setLayout(webcamLayout)

    def back(self):
        pass

    def run(self):
        cap = cv2.VideoCapture(0)

        width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

        self.camView.resize(width, height)

        while True:
            ret, img = cap.read()
            if ret:
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                h, w, c = img.shape

                qImg = QtGui.QImage(img.data, w, h, w * c, QtGui.QImage.Format_RGB888)
                pixmap = QtGui.QPixmap.fromImage(qImg)
                self.camView.setPixmap(pixmap)
            else:
                QMessageBox.about(self, "Error", "Cannot read frame.")
                print("cannot read frame.")
                break
        cap.release()
        print("Thread end.")

    def start(self):
        self.show()
        th = threading.Thread(target=self.run)
        th.start()
