from tkinter import *
import datetime

# 把資料夾叫開
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint
scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',
"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name(r"C:\Users\User\Desktop\GitHub\NTU-Coin\python-google-sheet-d3544b66f48e.json", scope)
client = gspread.authorize(creds)
sheet = client.open("NTU Coin").worksheet("Missions")

transaction_phase = []
#第一項為上傳任務初始檔，第二項為接收者帳號，第三項為任務結束檔

# 新增任務
def establish_mission(submitter_account, mission_name, mission_content, payment):
    sub_time_create = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
    mission_index = int(len(sheet.col_values(1)))+1
    status = "on-going"
    account = submitter_account
    lst = [mission_index, account, mission_name, mission_content, payment, status, sub_time_create]
    sheet.append_row(lst)
    # 將任務此階段原始細節另存入一個list
    global transaction_phase
    transaction_phase.append(lst)
    ## 有ongoing標籤的是要進到任務總覽裡面的

# 接收任務
def accept_mission(accepter_account,mission_index):
    #因為有mission_index所以就有一個任務裡面的所有要件了
    sub_time_accept = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
    row = sheet.find(mission_index).row
    status = "taken"
    sheet.update_cell(row,6,status)
    sheet.update_cell(row,7,sub_time_accept)
    global transaction_phase
    transaction_phase.append(accepter_account)
    ## 一旦標籤不是ongoing的時候，任務總覽裡面就不能有這任務

# 完成任務
def finish_mission(accepter_account,mission_index):
    # 要餵mission index給這個函數，因為一個人可以同時具有多個正在執行的任務。挑選到要提交的任務之後傳出mission index由此接收
    sub_time_finish = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
    row = sheet.find(mission_index).row
    status = "finished"
    sheet.update_cell(row,6,status)
    sheet.update_cell(row,7,sub_time_finish)
    mission_account = accepter_account
    mission_name = sheet.cell(row,3).value
    mission_content = sheet.cell(row,4).value
    payment = sheet.cell(row,5).value
    account = accepter_account
    lst = [mission_index, account, mission_name, mission_content, payment, status, sub_time_finish]
    global transaction_phase
    transaction_phase.append(lst)

def pay(list):
    # 傳入transaction_phase
    # 將交易開始與結束移轉到紀錄系統
    # 將交易金額記錄到使用者即時資料庫
    mission_name = list[0][2]
    provider = list[0][1]
    accepter = list[2][1]
    accounts_payable = list[0][4]
    accounts_receivable = list[0][4]
    pay_time = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')

    user_info = client.open("NTU Coin").worksheet("User_Info")
    # 扣交付任務者錢
    user_info_row = user_info.find(provider).row
    balance = int(user_info.cell(user_info_row,5).value)
    balance -= int(accounts_payable)
    user_info.update_cell(user_info_row,5,balance)
    # 給受雇者錢
    user_info_row_accept = user_info.find(accepter).row
    balance_accepter = int(user_info.cell(user_info_row_accept,5).value)
    balance_accepter += int(accounts_receivable)
    user_info.update_cell(user_info_row_accept,5,balance_accepter)
    

    exchange_records = client.open("NTU Coin").worksheet("Exchange Record")
    # 紀錄登錄
    index = exchange_records.row_count +1
    cred1 = [index, "norm-", provider, accepter,-int(accounts_payable),balance, pay_time]
    cred2 = [index+1, "norm+", accepter, provider, int(accounts_receivable), balance_accepter, pay_time]
    exchange_records.append_row(cred1)
    exchange_records.append_row(cred2)

# establish_mission("b09704063@ntu.edu.tw","i am so tired","it's fucking 1:49","10000000")
# accept_mission("bb@ntu.edu.tw","3")
# finish_mission("bb@ntu.edu.tw", "3")
# pay(transaction_phase)

# 自登錄訊息中取得登錄者的餘額(provider應被替換為餘額)
def enough_coins(provider):
    if provider < 0:
        return False
    else: 
        return True 
# 準備好介面所需資訊給無進化接手
def quest_summary_info():
    display_list = []
    def available_or_not(status):
        if status != "on-going":
            return False
        else:
            return True
    mission_summary = client.open("NTU Coin").worksheet("Mission")
    for i in range(mission_summary.row_count):
        if available_or_not(mission_summary.cell(i,6).value) == True:
            time = mission_summary.cell(i,7).value
            account = mission_summary.cell(i,1).value
            task = mission_summary.cell(i,2).value
            coins = mission_summary.cell(i,5).value
            lst = [time, account, task, coins]
            display_list.append(lst)
        else:
            pass
    return display_list