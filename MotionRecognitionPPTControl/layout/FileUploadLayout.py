from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QPushButton, QFileDialog


# 메인 화면 구성요소 - 드래그앤드랍(라벨), 파일업로드(버튼)


class FileUploadLayout(QWidget):

    def __init__(self, app):
        super().__init__()
        self.path = None
        self.app = app

        self.resize(400, 400)
        self.setAcceptDrops(True)
        self.setWindowTitle("파일업로드")

        fileUploadLayout = QGridLayout()

        self.dragAndDropsLabel = QLabel()
        self.dragAndDropsLabel.setAlignment(Qt.AlignCenter)
        self.dragAndDropsLabel.setText('파일을 드래그해서 올려주세요.')
        self.dragAndDropsLabel.setFont(QtGui.QFont("맑음", 14))
        self.dragAndDropsLabel.setStyleSheet('''
                        QLabel{
                            border: 4px dashed #aaa
                        }
                    ''')

        # 웹캠 테스트
        self.camTestButton = QPushButton("웹캠 테스트")
        self.camTestButton.setFont(QtGui.QFont("맑음", 10))
        self.camTestButton.clicked.connect(self.next)

        # 뒤로가기
        self.backButton = QPushButton("사용설명서 보러가기")
        self.backButton.setFont(QtGui.QFont("맑음", 10))
        self.backButton.clicked.connect(self.back)

        # 파일 업로드 버튼
        self.pushButton = QPushButton("파일 업로드")
        self.pushButton.setMaximumHeight(60)

        self.pushButton.setChecked(True)
        self.pushButton.toggle()

        # 그리드 사용
        fileUploadLayout.addWidget(self.dragAndDropsLabel, 0, 1)
        fileUploadLayout.addWidget(self.pushButton, 1, 1)
        fileUploadLayout.addWidget(self.backButton, 2, 1)
        fileUploadLayout.addWidget(self.camTestButton, 3, 1)

        self.pushButton.clicked.connect(self.addOpen)
        self.setLayout(fileUploadLayout)

    def back(self):
        pass

    def next(self):
        pass

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls:
            event.setDropAction(Qt.CopyAction)

            # 파일 경로
            self.app.ppt.path = event.mimeData().urls()[0].toLocalFile()

            # 준비 완료(init)
            self.readyForSlideShow()

            event.accept()
        else:
            event.ignore()

    def addOpen(self):
        if self.pushButton.text() == "시작":
            self.app.ppt.fullScreen()
            self.app.nextPage()
            self.app.start()
            pass
        else:
            FileOpen = QFileDialog.getOpenFileName(self, 'Open file', './')

            # 파일 경로
            self.app.ppt.path = str(FileOpen[0])

            # 준비 완료(init)
            self.readyForSlideShow()
            return

    def readyForSlideShow(self):
        if self.app.ppt.path == "":
            return

        # 경로 받아오기
        self.pushButton.setText("시작")
        self.dragAndDropsLabel.setText(
            "파일경로\n" + self.app.ppt.path + "\n\n시작 버튼을 누르면 슬라이드쇼가 실행됩니다.")
