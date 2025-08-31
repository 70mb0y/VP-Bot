import pyautogui
import time

print("Move your mouse to a button/area within 5 seconds...")

time.sleep(10)  # give you time to move your mouse

# Capture and print current mouse position
x, y = pyautogui.position()
print(f"Mouse position: ({x}, {y})")
