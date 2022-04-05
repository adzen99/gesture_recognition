import cv2
from key import Key
from handtracker import HandTracker
from pynput.keyboard import Controller
import time
from utils import distance

class KeyboardController:
    def __init__(self):
        self.mouse_x, self.mouse_y = 0, 0
        self.clicked_x, self.clicked_y = 0, 0

    def get_mouse_pos(self, event , x, y, flags, param):
        if event == cv2.EVENT_LBUTTONUP:
            self.clicked_x, self.clicked_y = x, y
        if event == cv2.EVENT_MOUSEMOVE:
            self.mouse_x, self.mouse_y = x, y

    def create_keyboard(self):
        w, h = 80, 60
        start_x, start_y = 40, 200
        keys = []
        letters = list("QWERTYUIOPASDFGHJKLZXCVBNM")
        for i, l in enumerate(letters):
            if i < 10:
                keys.append(Key(start_x + i*w + i*5, start_y, w, h, l))
            elif i < 19:
                keys.append(Key(start_x + (i-10)*w + i*5, start_y + h + 5, w, h, l))
            else:
                keys.append(Key(start_x + (i-19)*w + i*5, start_y + 2*h + 10, w, h, l))
        keys.append(Key(start_x+25, start_y+3*h+15, 5*w, h, "Space"))
        keys.append(Key(start_x+8*w + 50, start_y+2*h+10, w, h, "clr"))
        keys.append(Key(start_x+5*w+30, start_y+3*h+15, 5*w, h, "<--"))

        show_key = Key(300,5,80,50, 'Show')
        exit_key = Key(300,65,80,50, 'Exit')
        textBox = Key(start_x, start_y-h-5, 10*w+9*5, h,'')

        cap = cv2.VideoCapture(0)
        ptime = 0

        # initiating the hand tracker
        handtracker = HandTracker()

        # getting frame's height and width
        frame_height, frame_width, _ = cap.read()[1].shape
        show_key.x = int(frame_height*1.5) - 85
        exit_key.x = int(frame_height*1.5) - 85

        clicked_x, clicked_y = 0, 0
        mouse_x, mouse_y = 0, 0

        show = False
        cv2.namedWindow('video')
        counter = 0
        previous_click = 0

        keyboard = Controller()

        while True:
            if counter >0:
                counter -=1
            
            sign_tip_x = 0
            sign_tip_y = 0

            thumb_tip_x = 0
            thumb_tip_y = 0

            ret, frame = cap.read()
            if not ret:
                break
            frame = cv2.resize(frame,(int(frame_width*1.5), int(frame_height*1.5)))
            frame = cv2.flip(frame, 1)
            #find hands
            frame = handtracker.findHands(frame)
            landmarks = handtracker.hand_landmarks(frame, draw=False)
            if landmarks:
                sign_tip_x, sign_tip_y = landmarks[8][1], landmarks[8][2]
                thumb_tip_x, thumb_tip_y = landmarks[4][1], landmarks[4][2]
                if distance((sign_tip_x, sign_tip_y), (thumb_tip_x, thumb_tip_y)) <50:
                    centerX = int((sign_tip_x+thumb_tip_x)/2)
                    centerY = int((sign_tip_y + thumb_tip_y)/2)
                    cv2.line(frame, (sign_tip_x, sign_tip_y), (thumb_tip_x, thumb_tip_y), (0,255,0),2)
                    cv2.circle(frame, (centerX, centerY), 5, (0,255,0), cv2.FILLED)

            ctime = time.time()
            fps = int(1/(ctime-ptime))

            cv2.putText(frame,str(fps) + " FPS", (10,20), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,0),2)
            show_key.drawKey(frame,(255,255,255), (0,0,0),0.1, font_scale=0.5)
            exit_key.drawKey(frame,(255,255,255), (0,0,0),0.1, font_scale=0.5)
            cv2.setMouseCallback('video', self.get_mouse_pos)

            if show_key.isOver(self.clicked_x, self.clicked_x):
                show = not show
                show_key.text = "Hide" if show else "Show"
                self.clicked_x, self.clicked_y = 0, 0

            if exit_key.isOver(self.clicked_x, self.clicked_y):
                #break
                exit()

            #checking if sign finger is over a key and if click happens
            alpha = 0.5
            if show:
                textBox.drawKey(frame, (255,255,255), (0,0,0), 0.3)
                for k in keys:
                    if k.isOver(self.mouse_x, self.mouse_y) or k.isOver(sign_tip_x, sign_tip_y):
                        alpha = 0.1
                        # writing using mouse right click
                        if k.isOver(self.clicked_x, self.clicked_y):                              
                            if k.text == '<--':
                                textBox.text = textBox.text[:-1]
                            elif k.text == 'clr':
                                textBox.text = ''
                            elif len(textBox.text) < 30:
                                if k.text == 'Space':
                                    textBox.text += " "
                                else:
                                    textBox.text += k.text
                                    
                        # writing using fingers
                        if (k.isOver(thumb_tip_x, thumb_tip_y)):
                            clickTime = time.time()
                            if clickTime - previousClick > 0.4:                               
                                if k.text == '<--':
                                    textBox.text = textBox.text[:-1]
                                elif k.text == 'clr':
                                    textBox.text = ''
                                elif len(textBox.text) < 30:
                                    if k.text == 'Space':
                                        textBox.text += " "
                                    else:
                                        textBox.text += k.text
                                        #simulating the press of actuall keyboard
                                        keyboard.press(k.text)
                                previousClick = clickTime
                    k.drawKey(frame,(255,255,255), (0,0,0), alpha=alpha)
                    alpha = 0.5
                self.clicked_x, self.clicked_x = 0, 0        
            ptime = ctime
            cv2.imshow('video', frame)

            ## stop the video when 'q' is pressed
            pressed_key = cv2.waitKey(1)
            if pressed_key == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

