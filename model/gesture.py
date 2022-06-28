import autopy
from utils.utils import distance3d, percentageOfNumber
import pyautogui

class Gesture:
    def __init__(self, landmarks):
        self.landmarks = landmarks
        self.screen_width, self.screen_height = autopy.screen.size()
        self.mouse_sensitivity = 50
        self.percentage = 20

    def get_poining_fingertip_coordinatees(self):
        return (self.landmarks[8][1], self.landmarks[8][2])

    def fingers_flags(self):
        tip_ids = [8, 12, 16, 20]  # Indexes for the tips of each finger
        fingertips = []  # To store 4 sets of 1s or 0s

        for index in range(4):
                if self.landmarks[tip_ids[index]][2] < self.landmarks[tip_ids[index] - 3][2]:  # Checks to see if the tip of the finger is higher than the joint
                    fingertips.append(1)
                else:
                    fingertips.append(0)

        return fingertips

    def move_mouse(self, current_x, current_y):
        if self.fingers_flags() == [1, 0, 0, 0]:
            autopy.mouse.move(self.screen_width - current_x, current_y) 
    
    def mouse_left_click(self):
        p = self.landmarks[4][1:]
        q = self.landmarks[8][1:]
        if distance3d(p, q) < percentageOfNumber(distance3d(self.landmarks[0][1:], self.landmarks[1][1:]), self.percentage) :
            pyautogui.click(button='left')  # Left click
    
    def mouse_middle_click(self):
        p = self.landmarks[4][1:]
        q = self.landmarks[16][1:]
        if distance3d(p, q) < percentageOfNumber(distance3d(self.landmarks[0][1:], self.landmarks[1][1:]), self.percentage) :
            pyautogui.click(button='middle')  # Middle click

    def mouse_right_click(self):
        p = self.landmarks[4][1:]
        q = self.landmarks[12][1:]
        if distance3d(p, q) < percentageOfNumber(distance3d(self.landmarks[0][1:], self.landmarks[1][1:]), self.percentage) :
            pyautogui.click(button='right')  # Right click

    def mouse_left_double_click(self):
        p = self.landmarks[4][1:]
        q = self.landmarks[7][1:]
        if distance3d(p, q) < percentageOfNumber(distance3d(self.landmarks[0][1:], self.landmarks[1][1:]), self.percentage):
            pyautogui.click(button='left', clicks=2)  # Left double click

    def mouse_left_triple_click(self):
        p = self.landmarks[4][1:]
        q = self.landmarks[6][1:]
        if distance3d(p, q) < percentageOfNumber(distance3d(self.landmarks[0][1:], self.landmarks[1][1:]), self.percentage):
            pyautogui.click(button='left', clicks=3)  # Left triple click
    
    def mouse_scroll(self, current_x, current_y):
        if self.fingers_flags() == [1, 1, 0, 0]:
            pyautogui.vscroll(10)
    



