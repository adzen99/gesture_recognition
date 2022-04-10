import cv2
import numpy
class Key:
    def __init__(self, x, y, w, h, text):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.text = text
    
    def draw_key(self, img, text_color = (255, 255, 255), bg_color = (0, 0, 0), alpha = 0.5, font_face = cv2.FONT_HERSHEY_SIMPLEX, font_scale = 0.8, thickness = 2):
        # draw the box

        bg_rec = img[self.y : self.y + self.h, self.x : self.x + self.w]
        white_rect = numpy.ones(bg_rec.shape, dtype = numpy.uint8)
        white_rect[:] = bg_color
        res = cv2.addWeighted(bg_rec, alpha, white_rect, 1-alpha, 1.0)

        # putting the image back to its position
        img[self.y : self.y + self.h, self.x : self.x + self.w] = res

        #put the letter
        tetx_size = cv2.getTextSize(self.text, font_face, font_scale, thickness)
        text_pos = (int(self.x + self.w/2 - tetx_size[0][0]/2), int(self.y + self.h/2 + tetx_size[0][1]/2))
        cv2.putText(img, self.text,text_pos , font_face, font_scale,text_color, thickness)

    def is_over(self,x,y):
        if (self.x + self.w > x > self.x) and (self.y + self.h> y >self.y):
            return True
        return False
