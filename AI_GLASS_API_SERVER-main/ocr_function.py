import cv2
import pytesseract
import pyttsx3
import time
import numpy as np

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def ocr_image_to_text(image_path, lang=None):
  image = cv2.imread(image_path) 

  gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # Ensure grayscale

  # Optional: Enhance for OCR (adjust as needed)
  #  frame_enh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 85, 11)
  laplacian_filter = np.array([[0,-1,0], [-1,5,-1], [0,-1,0]])
  frame_enh = cv2.filter2D(gray, -1, laplacian_filter) 

  # Perform OCR
  if lang == 'ar':
    config = r'--psm 3 --oem 3 -l ara'
    txt = pytesseract.image_to_string(frame_enh, config=config)
  else:
    txt = pytesseract.image_to_string(frame_enh)

  # Text-to-Speech
  if txt:
    return txt
  else:
    return "Nothing To Read"


def test_ocr():
  print(ocr_image_to_text("static/logo.png"))