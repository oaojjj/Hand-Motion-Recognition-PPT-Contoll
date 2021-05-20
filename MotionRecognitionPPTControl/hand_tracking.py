import time

import cv2
import mediapipe as mp
import numpy as np
import PPTController

from tensorflow.keras.models import load_model

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

# 모델 불러오기
global model

# For webcam input:
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.5, min_tracking_confidence=0.5)
cap = cv2.VideoCapture(0)

def hand_recognition(point):
    sign = None
    if point[3]['y'] >= point[4]['y'] >= point[8]['y'] and point[6]['y'] >= point[10]['y'] and \
            point[6]['y'] >= point[14]['y'] and point[20]['y'] <= point[19]['y']:
        sign = 'ok_sign'
    elif (point[7]['y'] <= point[14]['y']) and (point[6]['y'] <= point[18]['y']) and \
            (point[11]['y'] <= point[14]['y']) and (point[10]['y'] <= point[18]['y']) and \
            (point[16]['y'] >= point[15]['y']) and (point[20]['y'] >= point[19]['y']) and \
            (point[2]['x'] <= point[4]['x']):
        sign = 'v_sign'
    elif point[3]['y'] <= point[5]['y'] and point[8]['x'] >= point[6]['x'] and point[12]['x'] >= point[10]['x'] and \
            point[16]['x'] >= point[14]['x'] and point[20]['x'] >= point[18]['x']:
        sign = 'thumb_up_sign'
    elif point[4]['y'] >= point[3]['y'] >= point[2]['y'] >= point[5]['y'] >= point[9]['y'] >= point[13]['y']:
        sign = 'thumb_down_sign'

    elif point[4]['x'] <= point[3]['x'] <= point[2]['x'] <= point[1]['x'] and point[5]['x'] < point[9]['x'] <= point[13]['x'] <= point[17]['x'] and \
        point[8]['y'] <= point[7]['y'] <= point[6]['y'] and \
        point[12]['y'] >= point[11]['y'] >= point[10]['y'] and point[16]['y'] >= point[15]['y'] >= point[14]['y'] and \
        point[20]['y'] >= point[19]['y'] >= point[18]['y']:
        sign = 'start_sign'

    elif point[4]['x'] >= point[3]['x'] and point[3]['x'] <= point[2]['x'] <= point[1]['x'] <= point[0]['x'] and \
            point[8]['y'] >= point[7]['y'] >= point[6]['y'] and \
            point[12]['y'] >= point[11]['y'] >= point[10]['y'] and point[16]['y'] >= point[15]['y'] >= point[14]['y'] and \
            point[20]['y'] >= point[19]['y'] >= point[18]['y']:
            sign = 'end_sign'

    elif point[4]['x'] >= point[5]['x'] and point[4]['x'] >= point[1]['x'] and point[4]['x']<= point[0]['x'] and \
            point[5]['x'] < point[9]['x'] <= point[13]['x'] <= point[17]['x'] and \
            point[8]['y'] <= point[7]['y'] <= point[6]['y'] <= point[5]['y'] and \
            point[12]['y'] >= point[11]['y'] >= point[10]['y'] and point[16]['y'] >= point[15]['y'] >= point[14]['y'] and \
            point[20]['y'] >= point[19]['y'] >= point[18]['y']:
            sign = 'click_sign'
    return sign

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
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # x,y,z 좌표 얻기
            for data_point in hand_landmarks.landmark:
                key_point.append({'point': point, 'x': data_point.x, 'y': data_point.y})
                point += 1

            sign = hand_recognition(key_point)

            # sign
            cv2.putText(image, text=str(sign), org=(30, 90), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                        fontScale=2,
                        color=(0, 0, 255),
                        thickness=3)

    cv2.imshow('MediaPipe Hands', image)
    if cv2.waitKey(5) & 0xFF == 27:
        break



hands.close()
cap.release()