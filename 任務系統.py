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
user_info = client.open("NTU Coin").worksheet("User_Info")
mission_records = client.open("NTU Coin").worksheet("Mission Record")

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
    sheet.update_cell(row,6,status) #5
    sheet.update_cell(row,7,sub_time_accept) #6
    sheet.update_cell(row,8,accepter_account) #7
    ## 一旦標籤不是ongoing的時候，任務總覽裡面就不能有這任務

# 完成任務
def finish_mission(mission_index):
    # 要餵mission index給這個函數，因為一個人可以同時具有多個正在執行的任務。挑選到要提交的任務之後傳出mission index由此接收
    sub_time_finish = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
    row = sheet.find(mission_index).row
    row_list = sheet.row_values(row)
    status = "finished"
    sheet.update_cell(row,6,status)
    sheet.update_cell(row,7,sub_time_finish)
    def pay(mission_index):
        # 將交易開始與結束移轉到紀錄系統
        # 將交易金額記錄到使用者即時資料庫
        mission_name = row_list[2]
        mission_content = row_list[3]
        provider = row_list[1]
        accepter = row_list[7]
        accounts_payable = row_list[4]
        accounts_receivable = row_list[4]
        pay_time = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')

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

        # 紀錄登錄
        index = len(mission_records.col_values(2))+1
        cred1 = [index, "norm-",provider, accepter,-int(accounts_payable), pay_time, mission_name, mission_content]
        cred2 = [index+1, "norm+",accepter, provider,"+" +str(int(accounts_receivable)), pay_time, mission_name, mission_content]
        mission_records.append_row(cred1)
        mission_records.append_row(cred2)
    pay(mission_index)


# 準備好介面所需資訊給任務介面
def quest_summary_info():
    display_list = []
    mission_summary = client.open("NTU Coin").worksheet("Missions")
    for i in range(mission_summary.row_count):
        row_list = mission_summary.row_values(i)
        if row_list[5] == 'on-going':
            time = row_list[6]
            account = row_list[1]
            task = row_list[2]
            coins = row_list[4]
            lst = [time, account, task, coins]
            display_list.append(lst)
    return display_list
# 從任務大廳按了欲接收的任務之後的動作,回傳任務index,content,payment
def click_accept_mission_from_lobby(mission_index):
    mission_index = str(mission_index)
    ficher = client.open("NTU Coin").worksheet("Missions")
    mission_row = ficher.find(mission_index).row
    row_list = ficher.row_values(mission_row)
    index = row_list[0]
    content = row_list[3]
    payment = row_list[4]
    lst = [index, content, payment]
    return lst
# 進入查看任務介面查看已接收任務
def mission_inquiry(accepter_account):
    display_list = []
    for i in range(len(sheet.col_values(1))):
        i +=1
        row_list = sheet.row_values(i)
        accepter_in_list = row_list[7]
        status = row_list[5]
        if accepter_in_list == accepter_account and status == "taken":
            mission_index = row_list[0]
            mission_name = row_list[2] 
            mission_pay = row_list[4] 
            lst = [mission_index, mission_name, mission_pay]
            display_list.append(lst)
    return display_list

# 從查看任務按了已接收的任務之後，回傳任務index,name,content,payment
def click_accepted_mission_from_mission_inquiry(mission_index):
    ficher = client.open("NTU Coin").worksheet("Missions")
    mission_row = ficher.find(mission_index).row
    row_list = ficher.row_values(mission_row)
    index = row_list[0] #0
    name = row_list[2] #2
    content = row_list[3] #3
    payment = row_list[4] #4
    lst = [index, name, content, payment]
    return lst
# 放棄任務
def abort_mission(mission_index):
    mission_row = sheet.find(mission_index).row
    row_list = sheet.row_values(mission_row)
    if row_list[5] == "taken":
        status = "on-going"
        sheet.update_cell(mission_row, 6, status)
        sheet.update_cell(mission_row, 8, "")

# establish_mission("b09704063@ntu.edu.tw","不能用中文","不要用中文","10")
# accept_mission("bb@ntu.edu.tw","13")
# finish_mission("12")
# abort_mission("13")
