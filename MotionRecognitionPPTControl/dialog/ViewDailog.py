import pyautogui
from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QLabel, QVBoxLayout


class ViewDialog(QDialog):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.signLabel = QLabel(self)
        self.timeLabel = QLabel(self)

        self.signLabel.setText("동작 유추")
        self.signLabel.setFont(QtGui.QFont("맑음", 16))
        self.timeLabel.setText("시간")
        self.timeLabel.setFont(QtGui.QFont("맑음", 16))

        layout.addWidget(self.signLabel)
        layout.addWidget(self.timeLabel)

        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.setWindowFlag(Qt.WindowStaysOnTopHint)

        self.setWindowTitle('motion view')
        self.setWindowModality(Qt.ApplicationModal)

        width, height = pyautogui.size()
        print(width)
        print(height)
        self.setGeometry(width-260, height-100, 240, 80)  # x, y, width, height

        self.resize(240, 80)
        self.setLayout(layout)
