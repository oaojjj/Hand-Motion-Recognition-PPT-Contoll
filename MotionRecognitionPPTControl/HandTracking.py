import cv2
import mediapipe as mp

from tensorflow.python.keras.models import load_model


class HandTracking:
    MODEL_NAME = "new_model.h5"
    MP_DRAWING = mp.solutions.drawing_utils
    MP_HANDS = mp.solutions.hands

    def __init__(self):
        self.model = load_model("model/" + self.MODEL_NAME)
