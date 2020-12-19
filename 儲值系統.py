import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint
from datetime import datetime


scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets', "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name("C:\\NTU\python\\PDOGS\\期末專案\\NTU COIN-f19789ce087d.json", scope)

client = gspread.authorize(creds)

sheet_coin_money = client.open ("NTU Coin").get_worksheet(4)  # Open the spreadhseet
sheet_userInfo = client.open ("NTU Coin").get_worksheet(0)

def money2coin():

    money = 200  # 改成輸入的數字
    userInfo =['7', 'admin', '1', 'admin2', '411', '4444444']  # 改成使用者的資訊

    userInfo[4] = int(userInfo[4])
    userInfo[4] = str(userInfo[4] + money)

    sheet_userInfo.update_cell(userInfo[0], 5, userInfo[4])  #　更改userInfo 的 Balance

    now = datetime.now()
    dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
    index = int(len(sheet_coin_money.col_values(1)))
    record = [index, 'norm+', userInfo[1], userInfo[1], money, dt_string]
    sheet_coin_money.append_row(record)

def coin2money():    

    money = -100  # 要改成負的
    userInfo =['7', 'admin', '1', 'admin2', '411', '4444444']

    userInfo[4] = int(userInfo[4])
    userInfo[4] = str(userInfo[4] + money)

    sheet_userInfo.update_cell(userInfo[0], 5, userInfo[4])  #　更改userInfo 的 Balance

    now = datetime.now()
    dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
    index = int(len(sheet_coin_money.col_values(1)))
    record = [index, 'norm-', userInfo[1], userInfo[1], money, dt_string]
    sheet_coin_money.append_row(record)

