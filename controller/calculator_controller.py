import cv2
import numpy
from model.handtracker import HandTracker
from model.calculator_gesture import CalculatorGesture
from model.key import Key
import time

class CalculatorController:
    def __init__(self):
        pass

    def display(self):
        handtracker = HandTracker()
        text_box = Key(50, 400, 550, 100, '')

        cap = cv2.VideoCapture(0)
        count = 0
        while True:
            _, img = cap.read()  
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) 
            landmarks = handtracker.hand_landmarks(img, img_rgb)
            text_box.draw_key(img, (255,255,255), (0,0,0), 0.3)

            if(landmarks):
                calculator_gesture = CalculatorGesture(landmarks)
                if count and count % 10 == 0:
                    operation = calculator_gesture.operation()
                    floating_point = calculator_gesture.floating_point()
                    del_character = calculator_gesture.del_character()
                    if operation:
                        if operation == '=':
                            text_box.text = str(eval(text_box.text))
                        else:
                            text_box.text += operation;
                            count = 0
                    elif floating_point:
                        text_box.text += floating_point;
                        count = 0
                    elif del_character:
                        text_box.text = text_box.text[:-1]
                        count = 0
                    else:
                        text_box.text += str(calculator_gesture.fingers_flags())
                        count = 0
                count += 0.5
            else:
                count = 0
            cv2.imshow("Webcam", img)
            if cv2.waitKey(5) & 0xFF == 27:
                break
            
            