

from matplotlib.pyplot import text
from calculator_controller import CalculatorController
from handtracker import HandTracker
from gui import GUI
from keyboard_controller import KeyboardController
import os
import dotenv
from mouse_controller import MouseController
from calculator_controller import CalculatorController

def main():

    gui = GUI(width=800, height=600, title='Gesture hand commands')
    mouse_controller = MouseController()
    keyboard_controller = KeyboardController()
    calculator_controller = CalculatorController()

    gui.create_button('Mouse controller', mouse_controller.actions)
    gui.create_button('Keyboard controller', keyboard_controller.create_keyboard)
    gui.create_button('Calculator controller', calculator_controller.display)

    gui.create_button('Options', gui.options_popup)
    gui.create_button('User manual', gui.options_popup)

    gui.display_gui()

main()