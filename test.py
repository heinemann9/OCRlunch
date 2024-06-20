import easyocr
import requests
from PIL import Image
from io import BytesIO
from google.oauth2 import service_account
from googleapiclient.discovery import build

def extract_text_from_file(image_path):
    try:
        # 이미지 파일 열기
        img = Image.open(image_path)
        img.verify()  # 이미지 파일 검증

        # EasyOCR을 사용하여 텍스트 추출
        img = Image.open(image_path)  # 검증 후 다시 열기
        reader = easyocr.Reader(['ko', 'en'])  # 한국어와 영어 지원
        result = reader.readtext(img)
        texts = [item[1] for item in result]
        return "\n".join(texts)
    except (Image.UnidentifiedImageError, IOError) as e:
        print(f"이미지 파일 오류: {e}")
        return None


def update_google_sheet(text):
    # Google Sheets API 인증 설정
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    SERVICE_ACCOUNT_FILE = 'credentials.json'  # 서비스 계정 키 파일 경로

    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()

    # Google Sheets ID와 범위 설정
    SPREADSHEET_ID = 'your_spreadsheet_id'  # 자신의 스프레드시트 ID로 변경
    RANGE_NAME = 'Sheet1!A1'  # 업데이트할 셀 범위

    # 업데이트할 데이터 설정
    values = [[text]]
    body = {
        'values': values
    }

    # Google Sheets에 데이터 업데이트
    result = sheet.values().update(
        spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME,
        valueInputOption='RAW', body=body).execute()

    print(f"{result.get('updatedCells')} cells updated.")

# 이미지 URL에서 텍스트 추출 및 Google Sheets 업데이트
img_path = "test_lunch.jpg"
text = extract_text_from_file(img_path)
print(text)
#update_google_sheet(text)
