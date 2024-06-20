import os
from pororo import Pororo

def extract_text_from_file(image_path):
    if not os.path.isfile(image_path):
        raise FileNotFoundError(f"Image file not found: {image_path}")

    ocr = Pororo(task="ocr", lang="ko")
    result = ocr(image_path, detail=True)
    return result

def sort_text_by_x_position(ocr_result):
    # 먼저 y 값을 기준으로 정렬
    sorted_result = sorted(ocr_result['bounding_poly'], key=lambda item: item['vertices'][0]['y'])
    
    # y 값의 차이가 50 이하인 경우 x 값을 기준으로 정렬
    grouped_lines = []
    current_line = []
    last_y = None

    for item in sorted_result:
        current_y = item['vertices'][0]['y']
        if last_y is None or abs(current_y - last_y) <= 5:
            current_line.append(item)
        else:
            grouped_lines.append(current_line)
            current_line = [item]
        last_y = current_y

    if current_line:
        grouped_lines.append(current_line)

    # 각 그룹 내에서 x 값을 기준으로 정렬
    for line in grouped_lines:
        line.sort(key=lambda item: item['vertices'][0]['x'])

    # 정렬된 결과를 하나의 리스트로 병합
    sorted_result = [item for line in grouped_lines for item in line]
    
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
    sorted_text = extract_sorted_text(ocr_result)
    print(sorted_text)

