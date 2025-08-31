import pytesseract
import pyautogui
from PIL import Image, ImageDraw
import cv2
import numpy as np
import time
from rapidfuzz import fuzz, process  # for fuzzy matching

# Path to Tesseract (update if needed)
pytesseract.pytesseract.tesseract_cmd = r"C:\Users\tesseract.exe"

# List of approved names
approved_names = ["RomO", "LODZ", "Vudu", "GroW", "BEQI", "DKSI", "DkCy", "xESE", "BAMF"]

# Define screen region (x, y, width, height)
name_region = (840, 295, 65, 28)

time.sleep(10)  # give you time to move your mouse

# Grab screenshot
screenshot = pyautogui.screenshot(region=name_region)

# Convert screenshot to OpenCV format
img = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

# Scale image up to improve OCR on small text
scale_factor = 2
img = cv2.resize(img, None, fx=scale_factor, fy=scale_factor, interpolation=cv2.INTER_CUBIC)

# Preprocess image for OCR
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blur = cv2.medianBlur(gray, 3)
_, thresh = cv2.threshold(blur, 150, 255, cv2.THRESH_BINARY)

# Optional: sharpen image slightly
kernel = np.array([[0, -1, 0],
                   [-1, 5, -1],
                   [0, -1, 0]])
sharpened = cv2.filter2D(thresh, -1, kernel)

# Run OCR with bounding box data
data = pytesseract.image_to_data(sharpened, output_type=pytesseract.Output.DICT)

# Draw bounding boxes for visualization
draw = ImageDraw.Draw(screenshot)
detected_words = []

for i, text in enumerate(data['text']):
    clean_text = text.strip()
    conf = int(data['conf'][i])  # fixed: conf is already int
    if clean_text:
        # Scale bounding boxes to original screenshot coordinates
        x, y, w, h = (data['left'][i] / scale_factor, data['top'][i] / scale_factor,
                      data['width'][i] / scale_factor, data['height'][i] / scale_factor)
        draw.rectangle([x, y, x+w, y+h], outline="red", width=2)
        draw.text((x, y-12), clean_text, fill="yellow")
        detected_words.append(clean_text)
        print(f"Detected: '{clean_text}' with confidence {conf}")

# Combine all detected words into one string
if detected_words:
    main_text = " ".join(detected_words)
    
    # Fuzzy matching against approved names
    match_name, match_score, _ = process.extractOne(main_text, approved_names, scorer=fuzz.ratio)
    if match_score >= 80:
        print(f"'{main_text}' is APPROVED ✅ (matched with '{match_name}', score {match_score})")
    else:
        print(f"'{main_text}' is NOT approved ❌ (closest match '{match_name}', score {match_score})")
else:
    print("No text detected in the region!")

# Show result
screenshot.show()   
screenshot.save("ocr_debug.png")
