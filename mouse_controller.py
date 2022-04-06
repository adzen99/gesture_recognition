import numpy
import cv2
import autopy
from gesture import Gesture
from handtracker import HandTracker

class MouseController:

    def actions(self):
        handtracker = HandTracker()
        screen_width, screen_height = autopy.screen.size()
        previous_x, previous_y, current_x, current_y = 0, 0, 0, 0
        cap = cv2.VideoCapture(0)
        while True:
            _, img = cap.read()  
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) 
            landmarks = handtracker.hand_landmarks(img, img_rgb)
            if(landmarks):
                gesture = Gesture(landmarks)
                
                x, y = landmarks[8][1:3]

                x2 = numpy.interp(x, (75, 640 - 75), (0, screen_width)) 
                y2 = numpy.interp(y, (75, 480 - 75), (0, screen_height))  
                
                current_x = previous_x + (x2 - previous_x) / 7  
                current_y = previous_y + (y2 - previous_y) / 7

                gesture.move_mouse(current_x, current_y)
                gesture.mouse_scroll(current_x, current_y)
                previous_x, previous_y = current_x, current_y
                
                gesture.mouse_left_click()
                gesture.mouse_right_click()
                gesture.mouse_middle_click()
                gesture.mouse_left_double_click()
            cv2.imshow("Webcam", img)
            if cv2.waitKey(5) & 0xFF == 27:
                break