import os
import cv2
from pororo import Pororo

#def reformat_input(image_path):
#    img = cv2.imread(image_path)
#    if img is None:
#        raise ValueError("Failed to load image. Please check the file path and format.")
#    img_cv_grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#    return img, img_cv_grey

def extract_text_from_file(image_path):
    if not os.path.isfile(image_path):
        raise FileNotFoundError(f"Image file not found: {image_path}")
    
#    img, img_cv_grey = reformat_input(image_path)
    ocr = Pororo(task="ocr", lang="ko")
    result = ocr(image_path, detail=True)
    return result

def sort_text_by_x_position(ocr_result):
    try:
        sorted_result = sorted(ocr_result['bounding_poly'], key=lambda item: (item['vertices'][0]['y'], item['vertices'][0]['x']))
    except TypeError as e:
        print(f"Error: {e}")
        raise
    return sorted_result

def extract_sorted_text(ocr_result):
    sorted_result = sort_text_by_x_position(ocr_result)
    sorted_text = ' '.join([item['description'] for item in sorted_result])
    return sorted_text

image_path = "test_lunch.jpg"
ocr_result = extract_text_from_file(image_path)

print(ocr_result)

# OCR 결과가 문자열 형태인 경우 처리
if isinstance(ocr_result, str):
    print("OCR 결과가 문자열 형태로 반환되었습니다.")
else:
    #print(type(ocr_result))
    #for row in ocr_result:
    #    print(row)
    sorted_text = extract_sorted_text(ocr_result)
    print(sorted_text)

