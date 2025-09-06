import re
import time
import cv2
import numpy as np
import pyautogui
import pytesseract
from PIL import ImageGrab
from rapidfuzz import fuzz, process

time.sleep(5)  # small delay before script starts to allow navigation to game screen

# --- CONFIG ---
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

approved_names = ["RomO", "LODZ", "Vudu", "GroW", "BEQI", "DKSI", "DkCy", "xESE", "BAMF", "K4BR"]

# Slots to process
slots = [
    (681, 383),  # Slot 2 Strategy
    (786, 392),  # Slot 3 Defense
    (573, 518),  # Slot 4 Development
    (683, 523),  # Slot 5 Science
    (790, 519),  # Slot 6 Interior
]

# Buttons (calibrate these)
list_button   = (815, 617)
approve_btn   = (764, 217)
reject_btn    = (812, 217)
exit_btn      = (836, 134)
close_confirm = (746, 516)

# Region where a single name appears (x, y, width, height)
list_region = (595, 200, 50, 20)  # slightly larger for OCR

# Behavior toggles / thresholds
REJECT_UNKNOWN = True  # Reject names not in the whitelist
FUZZ_THRESHOLD = 60    # minimum similarity to count as approved

# --- CONFIG ---
drag_x, drag_y = 663, 200         # Starting position (where to click and hold)
drag_distance = 500     # Pixels to drag down
drag_duration = 0.5     # Seconds to drag
drag_repeats = 6        # Number of drags

# --- HELPERS ---

def read_name_from_region():
    """
    Capture slot region and OCR with minimal preprocessing.
    Returns (detected_name, avg_conf) or (None, 0.0)
    """
    x, y, w, h = list_region
    shot = ImageGrab.grab(bbox=(x, y, x + w, y + h))

    # Convert to OpenCV, grayscale, upscale
    img_cv = cv2.cvtColor(np.array(shot), cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)

    scale_factor = 4
    gray = cv2.resize(gray, None, fx=scale_factor, fy=scale_factor, interpolation=cv2.INTER_CUBIC)

    # Optional: slight blur to reduce noise
    gray = cv2.medianBlur(gray, 3)

    # OCR using Tesseract
    config = "--psm 7 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
    data = pytesseract.image_to_data(gray, output_type=pytesseract.Output.DICT, config=config)

    tokens = []
    # Debug: print all OCR tokens
    for txt, conf in zip(data['text'], data['conf']):
        print(f"OCR token: {txt!r}, conf: {conf}")
        if txt and txt.strip():
            tokens.append(txt.strip())

    if not tokens:
        return None, 0.0

    raw = " ".join(tokens)
    clean = re.sub(r"[^A-Za-z0-9]", "", raw)
    return clean if clean else None, 0.0

def match_to_whitelist(ocr_name):
    """
    Fuzzy match OCR output against whitelist.
    Returns (matched_name, score) or (None, 0)
    """
    result = process.extractOne(ocr_name, approved_names, scorer=fuzz.ratio)
    if not result:
        return None, 0
    match, score, _ = result
    if score >= FUZZ_THRESHOLD:
        return match, score
    return None, score

def exit_back():
    """Consistent exit sequence used in multiple places."""
    pyautogui.click(exit_btn)
    time.sleep(4)
    pyautogui.click(exit_btn)
    time.sleep(4)

# --- CORE FLOW ---

def process_slot(slot_pos):
    # Enter slot
    pyautogui.click(slot_pos)
    time.sleep(4)

    # Open List pane
    pyautogui.click(list_button)
    time.sleep(4)

    # >>> Perform 6 drag motions down <<<
    for i in range(drag_repeats):
        pyautogui.moveTo(drag_x, drag_y, duration=.03)
        pyautogui.mouseDown()
        pyautogui.moveRel(0, drag_distance, duration=drag_duration)
        pyautogui.mouseUp()
        time.sleep(.5)

    # Read name
    for i in range(5):
        name, conf = read_name_from_region()
        print(f"Detected name: {name!r}")

        if not name:
            print("⚠️ No valid name detected — skipping.")
            exit_back()
            return

        matched, score = match_to_whitelist(name)
        if matched:
            pyautogui.click(approve_btn)
            print(f"✅ Approved (OCR: '{name}' → '{matched}', score={score})")
            time.sleep(4)
        else:
            print(f"❌ Not in whitelist (OCR: '{name}')")
            if REJECT_UNKNOWN:
                pyautogui.click(reject_btn)
                time.sleep(4)
                pyautogui.click(close_confirm)
                time.sleep(4)
    time.sleep(0.5)

    # Exit back to main screen
    exit_back()

# --- MAIN LOOP ---

while True:
    for slot in slots:
        process_slot(slot)
    time.sleep(15)
