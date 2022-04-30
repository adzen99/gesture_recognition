import cv2
import mediapipe
import numpy
import autopy
import dotenv
import os

from gesture import Gesture

class HandTracker:
    def __init__(self):
        self.init_hand = mediapipe.solutions.hands
        self.main_hand = self.init_hand.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.5)
        self.draw = mediapipe.solutions.drawing_utils
        dotenv.load_dotenv()
        self.flag_landmarks = int(os.environ['DISPLAY_LANDMARKS'])
        
    def hand_landmarks(self, img, color_img):
        landmark_list = []
        
        landmark_positions = self.main_hand.process(color_img)
        landmark_check = landmark_positions.multi_hand_landmarks
        if landmark_check:  
            for hand in landmark_check: 
                for index, landmark in enumerate(hand.landmark): 
                    if not self.flag_landmarks:
                        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
                    self.draw.draw_landmarks(img, hand, self.init_hand.HAND_CONNECTIONS) 
                    h, w, c = img.shape 
                    center_x, center_y = int(landmark.x * w), int(landmark.y * h)  
                    landmark_list.append([index, center_x, center_y, landmark.z])
        return landmark_list
