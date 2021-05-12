from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton


# 인트로 화면 구성요소 - 설명(lable), 다음페이지(버튼)


class IntroLayout(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("인트로")
        self.resize(500, 400)

        introLayout = QVBoxLayout()
        introLayout.setContentsMargins(24, 36, 24, 0)

        label = QLabel("앱에 대한 간단한 설명 및 소개")
        label.setAlignment(Qt.AlignCenter)
        label.setFont(QtGui.QFont("맑음", 14))
        label.setStyleSheet(
            "border-style: solid;"
            "border-width: 2px;"
            "border-color: gray;"
            "border-radius: 4px;"
            "padding: 16px;"
        )

        self.nextButton = QPushButton("시작하기")
        self.nextButton.setFont(QtGui.QFont("맑음", 14))
        self.nextButton.setFixedSize(120, 40)

        introLayout.addWidget(label)
        introLayout.addWidget(self.nextButton, alignment=Qt.AlignCenter)

        self.nextButton.clicked.connect(self.next)

        self.setLayout(introLayout)

    def next(self):
        pass
