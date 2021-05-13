import os
import sys
import time

from PyQt5 import QtGui
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget

from PyQt5.QtWidgets import (QHBoxLayout, QLabel,
                             QSizePolicy, QSlider, QStyle, QVBoxLayout, QComboBox, QListView, QMainWindow, QApplication)
from PyQt5.QtWidgets import QWidget, QPushButton


class GuideLayout(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("사용설명서")
        self.resize(500, 400)

        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)

        videoWidget = QVideoWidget()

        # 플레이버튼, 정지버튼
        self.playButton = QPushButton()
        self.playButton.setEnabled(False)
        self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playButton.clicked.connect(self.play)

        self.positionSlider = QSlider(Qt.Horizontal)
        self.positionSlider.setRange(0, 0)
        self.positionSlider.sliderMoved.connect(self.setPosition)

        self.error = QLabel()
        self.error.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)

        # 뒤로가기
        self.backButton = QPushButton("Back")
        self.backButton.setFont(QtGui.QFont("맑음", 10))
        self.backButton.setFixedSize(50, 40)
        self.backButton.clicked.connect(self.back)

        # 파일업로드 가기
        self.nextButton = QPushButton("PPT Upload")
        self.nextButton.setFont(QtGui.QFont("맑음", 10))
        self.nextButton.setFixedSize(90, 40)
        self.nextButton.clicked.connect(self.next)

        # 콤보박스
        cb = QComboBox(self)  # 콤보박스 생성
        cb.setFixedHeight(30)

        cb.setView(QListView())
        cb.addItems(['넘기기(next)', '뒤로가기(back)', '잠금(lock)', '잠금풀기(unlock)',
                     '음량높이기(volume up)', '음량낮추기(volume down)'])

        cb.setStyleSheet("QListView::item {height:30px;}")

        # 옵션을 선택하면, onActivated() 메서드가 호출
        cb.activated[str].connect(self.onActivated)

        fileName = self.resource_path("video\\next.avi")
        self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(fileName)))
        self.playButton.setEnabled(True)

        # Create layouts to place inside widget
        controlLayout = QHBoxLayout()
        controlLayout.setContentsMargins(0, 0, 0, 0)
        controlLayout.addWidget(self.playButton)
        controlLayout.addWidget(self.positionSlider)

        moveLayout = QHBoxLayout()
        moveLayout.setContentsMargins(0, 0, 350, 0)
        moveLayout.addWidget(self.backButton)
        moveLayout.addWidget(self.nextButton)

        mainLayout = QVBoxLayout()
        mainLayout.addLayout(moveLayout)
        mainLayout.addWidget(cb)
        mainLayout.addWidget(videoWidget)
        mainLayout.addLayout(controlLayout)
        #mainLayout.addWidget(self.error)

        self.mediaPlayer.setVideoOutput(videoWidget)
        self.mediaPlayer.stateChanged.connect(self.mediaStateChanged)
        self.mediaPlayer.positionChanged.connect(self.positionChanged)
        self.mediaPlayer.durationChanged.connect(self.durationChanged)
        self.mediaPlayer.error.connect(self.handleError)

        self.setLayout(mainLayout)

    def onActivated(self, text):
        print(text)

        # dict로 관리하면 편한데 걍 조건문으로 대충 빨리 하는게 나을 듯

        path = None
        if text == '넘기기(next)':
            path = "video\\next.avi"
        elif text == '뒤로가기(back)':
            path = "video\\back.avi"
        elif text == '잠금(lock)':
            path = "video\\lock.avi"
        elif text == '잠금풀기(unlock)':
            path = "video\\unlock.avi"
        elif text == '음량높이기(volume up)':
            path = "video\\volume_up.avi"
        elif text == '음량낮추기(volume down)':
            path = "video\\volume_down.avi"

        fileName = self.resource_path(path)
        self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(fileName)))
        self.playButton.setEnabled(True)
        self.play()

    def resource_path(self, relative_path):
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        print(relative_path)
        print(os.path.join(base_path, relative_path))
        return os.path.join(base_path, relative_path)

    def play(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()

    def mediaStateChanged(self, state):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.playButton.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.playButton.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPlay))

    def positionChanged(self, position):
        self.positionSlider.setValue(position)

    def durationChanged(self, duration):
        self.positionSlider.setRange(0, duration)

    def setPosition(self, position):
        self.mediaPlayer.setPosition(position)

    def handleError(self):
        self.playButton.setEnabled(False)
        self.error.setText("Error: " + self.mediaPlayer.errorString())
        print('error')

    def next(self):
        self.mediaPlayer.pause()
        pass

    def back(self):
        self.mediaPlayer.pause()
        pass
