from __future__ import absolute_import, division, print_function, unicode_literals
from keras.models import Sequential
from keras import layers
import numpy as np
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.utils import to_categorical
import random
import os


def make_label(text):
    with open("../../../mediapipe/label.txt", "w") as f:
        f.write(text)
    f.close()


def load_data(dirname):
    if dirname[-1] != '/':
        dirname = dirname + '/'
    listfile = os.listdir(dirname)  # label
    X = []
    Y = []
    XT = []
    YT = []

    for file in listfile:
        if "_" in file:
            continue
        wordname = file  # next, back, lock ....
        textlist = os.listdir(dirname + wordname)  # 좌표 dataset
        k = 0
        for text in textlist:  # 좌표 데이터 하나 씩
            if "DS_" in text:
                continue
            textname = dirname + wordname + "/" + text

            print('textname:{0}'.format(textname))
            with open(textname, mode='r') as t:
                numbers = [float(num) for num in t.read().split()]
                # print('before numbers:{0}'.format(numbers))
                for i in range(len(numbers), 7560):  # #25200 600프레임(600*42)
                    numbers.extend([0.000])
                # print('after numbers:{0}'.format(numbers))
            row = 0
            landmark_frame = []
            for i in range(0, 140):  # (60*42->70)60프레임
                landmark_frame.extend(numbers[row:row + 84])
                row += 84
            landmark_frame = np.array(landmark_frame)
            landmark_frame = list(landmark_frame.reshape(-1, 84))  # 2차원으로 변환(260*42)
            if k % 3 == 2:
                XT.append(np.array(landmark_frame))  # 테스트 데이터 (33%)
                YT.append(wordname)
            else:
                X.append(np.array(landmark_frame))  # 트레이닝 데이터 (66%)
                Y.append(wordname)
            k += 1

    X = np.array(X)  # 테스트 좌표 데이터셋
    Y = np.array(Y)  # 테스트 좌표 라벨
    XT = np.array(XT)  # 트레이닝 좌표 데이터셋
    YT = np.array(YT)  # 트레이닝 좌표 라벨

    print('X:{0}'.format(X))
    print('Y:{0}'.format(Y))
    print('XT:{0}'.format(XT))
    print('YT:{0}'.format(YT))

    tmp = [[x, y] for x, y in zip(X, Y)]
    random.shuffle(tmp)

    tmp1 = [[xt, yt] for xt, yt in zip(XT, YT)]
    random.shuffle(tmp1)

    X = [n[0] for n in tmp]
    Y = [n[1] for n in tmp]
    XT = [n[0] for n in tmp1]
    YT = [n[1] for n in tmp1]

    k = set(Y)
    ks = sorted(k)
    text = ""
    for i in ks:
        text = text + i + " "
    make_label(text)

    s = Tokenizer()
    s.fit_on_texts([text])
    encoded = s.texts_to_sequences([Y])[0]  # 단어:숫자 시퀀스로 변환 dict랑 비슷한듯
    encoded1 = s.texts_to_sequences([YT])[0]
    print('encoded:{0}'.format(encoded))
    print('encoded1:{0}'.format(encoded1))

    one_hot = to_categorical(encoded)
    one_hot2 = to_categorical(encoded1)  # 벡터
    print('one_hot:{0}'.format(one_hot))
    print('one_hot2:{0}'.format(one_hot2))
    # https://wikidocs.net/22647 원핫인코딩 설명

    (x_train, y_train) = X, one_hot
    (x_test, y_test) = XT, one_hot2
    x_train = np.array(x_train)
    y_train = np.array(y_train)
    x_test = np.array(x_test)
    y_test = np.array(y_test)
    return x_train, y_train, x_test, y_test


def build_model(label):
    model = Sequential()
    model.add(layers.LSTM(64, return_sequences=True, input_shape=(70, 84)))
    model.add(layers.LSTM(32, return_sequences=True))
    model.add(layers.LSTM(32))
    model.add(layers.Dense(label, activation='softmax'))
    model.compile(loss='categorical_crossentropy',
                  optimizer='adam',
                  metrics=['accuracy'])
    return model
