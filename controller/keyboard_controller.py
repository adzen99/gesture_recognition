import cv2
from model.key import Key
from model.handtracker import HandTracker
from pynput.keyboard import Controller
import time
from utils.utils import distance2d

class KeyboardController:
    def __init__(self):
        self.mouse_x, self.mouse_y = 0, 0
        self.clicked_x, self.clicked_y = 0, 0

    def get_mouse_pos(self, event , x, y):
        if event == cv2.EVENT_LBUTTONUP:
            self.clicked_x, self.clicked_y = x, y
        if event == cv2.EVENT_MOUSEMOVE:
            self.mouse_x, self.mouse_y = x, y

    def create_keyboard(self):
        w, h = 80, 60
        start_x, start_y = 40, 150
        keys = []
        letters = list("QWERTYUIOPASDFGHJKLZXCVBNM")
        for i, l in enumerate(letters):
            if i < 10:
                keys.append(Key(start_x + i*w + i*5, start_y, w, h, l))
            elif i < 19:
                keys.append(Key(start_x + (i-10)*w + i*5, start_y + h + 5, w, h, l))
            else:
                keys.append(Key(start_x + (i-19)*w + i*5, start_y + 2*h + 10, w, h, l))
        keys.append(Key(start_x+25, start_y+3*h+15, 5*w, h, "space"))
        keys.append(Key(start_x+8*w + 50, start_y+2*h+10, w, h, "clear"))
        keys.append(Key(start_x+5*w+30, start_y+3*h+15, 5*w, h, "delete"))

        show_key = Key(300,5,80,50, 'Show')
        exit_key = Key(300,65,80,50, 'Exit')
        text_box = Key(start_x, start_y-h-5, 10*w+9*5, h,'')

        cap = cv2.VideoCapture(0)

        # initiating the hand tracker
        handtracker = HandTracker()

        frame_height, frame_width, _ = cap.read()[1].shape

        cv2.namedWindow('video')
        counter = 0
        previous_click = 0

        keyboard = Controller()

        while True:
            _, img = cap.read()  
            if counter >0:
                counter -=1
            
            sign_tip1_x = 0
            sign_tip1_y = 0

            sign_tip2_x = 0
            sign_tip2_y = 0

            ret, frame = cap.read()
            if not ret:
                break
            frame = cv2.resize(frame,(int(frame_width*1.5), int(frame_height*1.5)))
            #find hands
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) 
            landmarks = handtracker.hand_landmarks(frame, img_rgb)
            if landmarks:
                sign_tip1_x, sign_tip1_y = landmarks[8][1], landmarks[8][2]
                sign_tip2_x, sign_tip2_y = landmarks[12][1], landmarks[12][2]
                if distance2d((sign_tip1_x, sign_tip1_y), (sign_tip2_x, sign_tip2_y)) < 5:
                    center_x = int((sign_tip1_x+sign_tip2_x)/2)
                    center_y = int((sign_tip1_y + sign_tip2_y)/2)
                    cv2.line(frame, (sign_tip1_x, sign_tip1_y), (sign_tip2_x, sign_tip2_x), (0,255,0),2)
                    cv2.circle(frame, (center_x, center_y), 5, (0,255,0), cv2.FILLED)

            ctime = time.time()
            cv2.setMouseCallback('video', self.get_mouse_pos)

            #checking if sign finger is over a key and if click happens
            alpha = 0.5
            text_box.draw_key(frame, (255,255,255), (0,0,0), 0.3)
            for k in keys:
                if k.is_over(self.mouse_x, self.mouse_y) or k.is_over(sign_tip1_x, sign_tip1_y):
                    alpha = 0.1
                    # writing using mouse right click
                    if k.is_over(self.clicked_x, self.clicked_y):                              
                        if k.text == 'delete':
                            text_box.text = text_box.text[:-1]
                        elif k.text == 'clear':
                            text_box.text = ''
                        elif len(text_box.text) < 30:
                            if k.text == 'space':
                                text_box.text += " "
                            else:
                                text_box.text += k.text
                                
                    # writing using fingers
                    if (k.is_over(sign_tip2_x, sign_tip2_y)):
                        click_time = time.time()
                        if click_time - previous_click > 0.4:                               
                            if k.text == 'delete':
                                text_box.text = text_box.text[:-1]
                            elif k.text == 'clear':
                                text_box.text = ''
                            elif len(text_box.text) < 30:
                                if k.text == 'space':
                                    text_box.text += " "
                                else:
                                    text_box.text += k.text
                                    keyboard.press(k.text)
                            previous_click = click_time
                k.draw_key(frame,(255,255,255), (0,0,0), alpha=alpha)
                alpha = 0.5
            self.clicked_x, self.clicked_x = 0, 0        
            ptime = ctime
            cv2.imshow('video', frame)

            # stop the video when 'q' is pressed
            pressed_key = cv2.waitKey(1)
            if pressed_key == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

