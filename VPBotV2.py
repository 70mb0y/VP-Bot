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
pytesseract.pytesseract.tesseract_cmd = r"C:\Users\tesseract.exe"

approved_names = ["RomO", "LODZ", "Vudu", "GroW", "BEQI", "DKSI", "DkCy", "xESE", "BAMF", "K4BR"]

# Slots to process
slots = [
    (957, 537),   # Slot 2 Strategy
    (1107, 551),  # Slot 3 Defense
    (813, 724),   # Slot 4 Development
    (958, 719),   # Slot 5 Science
    (1100, 723),  # Slot 6 Interior
]

# Buttons (calibrate these)
list_button   = (1138, 849)
approve_btn   = (1062, 316)
reject_btn    = (1134, 318)
exit_btn      = (1166, 211)
close_confirm = (1042, 722)

# Region where a single name appears (x, y, width, height)
list_region = (830, 285, 80, 40)  # slightly larger for OCR

# Behavior toggles / thresholds
REJECT_UNKNOWN = True  # Reject names not in the whitelist
FUZZ_THRESHOLD = 60    # minimum similarity to count as approved

# Drag motion config
drag_x, drag_y = 1138, 849  # start near list_button (adjust if needed)
drag_distance = 100         # smaller drag per name so each check moves down
drag_duration = 0.4         # drag speed

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

    # Perform 5 approval/rejection checks in sequence
    for i in range(5):
        name, conf = read_name_from_region()
        print(f"[Check {i+1}/5] Detected name: {name!r}")

        if not name:
            print("⚠️ No valid name detected — skipping this check.")
        else:
            matched, score = match_to_whitelist(name)
            if matched:
                pyautogui.click(approve_btn)
                print(f"✅ Approved (OCR: '{name}' → '{matched}', score={score})")
                time.sleep(2)
            else:
                print(f"❌ Not in whitelist (OCR: '{name}')")
                if REJECT_UNKNOWN:
                    pyautogui.click(reject_btn)
                    time.sleep(2)
                    pyautogui.click(close_confirm)
                    time.sleep(2)

        # Drag down slightly to see the next candidate
        pyautogui.moveTo(drag_x, drag_y, duration=0.2)
        pyautogui.mouseDown()
        pyautogui.moveRel(0, drag_distance, duration=drag_duration)
        pyautogui.mouseUp()
        time.sleep(0.5)  # pause between checks

    # Exit back to main screen
    exit_back()

# --- MAIN LOOP ---

while True:
    for slot in slots:
        process_slot(slot)
    time.sleep(60)
