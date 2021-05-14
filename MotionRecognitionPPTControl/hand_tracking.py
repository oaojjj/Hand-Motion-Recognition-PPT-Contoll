import time

import cv2
import mediapipe as mp
import numpy as np
import pyautogui

import PPTController

from tensorflow.keras.models import load_model

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

# For webcam input:
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.5, min_tracking_confidence=0.5)
cap = cv2.VideoCapture(0)

while cap.isOpened():
    success, image = cap.read()
    if not success:
        print("Ignoring empty camera frame.")
        # If loading a video, use 'break' instead of 'continue'.
        continue

    # Flip the image horizontally for a later selfie-view display, and convert
    # the BGR image to RGB.
    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)

    # To improve performance, optionally mark the image as not writeable to
    # pass by reference.
    image.flags.writeable = False
    results = hands.process(image)

    # Draw the hand annotations on the image.
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    image_height, image_width, _ = image.shape

    point = 0

    if results.multi_hand_landmarks:  # 손이 보이는 순간부터 좌표값 넘어옴
        key_point = []
        indexFingerTip = None

        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            indexFingerTip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]

        # 좌표 객체 얻기
        mousePosition = pyautogui.position()
        windowSize = pyautogui.size()
        cap_x = cap.get(3)
        cap_y = cap.get(4)

        # 화면 전체 크기 확인하기
        print(pyautogui.size())

        # 웹캠 화면 사이즈
        print(cap_x, cap_y)

        # 마우스 x, y 좌표
        # print(position.x)
        # print(position.y)

        # 마우스 이동 ( 현재위치에서 )
        # pyautogui.moveRel(100, 100, 1)

        indexFingerTip_x = int(indexFingerTip.x * cap_x)
        indexFingerTip_y = int(indexFingerTip.y * cap_y)

        print("indexFingerTip_x")
        print(indexFingerTip_x)
        print("indexFingerTip_y")
        print(indexFingerTip_y)

        move_x = windowSize.width / cap_x * indexFingerTip_x
        move_y = windowSize.height / cap_y * indexFingerTip_y
        print(move_x)
        print(move_y)
        pyautogui.moveTo(move_x, move_y)

    cv2.imshow('MediaPipe Hands', image)
    if cv2.waitKey(5) & 0xFF == 27:
        break

hands.close()
cap.release()
