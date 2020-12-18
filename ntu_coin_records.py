import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/spreadsheets',
'https://www.googleapis.com/auth/drive.file','https://www.googleapis.com/auth/drive']

creds = ServiceAccountCredentials.from_json_keyfile_name('NTU-Coin-27f11025174e.json', scope)
client = gspread.authorize(creds)

# 把第X張worksheet的資料用爬蟲爬下來
def crawler(worksheet_index):
    sheet = client.open('NTU Coin').get_worksheet(worksheet_index)
    data = sheet.get_all_records()
    return data

rawExchange = crawler(2)
rawSaving = crawler(4)
rawMission = crawler(5)

# 將各張worksheet的資料加上屬於該worksheet的類別
def add_category(records, category_name):
  for i in range(len(records)):
    records[i]['category'] = category_name
  return records

ExchangeRecords = add_category(rawExchange, '貨幣交換')
SavingRecords = add_category(rawSaving, '儲值記錄')
MissionRecords = add_category(rawMission, '任務記錄')

# 將各張worksheet的資料合併為一個list
data = []
for i in (ExchangeRecords, SavingRecords, MissionRecords):
  for j in range(len(i)):
    data.append(i[j])


# 更改日期格式
def trans_time(adict):
    origin_time = adict.get('Time')
    new_time = origin_time[:10]
    adict['Time'] = new_time
    return adict

user = input('請輸入欲查詢的user = ')

# 挑出資料庫中，指定user的記錄
all_user_records = []
for i in range(len(data)):
    if data[i].get('Account') == user:
        all_user_records.append(trans_time(data[i]))

# 依照日期排序
all_user_records.sort(key=lambda all_user_records:all_user_records["Time"]) 

# 分為收入與支出
income_records = []  # 收入記錄
payment_records = [] # 支出記錄
for i in range(len(all_user_records)):
    if all_user_records[i].get('Status') == 'norm-':
        payment_records.append(all_user_records[i])
    else:
        income_records.append(all_user_records[i])


# 時間篩選器
import time
import datetime

current_date = time.strftime('%Y-%m-%d')
week_ago = (datetime.datetime.now() + datetime.timedelta(days=-7)).strftime('%Y-%m-%d')
month_ago = (datetime.datetime.now() + datetime.timedelta(days=-30)).strftime('%Y-%m-%d')
year_ago = (datetime.datetime.now() + datetime.timedelta(days=-365)).strftime('%Y-%m-%d')

def select_time(records, param1):
    new_records = []
    if param1 == '全部':
        new_records = records
    elif param1 == '過去一週':
        for i in range(len(records)):
            if records[i].get('Time') >= week_ago:
                new_records.append(records[i])
    elif param1 == '過去一月':
        for i in range(len(records)):
            if records[i].get('Time') >= month_ago:
                new_records.append(records[i])
    else:  # param1 == '過去一年'
        for i in range(len(records)):
            if records[i].get('Time') >= year_ago:
                new_records.append(records[i])

    return new_records

# 類別篩選器
def select_category(records, param2):
    new_records = []
    if param2 == '全部':
        new_records = records
    else:
        for i in range(len(records)):
            if records[i].get('Category') == param2:
                new_records.append(records[i])
    
    return new_records

# 關鍵字篩選器
def select_key(records, param3, param4):
    new_records = []
    for i in range(len(records)):
        if param3 == '用戶名':
            if records[i].get('Exchange Account') == param4:
                new_records.append(records[i])
        elif param3 == '關鍵字':
            if param4 in records[i].get('內容'):
                new_records.append(records[i])
        else:
            pass

    return new_records

# 與GUI連結，讓使用者自訂查詢依據
button1 = input('請輸入時間範圍 = ')
button2 = input('請輸入檢索類別 = ')
button3 = input('請輸入檢索依據 = ')
button4 = input('請輸入檢索關鍵字 = ')

# [篩選後的收入記錄，篩選後的支出記錄]
selected = []
for i in (income_records, payment_records):
    
    time_records = select_time(i, button1)

    category_records = select_category(time_records, button2)

    if button2 == '儲值記錄':
        selected.append(category_records)
    else:
        if button3 == '1':
            selected.append(category_records)
        else:
            key_records = select_key(category_records, button3, button4)
            selected.append(key_records)

# 將篩選結果轉換為清單儲存
def output_records(records):
    output = []

    for i in range(len(records)):
        date = records[i].get('Time')
        account = records[i].get('Exchange Account')
        category = records[i].get('Category')
        description = records[i].get('Description')
        amount = int(records[i].get('Amount'))
        temp = [date, account, category, description, amount]
        output.append(temp)
    
    return output

result_income = output_records(selected[0])  # 檢索結果：收入
result_payment = output_records(selected[1]) # 檢索結果：支出
