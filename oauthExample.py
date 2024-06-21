from oauth2client.service_account import ServiceAccountCredentials
import gspread

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('lunchalarmautomation-d6273e088fa6.json', scope)
gc = gspread.authorize(credentials)

gc1 = gc.open("점심메뉴").worksheet('sheet1')
gc2 = gc1.get_all_values()
print(gc2)