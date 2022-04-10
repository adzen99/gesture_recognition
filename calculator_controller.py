import cv2
import numpy
from handtracker import HandTracker
from gesture import Gesture

class CalculatorController:
    def __init__(self):
        pass

    def display(self):
        cap = cv2.VideoCapture(0)
        handtracker = HandTracker()
        draw_color = (255, 0, 0)
        img_canvas = numpy.zeros((480, 640, 3), numpy.uint8)
        xp, yp = 0, 0
        while True:
            _, img = cap.read()
            img = cv2.flip(img, 1)

            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) 
            landmarks = handtracker.hand_landmarks(img, img_rgb)
            if landmarks:
                gesture = Gesture(landmarks=landmarks)
                x1, y1 = landmarks[8][1:3]
                x2, y2 = landmarks[12][1:3]
                if gesture.fingers_flags() == [1, 0, 0, 0]:
                    if xp == 0 and yp == 0:
                        xp, yp = x1, y1
                    cv2.line(img, (xp, yp), (x1, y1), draw_color, 15)
                    cv2.line(img_canvas, (xp, yp), (x1, y1), draw_color, 15)
                    xp, yp = x1, y1
                else:
                    xp, yp = 0, 0
                
            img = cv2.addWeighted(img, 0.5, img_canvas, 0.5, 0)
            cv2.imshow("Image", img)
            if cv2.waitKey(5) & 0xFF == 27:
                break