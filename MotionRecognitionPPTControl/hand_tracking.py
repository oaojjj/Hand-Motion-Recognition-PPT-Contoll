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
model = load_model("model/model_05_09.h5")

# For webcam input:
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.5, min_tracking_confidence=0.5)
cap = cv2.VideoCapture(0)

start_time = 0
detected_time = 0
detected_point = []
detected_flag = False


# ppt = PPTController()


# prediction
def load_label():
    label = {}
    count = 1
    # list_labels = ['back', 'lock', 'next', 'unlock', 'volumeDown', 'volumeUp']
    list_labels = ['back', 'lock', 'next', 'unlock']
    for l in list_labels:
        if "_" in l:
            continue
        label[l] = count
        count += 1
    return label


def load_data():
    global detected_point

    X = []

    for _ in range(len(detected_point), 12600):
        detected_point.extend([0.000])  # 300 frame 고정

    row = 42 * 8  # 앞의 8프레임 제거 // 336
    landmark_frame = []

    for i in range(0, 70):  # 총 100프레임으로 고정
        landmark_frame.extend(detected_point[row:row + 84])
        row += 84

    landmark_frame = np.array(landmark_frame)

    # print('before reshape : {0}'.format(landmark_frame.shape))
    landmark_frame = landmark_frame.reshape(-1, 84)  # 2차원으로 변환(260*42)

    X.append(np.array(landmark_frame))

    X = np.array(X)

    x_train = X
    x_train = np.array(x_train)

    return x_train


def analysis():
    print("start analysis")

    global model

    x_test = load_data()
    labels = load_label()

    xhat = x_test
    yhat = model.predict(xhat)

    predictions = np.array([np.argmax(pred) for pred in yhat])
    rev_labels = dict(zip(list(labels.values()), list(labels.keys())))

    print(rev_labels[predictions[0]])

    return rev_labels[predictions[0]]


global lock_flag
lock_flag = False


def do_something(result_sign):
    global lock_flag

    if result_sign == 'lock':
        lock_flag = True
    elif result_sign == 'unlock':
        lock_flag = False

    if not lock_flag:
        if result_sign == 'next':
            PPTController.go_to_next()
        elif result_sign == 'back':
            PPTController.go_to_back()


sign = 'none'

def is_detect_sign(point):
    if abs(point[4]['x'] - point[9]['x']) < 0.005:
        return True
    return False

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

        if detected_flag:
            detected_time = time.time() - start_time

        # 시간
        cv2.putText(image, text=str(detected_time), org=(30, 30), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1,
                    color=(255, 255, 255),
                    thickness=2)

        key_point = []
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # x,y,z 좌표 얻기
            for data_point in hand_landmarks.landmark:
                detected_point.append(data_point.x)
                detected_point.append(data_point.y)
                key_point.append({'point': point, 'x': data_point.x, 'y': data_point.y})
                point += 1

            if not detected_flag:
                detected_flag = is_detect_sign(key_point)
                if detected_flag:
                    print("start time")
                    start_time = time.time()

            if detected_flag and detected_time > 2:
                sign = analysis()
                # do_something(sign)

                # reset data
                start_time = 0
                detected_time = 0
                detected_point = []
                detected_flag = False

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
