import cv2
import mediapipe
import numpy
import autopy

from gesture import Gesture

class HandTracker:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.init_hand = mediapipe.solutions.hands
        self.main_hand = self.init_hand.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.5)
        self.draw = mediapipe.solutions.drawing_utils
        self.screen_width, self.screen_height = autopy.screen.size()
        
    def hand_landmarks(self, img, color_img):
        landmark_list = []

        landmark_positions = self.main_hand.process(color_img)
        landmark_check = landmark_positions.multi_hand_landmarks
        if landmark_check:  
            for hand in landmark_check: 
                for index, landmark in enumerate(hand.landmark): 
                    # img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
                    self.draw.draw_landmarks(img, hand, self.init_hand.HAND_CONNECTIONS) 
                    h, w, c = img.shape 
                    center_x, center_y = int(landmark.x * w), int(landmark.y * h)  
                    landmark_list.append([index, center_x, center_y, landmark.z])
        return landmark_list
        
    def show(self):
        previous_x, previous_y, current_x, current_y = 0, 0, 0, 0
        while True:
            check, img = self.cap.read()  
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) 
            landmarks = self.hand_landmarks(img, img_rgb)
            if(landmarks):
                gesture = Gesture(landmarks)
                
                x, y = landmarks[8][1:3]

                x2 = numpy.interp(x, (75, 640 - 75), (0, self.screen_width)) 
                y2 = numpy.interp(y, (75, 480 - 75), (0, self.screen_height))  
                
                current_x = previous_x + (x2 - previous_x) / 7  
                current_y = previous_y + (y2 - previous_y) / 7

                gesture.move_mouse(current_x, current_y)
                previous_x, previous_y = current_x, current_y
                
                gesture.mouse_right_click()
                gesture.mouse_left_click()

            cv2.imshow("Webcam", img)
            if cv2.waitKey(5) & 0xFF == 27:
                break




