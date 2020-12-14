from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint
import tkinter as tk
import tkinter.font
import tkinter.messagebox
import datetime


# 交換系統介面
class Exchange_system(tk.Frame):
    def __init__(self):
        tk.Frame.__init__(self)
        self.grid()
        self.create_widgets()

    # 設定介面
    def create_widgets(self):
        self.butn_normal_exchange = tk.Button(self, text='一般交換', command=lambda: normal_exchange_page(self))  # 進入一般交換系統
        self.butn_normal_exchange.grid(row=0, column=0, sticky=tk.SW + tk.NE)

        self.butn_special_exchange = tk.Button(self, text='特殊交換')  # 進入特殊交換系統
        self.butn_special_exchange.grid(row=0, column=1, sticky=tk.SW + tk.NE)

    # 一般交換系統介面
    class Normal_exchange(tk.Frame):
        def __init__(self):
            tk.Frame.__init__(self)
            self.grid()
            self.create_widgets()

        # 設定介面
        def create_widgets(self):
            self.lab_title = tk.Label(self, text='一般交換系統')  # 系統名稱
            self.lab_title.grid(row=0, column=0, sticky=tk.NE +tk.SW)

            self.lab_account = tk.Label(self, text='交換帳號')    # 交換帳號
            self.account_entry = tk.Entry(self)    # 讓用戶輸入交換的帳號
            self.lab_account.grid(row=1, column=0, sticky=tk.E)
            self.account_entry.grid(row=1, column=1, sticky=tk.NE +tk.SW)

            self.lab_account_error = tk.Label(self, text='')      # 交換帳號錯誤訊息
            self.lab_account_error.grid(row=2, column=1, sticky=tk.NE +tk.SW)

            self.lab_amount = tk.Label(self, text='交換數量')     # 交換數量
            self.amount_entry = tk.Entry(self)                    # 讓用戶輸入交換硬幣數量
            self.lab_amount.grid(row=3, column=0, sticky=tk.E)
            self.amount_entry.grid(row=3, column=1, sticky=tk.NE +tk.SW)

            self.lab_amount_error = tk.Label(self, text='')       # 交換數量錯誤訊息
            self.lab_amount_error.grid(row=4, column=1, sticky=tk.NE +tk.SW)

            self.lab_password = tk.Label(self, text='交易密碼')   # 交易密碼
            self.password_entry = tk.Entry(self, show='*')        # 讓用戶輸入交易密碼
            self.lab_password.grid(row=5, column=0, sticky=tk.E)
            self.password_entry.grid(row=5, column=1, sticky=tk.NE +tk.SW)

            self.lab_password_error = tk.Label(self, text='')     # 交易密碼錯誤訊息
            self.lab_password_error.grid(row=6, column=1, sticky=tk.NE +tk.SW)

            self.butn_commit = tk.Button(self, text='確認', command=self.click_butn_commit)     # 確認送出按紐
            self.butn_commit.grid(row=7, column=0, sticky=tk.NE +tk.SW)

            self.butn_return = tk.Button(self, text='返回交換主頁', command=lambda: exchange_homepage(self))  # 返回交換主頁按紐
            self.butn_return.grid(row=7, column=1, sticky=tk.SW + tk.NE)


        # 確認送出
        def click_butn_commit(self):
            # 抓取使用者帳戶資訊
            user_account_all = sheet.col_values(2)              # 大家的帳號(Email)
            user_index = user_account_all.index(account) + 1    # 索引值
            user_info = sheet.row_values(user_index)            # 使用者帳戶資訊
            user_balance = int(user_info[4])    # 帳戶餘額

            # 檢查輸入內容

            exchange_account = self.account_entry.get()    # 交換的帳號
            # 確保交換帳號存在
            if exchange_account in user_account_all:
                self.lab_account_error.configure(text='')
                exchange_index = user_account_all.index(exchange_account) + 1    # 交換帳號的索引值
                account_accept = True
            else:
                self.lab_account_error.configure(text='帳號不存在')
                account_accept = False

            exchange_amount = self.amount_entry.get()      # 交換數量
            # 確保交換數量為數字
            try:
                int(exchange_amount)
            except:
                self.lab_amount_error.configure(text='請輸入數字')
                amount_accepted = False
            else:
                self.lab_amount_error.configure(text='')
                exchange_amount = int(exchange_amount)
                amount_accepted = True
                
                # 確保剩餘硬幣足夠
                if user_balance < exchange_amount:
                    self.lab_amount_error.configure(text='剩餘硬幣不足')
                    amount_accepted = False
                else:
                    self.lab_amount_error.configure(text='')
                    amount_accepted = True

                # 確保交換數量為正
                if exchange_amount > 0:
                    self.lab_amount_error.configure(text='')
                    amount_accepted = True
                else:
                    self.lab_amount_error.configure(text='交換數量須為正')
                    amount_accepted = False

            exchange_password = self.password_entry.get()    # 交易密碼
            # 確保密碼正確
            if exchange_password == str(user_info[5]):
                self.lab_password_error.configure(text='')
                password_accepted = True
            else:
                self.lab_password_error.configure(text='交易密碼錯誤')
                password_accepted = False

            # 輸入內容檢查通過
            if account_accept and amount_accepted and password_accepted:
                # 再次向使用者確認
                run_process = tk.messagebox.askyesno(title='提醒', message='確定執行交換程序?')
                # 執行交換程序
                if run_process:
                    exchange_info = sheet.row_values(exchange_index)    # 交換帳號帳戶資訊
                    exchange_balance = int(exchange_info[4])    # 交換帳號餘額
                    # 更新資訊
                    user_balance -= exchange_amount
                    exchange_balance += exchange_amount
                    sheet.update_cell(user_index, 5, user_balance)
                    sheet.update_cell(exchange_index, 5, exchange_balance)
                    # 顯示明細
                    self.destroy()
                    self.normal_exchange_info(exchange_account, exchange_amount, exchange_balance, user_index)
                    
                # 不執行交換程序，刷新系統介面
                else:
                    normal_exchange_page(self)

        @staticmethod
        # 顯示明細
        def normal_exchange_info(exchange_account, exchange_amount, exchange_balance, user_index):
            nor_ex_info = Exchange_system.Normal_exchange.Information(exchange_account, exchange_amount, exchange_balance, user_index)
            nor_ex_info.master.title("Exchange Information")
            nor_ex_info.mainloop()

        # 一般交換明細
        class Information(tk.Frame):
            def __init__(self, exchange_account, exchange_amount, exchange_balance, user_index):
                tk.Frame.__init__(self)
                self.exchange_account = exchange_account    # 交換帳號
                self.exchange_amount = exchange_amount      # 交換數量
                self.exchange_balance = exchange_balance    # 交換帳號餘額
                self.user_info = sheet.row_values(user_index)   # 使用者帳戶資訊
                self.user_balance = int(self.user_info[4])      # 帳戶餘額
                self.user_balance = self.user_balance   # 使用者帳戶餘額
                self.user_account = self.user_info[1]   # 使用者帳號
                self.user_name = self.user_info[3]      # 使用者帳戶名稱
                self.exchange_time = datetime.datetime.strftime(datetime.datetime.now(),'%Y-%m-%d %H:%M:%S')  # 交換時間
                self.upload_record()
                self.grid()
                self.create_widgets()

            # 設定介面
            def create_widgets(self):
                self.lab_title = tk.Label(self, text='交換明細')  # 系統名稱
                self.lab_title.grid(row=0, column=0, sticky=tk.NE +tk.SW)

                content = '交換帳號: ' + self.exchange_account
                self.lab_account = tk.Label(self, text=content)   # 交換帳號
                self.lab_account.grid(row=1, column=0, sticky=tk.W)

                content = '交換數量: ' + str(self.exchange_amount)
                self.lab_amount = tk.Label(self, text=content)    # 交換數量
                self.lab_amount.grid(row=2, column=0, sticky=tk.W)

                content = '帳戶餘額: ' + str(self.user_balance)
                self.lab_balance = tk.Label(self, text=content)   # 帳戶餘額
                self.lab_balance.grid(row=3, column=0, sticky=tk.W)

                content = '交換時間: ' + self.exchange_time
                self.lab_time = tk.Label(self, text=content)      # 交換數量
                self.lab_time.grid(row=4, column=0, sticky=tk.W)

                self.butn_return = tk.Button(self, text='返回交換主頁', command=lambda: exchange_homepage(self))    # 返回交換主頁按紐
                self.butn_return.grid(row=5, column=0, sticky=tk.SW + tk.NE)

            # 上傳紀錄
            def upload_record(self):
                exchange_record_sheet = client.open("NTU Coin").get_worksheet(3)    # 交換記錄表單
                num_rows = exchange_record_sheet.row_count
                row1 = [num_rows + 1, 'norm-', self.user_account, self.exchange_account, -self.exchange_amount, self.user_balance, self.exchange_time]
                row2 = [num_rows + 2, 'norm+', self.exchange_account, self.user_account, self.exchange_amount, self.exchange_balance, self.exchange_time]
                insert_rows = [row1, row2]
                exchange_record_sheet.append_rows(insert_rows)    # 新增紀錄


# 進入交換主頁
def exchange_homepage(window):
    window.destroy()    # 將原本的畫面刪除
    ex_system = Exchange_system()
    ex_system.master.title("Exchange System")
    ex_system.mainloop()

# 進入一般交換系統
def normal_exchange_page(window):
    window.destroy()    # 將原本的畫面刪除
    nor_ex = Exchange_system.Normal_exchange()
    nor_ex.master.title("Normal Exchange System")
    nor_ex.mainloop()


scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets'
         ,"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("C:\\Users\\tiffany\\Desktop\\姚冠宇\\商管程式設計\\期末project\\NTU Coin-adba92770851.json", scope)
client = gspread.authorize(creds)
sheet = client.open("NTU Coin").get_worksheet(0) # Open the spreadhseet
data = sheet.get_all_records() # Get a list of all records


account = 'b08701153@ntu.edu.tw'    # 使用者帳號(從登入資訊抓來)
ex_system = Exchange_system()
exchange_homepage(ex_system)
