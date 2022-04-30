import cv2
import numpy
from handtracker import HandTracker
from calculator_gesture import CalculatorGesture
from key import Key
import time

class CalculatorController:
    def __init__(self):
        pass

    def display(self):
        handtracker = HandTracker()
        text_box = Key(50, 400, 500, 100,'')

        cap = cv2.VideoCapture(0)
        count = 0
        while True:
            _, img = cap.read()  
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) 
            landmarks = handtracker.hand_landmarks(img, img_rgb)
            text_box.draw_key(img, (255,255,255), (0,0,0), 0.3)

            if(landmarks):
                calculator_gesture = CalculatorGesture(landmarks)
                if count % 30 == 0:
                    operation = calculator_gesture.operation()
                    if operation:
                        text_box.text += operation;
                    else:
                        text_box.text += str(calculator_gesture.fingers_flags())

            cv2.imshow("Webcam", img)
            if cv2.waitKey(5) & 0xFF == 27:
                break
            count += 1
            