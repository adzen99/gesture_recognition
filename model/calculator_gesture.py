import autopy
import numpy
from utils.utils import distance3d
import pyautogui


class CalculatorGesture:
    def __init__(self, landmarks):
        self.landmarks = landmarks

    def fingers_flags(self):
        tip_ids = [8, 12, 16, 20]  # Indexes for the tips of each finger

        fingersUp = 0

        if self.landmarks[4][1] > self.landmarks[3][1]:
            fingersUp += 1

        # try:
        #     if self.landmarks[25][1] > self.landmarks[24][1]:
        #         fingersUp += 1
        # except IndexError:
        #     pass

        for index in range(4):
            
            if self.landmarks[tip_ids[index]][2] < self.landmarks[tip_ids[index] - 3][2]:  # Checks to see if the tip of the finger is higher than the joint
                fingersUp += 1
            try:
                if self.landmarks[tip_ids[index]+21][2] < self.landmarks[tip_ids[index]+21 - 3][2]:  # Checks to see if the tip of the finger is higher than the joint
                    fingersUp += 1
            except IndexError:
                continue
                
        return fingersUp

    def floating_point(self):
        if distance3d(self.landmarks[4][1:], self.landmarks[8][1:]) < 30:
            return '.'
        try:
            if distance3d(self.landmarks[25][1:], self.landmarks[29][1:]) < 30:
                return '.'
        except IndexError:
            return ''
        return ''

    def del_character(self):
        try:
            if distance3d(self.landmarks[4][1:], self.landmarks[25][1:]) < 30:
                return True
        except IndexError:
            return False
        return False
    
    def operation(self):
        if len(self.landmarks) != 42:
            return ''
        if distance3d(self.landmarks[8][1:], self.landmarks[0+21][1:]) < 20 or distance3d(self.landmarks[0][1:], self.landmarks[8+21][1:]) < 20:
            return '+'
        elif distance3d(self.landmarks[12][1:], self.landmarks[0+21][1:]) < 20 or distance3d(self.landmarks[0][1:], self.landmarks[12+21][1:]) < 20:
            return '-'
        elif distance3d(self.landmarks[16][1:], self.landmarks[0+21][1:]) < 20 or distance3d(self.landmarks[0][1:], self.landmarks[16+21][1:]) < 20:
            return '*'
        elif distance3d(self.landmarks[20][1:], self.landmarks[0+21][1:]) < 20 or distance3d(self.landmarks[0][1:], self.landmarks[20+21][1:]) < 20:
            return '/'
        elif distance3d(self.landmarks[4][1:], self.landmarks[0+21][1:]) < 20 or distance3d(self.landmarks[0][1:], self.landmarks[4+21][1:]) < 20:
            return '='
        else:
            return ''
        
            



