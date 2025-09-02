import pyautogui
import time

# --- CONFIG ---
x, y = 937, 295    # Starting position (where to click and hold)
drag_distance = 600 # Pixels to drag down
drag_duration = 0.5 # Seconds to drag
repeats = 6         # Number of drags

# Small delay before starting
time.sleep(2)

for i in range(repeats):
    # Move to the starting position each time
    pyautogui.moveTo(x, y, duration=0.5)

    # Click and drag down
    pyautogui.mouseDown()
    pyautogui.moveRel(0, drag_distance, duration=drag_duration)
    pyautogui.mouseUp()

    time.sleep(0.3)  # small pause before next drag
