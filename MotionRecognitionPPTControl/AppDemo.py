import sys

from PyQt5.QtWidgets import QWidget, QApplication, QStackedLayout

from layout.GuideLayout import GuideLayout
from layout.IntroLayout import IntroLayout
from layout.FileUploadLayout import FileUploadLayout
from layout.WebcamLayout import WebcamLayout


class AppDemo(QWidget):
    def __init__(self):
        app = QApplication(sys.argv)

        # 화면 전환용 widget 설정
        self.widget = QStackedLayout()

        # 레이아웃 생성
        self.introLayout = IntroLayout()
        self.guideLayout = GuideLayout()
        self.fileUploadLayout = FileUploadLayout()
        self.webcamLayout = WebcamLayout()

        # widget 추가
        self.widget.addWidget(self.introLayout)
        self.widget.addWidget(self.guideLayout)
        self.widget.addWidget(self.fileUploadLayout)
        self.widget.addWidget(self.webcamLayout)

        self.introLayout.nextButton.clicked.connect(lambda: self.nextPage())
        self.guideLayout.nextButton.clicked.connect(lambda: self.nextPage())
        self.guideLayout.backButton.clicked.connect(lambda: self.backPage())
        self.fileUploadLayout.backButton.clicked.connect(lambda: self.backPage())
        self.fileUploadLayout.camTestButton.clicked.connect(lambda: self.nextPage())
        self.webcamLayout.backButton.clicked.connect(lambda: self.backPage())

        app.exec_()

    def nextPage(self):
        # max page : 4
        if self.widget.currentIndex() < 3:
            self.widget.setCurrentIndex(self.widget.currentIndex() + 1)

    def backPage(self):
        if self.widget.currentIndex() > 0:
            self.widget.setCurrentIndex(self.widget.currentIndex() - 1)
