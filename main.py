

from matplotlib.pyplot import text
from handtracker import HandTracker
from gui import GUI
from keyboard_controller import KeyboardController
import os
import dotenv
from mouse_controller import MouseController

def main():

    # dotenv.load_dotenv()
    
    # dotenv.set_key(dotenv.find_dotenv(), "A_B", "ABC12343")
    # dotenv.set_key(dotenv.find_dotenv(), "A_B_C", "134")

    # print(os.environ['A_B_C'])

    gui = GUI(width=800, height=600, title='Gesture hand commands')
    mouse_controller = MouseController()
    # keyboard_controller = KeyboardController()

    gui.create_button('Mouse controller', mouse_controller.actions)
    # gui.create_button('Keyboard controller', keyboard_controller.create_keyboard)

    gui.create_button('Options', gui.options_popup)
    gui.create_button('User manual', gui.options_popup)

    gui.display_gui()

main()