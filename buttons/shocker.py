import pyautogui
import threading
import time
from pynput.mouse import Listener

# Global variable to track the state of the mouse button
clicking = False

# Function to perform clicking at 10 clicks per second
def click_mouse():
    while clicking:
        pyautogui.click()
        time.sleep(0.1)  # 10 clicks per second = 0.1s per click

# Function to start clicking when the mouse button is pressed
def on_click(x, y, button, pressed):
    global clicking
    if pressed:
        if not clicking:
            clicking = True
            threading.Thread(target=click_mouse).start()  # Start the clicking thread
    else:
        clicking = False  # Stop clicking when the button is released

# Start the mouse listener
with Listener(on_click=on_click) as listener:
    listener.join()
