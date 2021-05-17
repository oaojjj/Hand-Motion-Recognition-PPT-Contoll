import cv2
import mediapipe as mp
import numpy as np
import time

from PyQt5 import QtGui
from tensorflow.python.keras.models import load_model

import AppDemo


class HandTracking:
    MODEL_NAME = "model0512_3.h5"
    MP_DRAWING = mp.solutions.drawing_utils
    MP_HANDS = mp.solutions.hands

    # For webcam input
    hands = MP_HANDS.Hands(
        static_image_mode=False,
        max_num_hands=1,
        min_detection_confidence=0.5, min_tracking_confidence=0.5)

    def __init__(self, dialog):
        self.model = load_model("model/" + self.MODEL_NAME)
        self.dialog = dialog
        self.startTime = 0
        self.detectedTime = 0
        self.detectedPoint = []
        self.detectedFlag = False
        self.mouseFlag = False
        self.lockFlag = False
        self.sign = None
        self.cap = None
        self.indexFingerTip = None

    def run(self, camView):
        self.cap = cv2.VideoCapture(0)

        while self.cap.isOpened():
            success, image = self.cap.read()
            if not success:
                print("Ignoring empty camera frame.")
                # If loading a video, use 'break' instead of 'continue'.
                continue

            image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)

            image.flags.writeable = False
            results = self.hands.process(image)

            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            imageHeight, imageWidth, imageColor = image.shape

            point = 0
            if results.multi_hand_landmarks:  # 손이 보이는 순간부터 좌표값 넘어옴

                if self.detectedFlag:
                    self.detectedTime = time.time() - self.startTime

                # 시간
                self.dialog.timeLabel.setText("동작 시간: " + str(round(self.detectedTime, 5)) + "초")
                cv2.putText(image, text=str(self.detectedTime), org=(30, 30), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                            fontScale=1,
                            color=(255, 255, 255),
                            thickness=2)

                keyPoint = []
                for hand_landmarks in results.multi_hand_landmarks:
                    self.MP_DRAWING.draw_landmarks(image, hand_landmarks, self.MP_HANDS.HAND_CONNECTIONS)
                    self.indexFingerTip = hand_landmarks.landmark[self.MP_HANDS.HandLandmark.INDEX_FINGER_TIP]

                    # x,y,z 좌표 얻기
                    for dataPoint in hand_landmarks.landmark:
                        self.detectedPoint.append(dataPoint.x)
                        self.detectedPoint.append(dataPoint.y)
                        keyPoint.append({'point': point, 'x': dataPoint.x, 'y': dataPoint.y})
                        point += 1

                    if not self.detectedFlag:
                        self.isMouseSign(keyPoint)

                    if not self.detectedFlag and not self.mouseFlag:
                        self.detectedFlag = self.isDetectSign(keyPoint)
                        if self.detectedFlag:
                            print("start time")
                            self.startTime = time.time()

                    if self.mouseFlag:
                        self.doSign()
                        self.isClickSign(keyPoint)
                    elif self.detectedFlag and self.detectedTime > 2:
                        print("start analysis")
                        self.sign = self.analysis()
                        self.doSign()

                        # reset data
                        self.startTime = 0
                        self.detectedTime = 0
                        self.detectedPoint = []
                        self.detectedFlag = False

                    # sign
                    self.dialog.signLabel.setText("동작 유추: " + str(self.sign))
                    cv2.putText(image, text=str(self.sign), org=(30, 90), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                                fontScale=2,
                                color=(0, 0, 255),
                                thickness=3)

            qImg = QtGui.QImage(image.data, imageWidth, imageHeight, imageWidth * imageColor,
                                QtGui.QImage.Format_BGR888)
            pixmap = QtGui.QPixmap.fromImage(qImg)
            camView.setPixmap(pixmap)

            if cv2.waitKey(5) & 0xFF == 27:
                self.hands.close()
                self.cap.release()
                break

    @staticmethod
    def loadLabel():
        label = {}
        count = 1
        list_labels = ['back', 'lock', 'next', 'unlock', 'volumeDown', 'volumeUp']
        # list_labels = ['back', 'lock', 'next', 'unlock']
        for l in list_labels:
            label[l] = count
            count += 1
        return label

    def loadData(self):
        X = []

        for _ in range(len(self.detectedPoint), 12600):
            self.detectedPoint.extend([0.000])  # 300 frame 고정

        row = 42 * 8  # 앞의 8프레임 제거 // 336
        landmarkFrame = []

        for i in range(0, 70):  # 총 100프레임으로 고정
            landmarkFrame.extend(self.detectedPoint[row:row + 84])
            row += 84

        landmarkFrame = np.array(landmarkFrame)

        # print('before reshape : {0}'.format(landmark_frame.shape))
        landmarkFrame = landmarkFrame.reshape(-1, 84)  # 2차원으로 변환(260*42)

        X.append(np.array(landmarkFrame))

        xTrain = np.array(np.array(X))

        return xTrain

    def analysis(self):
        print("start analysis")

        xTest = self.loadData()
        labels = self.loadLabel()

        xHat = xTest
        yHat = self.model.predict(xHat)

        predictions = np.array([np.argmax(pred) for pred in yHat])
        revLabels = dict(zip(list(labels.values()), list(labels.keys())))

        print(revLabels[predictions[0]])

        return revLabels[predictions[0]]

    def doSign(self):
        if self.sign == 'lock':
            self.lockFlag = True
            self.sign = "lock"
        elif self.sign == 'unlock':
            self.lockFlag = False
            self.sign = "unlock"

        if not self.lockFlag:
            if self.sign == 'next':
                AppDemo.AppDemo.ppt.goToNext()
            elif self.sign == 'back':
                AppDemo.AppDemo.ppt.goToBack()
            elif self.sign == 'volumeDown':
                AppDemo.AppDemo.ppt.volumeDown()
            elif self.sign == 'volumeUp':
                AppDemo.AppDemo.ppt.volumeUp()
            elif self.sign == 'moveMouse':
                AppDemo.AppDemo.ppt.moveMouse(self.cap, self.indexFingerTip)
            elif self.sign == 'click':
                AppDemo.AppDemo.ppt.mouseClick()

    def isDetectSign(self, point):
        if abs(point[4]['x'] - point[9]['x']) < 0.005:
            self.sign = None
            return True
        return False

    def isMouseSign(self, point):
        if self.sign == "lock":
            return
        if point[4]['x'] <= point[3]['x'] <= point[2]['x'] <= point[1]['x'] and point[5]['x'] < point[9]['x'] <= \
                point[13]['x'] <= point[17]['x'] and \
                point[8]['y'] <= point[7]['y'] <= point[6]['y'] and \
                point[12]['y'] >= point[11]['y'] >= point[10]['y'] and point[16]['y'] >= point[15]['y'] >= point[14][
            'y'] and \
                point[20]['y'] >= point[19]['y'] >= point[18]['y']:
            self.mouseFlag = True
            self.sign = "moveMouse"
        elif point[4]['x'] >= point[3]['x'] and point[3]['x'] <= point[2]['x'] <= point[1]['x'] <= point[0]['x'] and \
                point[8]['y'] >= point[7]['y'] >= point[6]['y'] and \
                point[12]['y'] >= point[11]['y'] >= point[10]['y'] and point[16]['y'] >= point[15]['y'] >= point[14][
            'y'] and \
                point[20]['y'] >= point[19]['y'] >= point[18]['y']:
            self.mouseFlag = False
            self.sign = "endMouse"

    def isClickSign(self, point):
        print("isClickSign")
        if point[5]['x'] <= point[4]['x'] <= point[0]['x'] and point[4]['x'] >= point[1]['x'] and \
                point[5]['x'] < point[9]['x'] <= point[13]['x'] <= point[17]['x'] and \
                point[8]['y'] <= point[7]['y'] <= point[6]['y'] <= point[5]['y'] and \
                point[12]['y'] >= point[11]['y'] >= point[10]['y'] and point[16]['y'] >= point[15]['y'] >= point[14][
            'y'] and \
                point[20]['y'] >= point[19]['y'] >= point[18]['y']:
            print("click")
            self.sign = "click"
            self.doSign()
