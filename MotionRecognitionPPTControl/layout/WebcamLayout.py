import threading

import cv2
from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox, QHBoxLayout

from HandTracking import HandTracking

# 웹캠 화면
from dialog.ViewDailog import ViewDialog


class WebcamLayout(QWidget):

    def __init__(self):
        super().__init__()
        self.dialog = ViewDialog()
        self.setWindowTitle("웹캠")
        self.resize(600, 600)

        webcamLayout = QVBoxLayout()

        controllerLayout = QVBoxLayout()

        # 뒤로가기
        self.backButton = QPushButton("뒤로가기")
        self.backButton.setFont(QtGui.QFont("맑음", 10))
        self.backButton.clicked.connect(self.back)

        # 웹캠 켜기
        self.camOpenButton = QPushButton("캠 켜기")
        self.camOpenButton.setFont(QtGui.QFont("맑음", 10))
        self.camOpenButton.clicked.connect(self.start)

        self.dialogButton = QPushButton("동작 도움 켜기")
        self.dialogButton.setFont(QtGui.QFont("맑음", 10))
        self.dialogButton.clicked.connect(self.dialog.show)

        controllerLayout.addWidget(self.backButton)
        controllerLayout.addWidget(self.camOpenButton)
        controllerLayout.addWidget(self.dialogButton)

        self.camView = QLabel()
        webcamLayout.addLayout(controllerLayout)
        webcamLayout.addWidget(self.backButton)
        webcamLayout.addWidget(self.camView)

        self.setLayout(webcamLayout)

    def back(self):
        pass

    def run(self):
        handTracking = HandTracking(self.dialog)

        handTracking.run(camView=self.camView)

        width = handTracking.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        height = handTracking.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

        self.camView.resize(width, height)

    def start(self):
        self.dialog.show()
        self.show()
        th = threading.Thread(target=self.run)
        th.start()
