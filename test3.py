import os
import cv2
from pororo import Pororo

def reformat_input(image_path):
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError("Failed to load image. Please check the file path and format.")
    img_cv_grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return img, img_cv_grey

def extract_text_from_file(image_path):
    if not os.path.isfile(image_path):
        raise FileNotFoundError(f"Image file not found: {image_path}")
    
    img, img_cv_grey = reformat_input(image_path)
    ocr = Pororo(task="ocr", lang="ko")
    result = ocr(img, detail=True)
    return result

image_path = "test_lunch.jpg"
text = extract_text_from_file(image_path)
print(text)

