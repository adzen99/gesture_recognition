

from matplotlib.pyplot import text
from handtracker import HandTracker
from gui import GUI

def main():

    gui = GUI(width=800, height=600, title='Gesture hand commands')
    hand_tracker = HandTracker()

    gui.create_button('Start', hand_tracker.show)
    gui.create_button('Options', gui.options_popup)
    gui.create_button('User manual', gui.options_popup)

    gui.display_gui()
 


main()