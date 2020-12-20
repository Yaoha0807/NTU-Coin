import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint
import tkinter as tk
import tkinter.font
import tkinter.messagebox
import tkinter.scrolledtext
from tkinter import ttk
import datetime
import random


# 交換系統介面
class Exchange_system(tk.Frame):
    def __init__(self):
        tk.Frame.__init__(self)
        self.grid()
        self.create_widgets()

    # 設定介面
    def create_widgets(self):
        self.butn_normal_exchange = tk.Button(self, text='一般交換', command=lambda: normal_exchange_page(self))   # 進入一般交換系統
        self.butn_normal_exchange.grid(row=0, column=0, sticky=tk.SW + tk.NE)

        self.butn_special_exchange = tk.Button(self, text='特殊交換', command=lambda: special_exchange_page(self))  # 進入特殊交換系統
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
            self.lab_title.grid(row=0, column=0, sticky=tk.NE + tk.SW)

            self.lab_account = tk.Label(self, text='交換帳號')    # 交換帳號
            self.account_entry = tk.Entry(self)    # 讓用戶輸入交換的帳號
            self.lab_account.grid(row=1, column=0, sticky=tk.E)
            self.account_entry.grid(row=1, column=1, sticky=tk.NE + tk.SW)

            self.lab_account_error = tk.Label(self, text='')      # 交換帳號錯誤訊息
            self.lab_account_error.grid(row=2, column=1, sticky=tk.NE + tk.SW)

            self.lab_amount = tk.Label(self, text='交換數量')     # 交換數量
            self.amount_entry = tk.Entry(self)                    # 讓用戶輸入交換硬幣數量
            self.lab_amount.grid(row=3, column=0, sticky=tk.E)
            self.amount_entry.grid(row=3, column=1, sticky=tk.NE + tk.SW)

            self.lab_amount_error = tk.Label(self, text='')       # 交換數量錯誤訊息
            self.lab_amount_error.grid(row=4, column=1, sticky=tk.NE + tk.SW)

            self.lab_password = tk.Label(self, text='交易密碼')   # 交易密碼
            self.password_entry = tk.Entry(self, show='*')        # 讓用戶輸入交易密碼
            self.lab_password.grid(row=5, column=0, sticky=tk.E)
            self.password_entry.grid(row=5, column=1, sticky=tk.NE + tk.SW)

            self.lab_password_error = tk.Label(self, text='')     # 交易密碼錯誤訊息
            self.lab_password_error.grid(row=6, column=1, sticky=tk.NE + tk.SW)

            self.lab_description = tk.Label(self, text='備註')    # 備註
            self.description_entry = tk.Entry(self)    # 讓用戶輸入備註
            self.lab_description.grid(row=7, column=0, sticky=tk.NE + tk.SW)
            self.description_entry.grid(row=7, column=1, sticky=tk.SW + tk.NE)

            self.butn_commit = tk.Button(self, text='確認', command=self.click_butn_commit)     # 確認送出按紐
            self.butn_commit.grid(row=8, column=0, sticky=tk.NE + tk.SW)

            self.butn_return = tk.Button(self, text='返回交換主頁', command=lambda: exchange_homepage(self))  # 返回交換主頁按紐
            self.butn_return.grid(row=8, column=1, sticky=tk.SW + tk.NE)

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
                self.account_accept = True
            else:
                self.lab_account_error.configure(text='帳號不存在')
                self.account_accept = False

            exchange_amount = self.amount_entry.get()      # 交換數量
            # 確保交換數量為數字
            try:
                int(exchange_amount)
            except Exception as error:
                self.lab_amount_error.configure(text='請輸入數字')
                self.amount_accepted = False
            else:
                self.lab_amount_error.configure(text='')
                exchange_amount = int(exchange_amount)
                self.amount_accepted = True

                # 確保剩餘硬幣足夠
                if user_balance < exchange_amount:
                    self.lab_amount_error.configure(text='剩餘硬幣不足')
                    self.amount_accepted = False
                else:
                    self.lab_amount_error.configure(text='')
                    self.amount_accepted = True

                # 確保交換數量為正
                if exchange_amount > 0:
                    self.lab_amount_error.configure(text='')
                    self.amount_accepted = True
                else:
                    self.lab_amount_error.configure(text='交換數量須為正')
                    self.amount_accepted = False

            exchange_password = self.password_entry.get()    # 交易密碼
            # 確保密碼正確
            if exchange_password == str(user_info[5]):
                self.lab_password_error.configure(text='')
                self.password_accepted = True
            else:
                self.lab_password_error.configure(text='交易密碼錯誤')
                self.password_accepted = False

            description = self.description_entry.get()

            # 輸入內容檢查通過
            if self.account_accept and self.amount_accepted and self.password_accepted:
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
                    self.normal_exchange_info(exchange_account, exchange_amount, exchange_balance, user_index, description)

                # 不執行交換程序，刷新系統介面
                else:
                    normal_exchange_page(self)

        @staticmethod
        # 顯示明細
        def normal_exchange_info(exchange_account, exchange_amount, exchange_balance, user_index, description):
            nor_ex_info = Exchange_system.Normal_exchange.Information(exchange_account, exchange_amount, exchange_balance, user_index, description)
            nor_ex_info.master.title("Exchange Information")
            nor_ex_info.mainloop()

        # 一般交換明細
        class Information(tk.Frame):
            def __init__(self, exchange_account, exchange_amount, exchange_balance, user_index, description):
                tk.Frame.__init__(self)
                self.exchange_account = exchange_account    # 交換帳號
                self.exchange_amount = exchange_amount      # 交換數量
                self.exchange_balance = exchange_balance    # 交換帳號餘額
                self.user_info = sheet.row_values(user_index)   # 使用者帳戶資訊
                self.user_balance = int(self.user_info[4])      # 帳戶餘額
                self.user_balance = self.user_balance   # 使用者帳戶餘額
                self.user_account = self.user_info[1]   # 使用者帳號
                self.exchange_time = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')  # 交換時間
                self.description = description          # 備註
                self.upload_record()
                self.grid()
                self.create_widgets()

            # 設定介面
            def create_widgets(self):
                self.lab_title = tk.Label(self, text='交換明細')  # 系統名稱
                self.lab_title.grid(row=0, column=0, sticky=tk.NE + tk.SW)

                content = '交換帳號: ' + self.exchange_account
                self.lab_account = tk.Label(self, text=content)   # 交換帳號
                self.lab_account.grid(row=1, column=0, sticky=tk.W)

                content = '交換數量: ' + str(self.exchange_amount)
                self.lab_amount = tk.Label(self, text=content)    # 交換數量
                self.lab_amount.grid(row=2, column=0, sticky=tk.W)

                content = '帳戶餘額: ' + str(self.user_balance)
                self.lab_balance = tk.Label(self, text=content)   # 帳戶餘額
                self.lab_balance.grid(row=3, column=0, sticky=tk.W)

                content = '備註: ' + str(self.description)
                self.lab_description = tk.Label(self, text=content)  # 備註
                self.lab_description.grid(row=4, column=0, sticky=tk.W)

                content = '交換時間: ' + self.exchange_time
                self.lab_time = tk.Label(self, text=content)       # 交換時間
                self.lab_time.grid(row=5, column=0, sticky=tk.W)

                self.butn_return = tk.Button(self, text='返回交換主頁', command=lambda: exchange_homepage(self))    # 返回交換主頁按紐
                self.butn_return.grid(row=6, column=0, sticky=tk.SW + tk.NE)

            # 上傳紀錄
            def upload_record(self):
                exchange_record_sheet = NTU_Coin.get_worksheet(2)    # 交換記錄表單
                num_rows = len(exchange_record_sheet.col_values(1))
                row1 = [str(num_rows + 1), 'norm-', self.user_account, self.exchange_account, -self.exchange_amount, self.user_balance, self.exchange_time, self.description]
                row2 = [num_rows + 2, 'norm+', self.exchange_account, self.user_account, self.exchange_amount, self.exchange_balance, self.exchange_time, self.description]
                insert_rows = [row1, row2]
                exchange_record_sheet.append_rows(insert_rows)    # 新增紀錄

    # 特殊交換系統
    class Special_exchange(tk.Frame):
        def __init__(self):
            tk.Frame.__init__(self)
            self.special_exchange_room = NTU_Coin.get_worksheet(3)    # 特殊交換的房間表單
            user_account_all = sheet.col_values(2)              # 大家的帳號(Email)
            user_index = user_account_all.index(account) + 1    # 索引值
            self.user_info = sheet.row_values(user_index)       # 使用者帳戶資訊
            self.user_account = self.user_info[1]               # 使用者帳號
            self.user_name = self.user_info[3]                  # 使用者帳戶名稱
            self.user_balance = self.user_info[4]               # 使用者帳戶餘額
            self.grid()
            self.create_widgets()

        # 設定介面
        def create_widgets(self):
            self.butn_return = tk.Button(self, text='返回交換主頁', command=lambda: exchange_homepage(self))    # 返回交換主頁按紐
            self.butn_return.grid(row=0, column=0, sticky=tk.W)

            self.butn_refresh = tk.Button(self, text='重新整理', command=self.refresh_room_sheet)      # 重新載入房間表單的按紐
            self.butn_refresh.grid(row=1, column=0, sticky=tk.W)

            self.butn_create_room = tk.Button(self, text='創建房間',
                                              command=lambda: self.create_room_page(self.user_account, self.user_name, self.user_balance))    # 創建新房間的按紐
            self.butn_create_room.grid(row=2, column=0, sticky=tk.W)

            caption_columns = self.special_exchange_room.row_values(1)[1:7]    # 定義每一列
            self.room_sheet = ttk.Treeview(self, show='headings', columns=caption_columns)    # 房間表單
            # 製作表頭
            for i in caption_columns:
                self.room_sheet.heading(i, text=i)
            # 顯示房間資訊
            for i in range(1, len(self.special_exchange_room.col_values(1))):
                room_info = self.special_exchange_room.row_values(i + 1)    # 房間資訊
                mode = room_info[1]       # 房間模式
                room_number = room_info[2]    # 房間號碼
                room_name = room_info[3]      # 房間名稱
                need_password_or_not = room_info[4]    # 是否需要密碼?
                people = room_info[5]         # 房間人數
                people_limit = room_info[6]   # 房間人數上限
                tmp = [mode, room_number, room_name, need_password_or_not, people, people_limit]
                self.room_sheet.insert('', 'end', values=tmp)
                self.room_sheet.grid(row=3, column=0, sticky=tk.SW + tk.NE)

            self.scroll_bar = tk.Scrollbar(self)    # 滑動卷軸
            self.scroll_bar.grid(row=3, column=2, sticky=tk.SW + tk.NE)
            self.scroll_bar.config(command=self.room_sheet.yview)      # 連動卷軸跟房間資訊表單
            self.scroll_bar.set(self.scroll_bar.get()[0], self.scroll_bar.get()[1])

            self.room_sheet.bind('<Double-1>', self.treeview_click)    # 連動右鍵雙擊跟進入房間

        # 重新載入房間表單
        def refresh_room_sheet(self):
            self.destroy()
            self.__init__()

        # 雙擊進入房間
        def treeview_click(self, event):
            for item in self.room_sheet.selection():
                room_info = self.room_sheet.item(item, "values")    # 房間資訊
                room_mode = room_info[0]      # 房間模式
                room_number = room_info[1]    # 房間號碼
                room_name = room_info[2]      # 房間名稱
                people_limit = int(room_info[5])     # 房間人數上限

            self.sheet_of_room = NTU_Coin.worksheet('Room %s' % (room_number))    # 該房間的表單
            self.special_exchange_room = NTU_Coin.get_worksheet(3)                # 特殊交換的房間表單
            room_number_all = self.special_exchange_room.col_values(3)            # 所有房間的號碼
            room_index = room_number_all.index(room_number) + 1                   # 房間索引值
            room_password = self.special_exchange_room.cell(room_index, 8).value  # 房間密碼
            people = int(self.special_exchange_room.cell(room_index, 6).value)    # 房間人數

            # 房間還沒滿
            if people_limit > people:
                # 詢問使用者是否進入房間
                enter_room = tk.messagebox.askyesno(title='提醒', message='確定進入%s?' % (room_name))
                # 進入房間
                if enter_room:
                    # 沒有密碼
                    if room_password == '':
                        self.sheet_of_room.append_row([self.user_account, self.user_name, 0, self.user_balance])    # 將使用者資料加入房間的表單
                        self.special_exchange_room.update_cell(room_index, 6, str(people + 1))   # 更新房間人數
                        self.destroy()
                        self.room_page(room_mode, room_name, room_number, people_limit, self.user_account)    # 進入房間頁面
                    # 有密碼，跳到房間密碼輸入頁面
                    else:
                        self.destroy()
                        self.room_password_page = self.Room_password_page(room_password, room_index, people, self.user_account, self.user_balance,
                                                                          self.user_name, room_mode, room_name, room_number, people_limit)
                        self.master.title("Room Password")
                        self.room_password_page.mainloop()
                # 不進入房間，刷新房間表單
                else:
                    self.refresh_room_sheet()
            # 房間滿了
            else:
                tk.messagebox.showerror(title='無法加入房間', message='房間人數已達上限')

        # 房間密碼輸入頁面
        class Room_password_page(tk.Frame):
            def __init__(self, room_password, room_index, people, user_account, user_balance, user_name, room_mode, room_name, room_number, people_limit):
                tk.Frame.__init__(self)
                self.sheet_of_room = NTU_Coin.worksheet('Room %s' % (room_number))    # 該房間的表單
                self.special_exchange_room = NTU_Coin.get_worksheet(3)                # 特殊交換的房間表單
                self.room_password = room_password    # 房間密碼
                self.room_index = room_index          # 房間索引值
                self.people = people                  # 房間人數
                self.user_account = user_account      # 使用者帳號
                self.user_balance = user_balance      # 使用者餘額
                self.user_name = user_name            # 使用者帳戶名稱
                self.room_mode = room_mode            # 房間模式
                self.room_name = room_name            # 房間名稱
                self.room_number = room_number        # 房間號碼
                self.people_limit = people_limit      # 房間人數上限
                self.grid()
                self.create_widgets()

            # 設定介面
            def create_widgets(self):
                self.lab_password = tk.Label(self, text='房間密碼')        # 房間密碼
                self.password_entry = tk.Entry(self)    # 讓使用者輸入房間密碼
                self.lab_password_entry_error = tk.Label(self, text='')    # 房間密碼錯誤訊息
                self.butn_commit = tk.Button(self, text='確認', command=self.password_comfirm)    # 確認按鈕
                self.butn_cancel = tk.Button(self, text='返回', command=lambda: special_exchange_page(self))    # 返回按鈕
                self.lab_password.grid(row=0, column=0, sticky=tk.E + tk.W)
                self.password_entry.grid(row=0, column=1, sticky=tk.E + tk.W)
                self.lab_password_entry_error.grid(row=1, column=1, sticky=tk.E + tk.W)
                self.butn_commit.grid(row=2, column=0, sticky=tk.E + tk.W)
                self.butn_cancel.grid(row=2, column=1, sticky=tk.E + tk.W)

            # 檢查密碼
            def password_comfirm(self):
                # 密碼正確
                if self.password_entry.get() == self.room_password:
                    self.destroy()
                    self.sheet_of_room.append_row([self.user_account, self.user_name, 0, self.user_balance])    # 將使用者資料加入房間的表單
                    self.special_exchange_room.update_cell(self.room_index, 6, str(self.people + 1))    # 更新房間人數
                    Exchange_system.Special_exchange.room_page(self.room_mode, self.room_name, self.room_number,
                                                               self.people_limit, self.user_account)    # 進入房間頁面
                # 密碼錯誤
                else:
                    self.lab_password_entry_error.configure(text='密碼錯誤')    # 顯示房間密碼錯誤訊息

        # 進入創建房間的頁面
        def create_room_page(self, user_account, user_name, user_balance):
            self.destroy()
            self.create_page = self.Create_room(user_account, user_name, user_balance)
            self.master.title("Create a Room")
            self.create_page.mainloop()

        # 創建房間的頁面
        class Create_room(tk.Frame):
            def __init__(self, user_account, user_name, user_balance):
                tk.Frame.__init__(self)
                self.special_exchange_room = NTU_Coin.get_worksheet(3)    # 特殊交換的房間表單
                self.user_account = user_account     # 使用者帳號
                self.user_name = user_name    # 使用者帳戶名稱
                self.user_balance = user_balance     # 使用者餘額
                self.grid()
                self.create_widgets()

            # 設定介面
            def create_widgets(self):
                self.lab_room_number = tk.Label(self, text='房間號碼')    # 房間號碼
                number = random.randint(1, 10000)        # 亂數產生號碼
                self.number = "{:0>5d}".format(number)   # 不足五位數則前方補零
                # 避免重複房間號碼
                while self.number in self.special_exchange_room.col_values(3):
                    number = random.randint(1, 10000)
                    self.number = "{:0>5d}".format(number)
                self.lab_number = tk.Label(self, text=self.number)        # 以亂數為房間號碼
                self.lab_room_number.grid(row=0, column=0, sticky=tk.E + tk.W)
                self.lab_number.grid(row=1, column=0, sticky=tk.E + tk.W)

                self.lab_room_name = tk.Label(self, text='房間名稱')      # 房間名稱
                self.room_name_entry = tk.Entry(self)    # 讓使用者輸入房間名稱
                self.lab_room_name.grid(row=2, column=0, sticky=tk.E + tk.W)
                self.room_name_entry.grid(row=3, column=0, sticky=tk.E + tk.W)

                self.lab_room_name_error = tk.Label(self, text='')        # 房間名稱錯誤訊息
                self.lab_room_name_error.grid(row=4, column=0, sticky=tk.E + tk.W)

                self.lab_room_mode = tk.Label(self, text='房間模式')           # 房間模式
                self.radioValue = tk.IntVar()
                self.room_mode1 = tk.Radiobutton(self, text='麻將', variable=self.radioValue, value=1, command=self.choose_mode)    # 房間模式-麻將
                self.room_mode2 = tk.Radiobutton(self, text='分錢', variable=self.radioValue, value=2, command=self.choose_mode)    # 房間模式-分錢
                self.room_mode = ''    # 預設為無
                self.lab_room_mode.grid(row=5, column=0, sticky=tk.E + tk.W)
                self.room_mode1.grid(row=6, column=0, sticky=tk.E + tk.W)
                self.room_mode2.grid(row=7, column=0, sticky=tk.E + tk.W)

                self.lab_people_limit = tk.Label(self, text='人數上限')    # 房間人數上限
                self.people_limit_entry = tk.Entry(self)    # 讓使用者輸入人數上限
                self.lab_people_limit.grid(row=0, column=1, sticky=tk.E + tk.W)
                self.people_limit_entry.grid(row=1, column=1, sticky=tk.E + tk.W)

                self.lab_people_limit_error = tk.Label(self, text='')      # 房間人數上限錯誤訊息
                self.lab_people_limit_error.grid(row=2, column=1, sticky=tk.E + tk.W)

                self.checkVar = tk.IntVar()
                self.check_box_password = tk.Checkbutton(self, text='設定密碼', variable=self.checkVar, command=self.set_password)    # 讓使用者選擇是否要設密碼
                self.lab_password = tk.Label(self, text='密碼')            # 密碼
                self.password_entry = tk.Entry(self, state='disable')      # 輸入密碼的欄位，預設為不開啟
                self.password_or_not = '否'    # 預設為沒有密碼
                self.check_box_password.grid(row=3, column=1, sticky=tk.E + tk.W)
                self.lab_password.grid(row=4, column=1, sticky=tk.E + tk.W)
                self.password_entry.grid(row=5, column=1, sticky=tk.E + tk.W)

                self.lab_password_entry_error = tk.Label(self, text='')    # 密碼輸入錯誤訊息
                self.lab_password_entry_error.grid(row=6, column=1, sticky=tk.E + tk.W)

                self.butn_create = tk.Button(self, text='創建', command=self.create_room)    # 創建按紐
                self.butn_cancel = tk.Button(self, text='取消', command=lambda: special_exchange_page(self))    # 取消按紐
                self.butn_create.grid(row=7, column=1, sticky=tk.E)
                self.butn_cancel.grid(row=8, column=1, sticky=tk.E)

            # 選擇房間模式
            def choose_mode(self):
                # 使願者選擇麻將模式
                if self.radioValue.get() == 1:
                    self.room_mode = '麻將'    # 房間模式
                    self.people_limit_entry = tk.Label(self, text=4)    # 強制設定人數上限
                    self.people_limit_entry.grid(row=1, column=1, sticky=tk.E + tk.W)
                # 使願者選擇分錢模式:
                else:
                    self.room_mode = '分錢'    # 房間模式
                    self.people_limit_entry = tk.Entry(self)    # 讓使用者輸入人數上限
                    self.people_limit_entry.grid(row=1, column=1, sticky=tk.E + tk.W)

            # 是否設定密碼
            def set_password(self):
                # 是
                if self.checkVar.get() == 1:
                    self.password_or_not = '是'    # 是否需要密碼?
                    self.password_entry = tk.Entry(self)    # 開啟設定密碼的欄位
                    self.password_entry.grid(row=5, column=1, sticky=tk.E + tk.W)
                # 否
                else:
                    self.password_or_not = '否'    # 是否需要密碼?
                    self.lab_password_entry_error.configure(text='')
                    self.password_entry = tk.Entry(self, state='disable')    # 關閉設定密碼的欄位
                    self.password_entry.grid(row=5, column=1, sticky=tk.E + tk.W)

            # 創建房間
            def create_room(self):
                self.room_number = self.number  # 房間號碼
                self.room_name = self.room_name_entry.get()
                self.people = 1   # 房間人數
                # 房間人數上限
                if self.room_mode == '麻將':
                    self.people_limit = 4
                else:
                    self.people_limit = self.people_limit_entry.get()
                # 房間密碼
                if self.password_or_not == '是':
                    self.password = self.password_entry.get()
                else:
                    self.password = ''

                # 檢查輸入內容

                # 確保房間名稱不重複
                if self.room_name in self.special_exchange_room.col_values(4):
                    self.lab_room_name_error.configure(text='名稱重複，請嘗試其他名稱')
                    self.room_name_accept = False
                else:
                    self.lab_room_name_error.configure(text='')
                    self.room_name_accept = True

                # 確保人數上限輸入值為數字
                try:
                    int(self.people_limit)
                except Exception as error:
                    self.lab_people_limit_error.configure(text='請輸入數字')
                    self.people_limit_accepted = False
                else:
                    self.lab_people_limit_error.configure(text='')
                    self.people_limit = int(self.people_limit)
                    self.people_limit_accepted = True

                space = ' '
                # 有要設密碼
                if self.password_or_not == '是':
                    # 確保密碼欄內有輸入
                    if self.password == '':
                        self.lab_password_entry_error.configure(text='請輸入密碼')
                        self.password_accepted = False
                    else:
                        self.lab_password_entry_error.configure(text='')
                        self.password_accepted = True

                        # 確保密碼輸入不含空白
                        if space in self.password:
                            self.lab_password_entry_error.configure(text='密碼內不得含有空白')
                            self.password_accepted = False
                        else:
                            self.lab_password_entry_error.configure(text='')
                            self.password_accepted = True
                # 沒有要設密碼
                else:
                    self.lab_password_entry_error.configure(text='')
                    self.password_accepted = True

                # 輸入符合限制，繼續程序
                if self.room_name_accept and self.people_limit_accepted and self.password_accepted:
                    self.sheet_of_room = NTU_Coin.add_worksheet(title='Room %s' % (self.room_number),
                                                                rows=str(self.people_limit + 3), cols='5')    # 創建該房間的表單
                    self.upload_room()    # 上傳房間資料
                    self.destroy()
                    Exchange_system.Special_exchange.room_page(self.room_mode, self.room_name, self.room_number,
                                                               self.people_limit, self.user_account)    # 進入房間

            # 上傳房間資料
            def upload_room(self):
                # 新增紀錄到特殊交換的房間表單
                num_rows = len(self.special_exchange_room.col_values(1))
                insert_row = [str(num_rows + 1), self.room_mode, self.room_number, self.room_name,
                              self.password_or_not, str(self.people), str(self.people_limit), str(self.password)]
                self.special_exchange_room.append_row(insert_row)
                # 新增紀錄到該房間的表單
                info_headings = ['模式', '號碼', '名稱', '人數上限']
                info = [self.room_mode, self.room_number, self.room_name,
                        str(self.people_limit)]
                user_headings = ['帳戶', '名稱', '分數', '餘額']
                user = [self.user_account, self.user_name, 0, self.user_balance]
                insert_rows = [info_headings, info, user_headings, user]
                self.sheet_of_room.append_rows(insert_rows)

        @staticmethod
        # 進入房間頁面
        def room_page(room_mode, room_name, room_number, people_limit, user_account):
            room_page = Exchange_system.Special_exchange.Room(room_mode, room_name, room_number, people_limit, user_account)
            room_page.master.title('Room %s' % (room_number))
            room_page.mainloop()

        # 房間頁面
        class Room(tk.Frame):
            def __init__(self, room_mode, room_name, room_number, people_limit, user_account):
                tk.Frame.__init__(self)
                self.special_exchange_room = NTU_Coin.get_worksheet(3)    # 特殊交換的房間表單
                self.sheet_of_room = NTU_Coin.worksheet('Room %s' % (room_number))    # 該房間的表單
                self.member = self.sheet_of_room.col_values(2)[3:]        # 房間成員帳戶名稱名單
                self.user_account = user_account    # 使用者帳號
                self.room_mode = room_mode          # 房間模式
                self.room_name = room_name          # 房間名稱
                self.room_number = room_number      # 房間號碼
                self.people_limit = people_limit    # 房間人數上限
                self.grid()
                if self.room_mode == '麻將':
                    self.create_widgets_mj()        # 麻將介面
                elif self.room_mode == '分錢':
                    self.create_widgets_share()     # 分錢介面

            # 設定麻將介面
            def create_widgets_mj(self):
                content = '房間模式: ' + self.room_mode
                self.lab_room_mode = tk.Label(self, text=content)      # 房間模式
                self.lab_room_mode.grid(row=0, column=0, sticky=tk.W)

                content = '房間號碼: ' + self.room_number
                self.lab_room_number = tk.Label(self, text=content)    # 房間號碼
                self.lab_room_number.grid(row=0, column=1, sticky=tk.W)

                content = '房間名稱: ' + self.room_name
                self.lab_room_name = tk.Label(self, text=content)      # 房間名稱
                self.lab_room_name.grid(row=0, column=2, sticky=tk.W)

                self.butn_refresh = tk.Button(self, text='重整房間', command=self.refresh_room)    # 重整房間按鈕
                self.butn_refresh.grid(row=0, column=3, sticky=tk.NW + tk.SE)

                self.butn_leave = tk.Button(self, text='離開房間', command=self.leave_room)        # 離開房間按鈕
                self.butn_leave.grid(row=0, column=4, sticky=tk.NW + tk.SE)

            # 設定分錢介面
            def create_widgets_share(self):
                print('分錢')

            # 重整房間頁面
            def refresh_room(self):
                self.destroy()
                Exchange_system.Special_exchange.room_page(self.room_mode, self.room_name, self.room_number,
                                                           self.people_limit, self.user_account)

            # 離開房間
            def leave_room(self):
                self.special_exchange_room = NTU_Coin.get_worksheet(3)    # 特殊交換的房間表單
                self.sheet_of_room = NTU_Coin.worksheet('Room %s' % (self.room_number))       # 該房間的表單
                self.account = self.sheet_of_room.col_values(1)[3:]       # 房間成員帳號名單
                self.room = self.special_exchange_room.find(self.room_number)    # 該房間
                self.user = self.sheet_of_room.find(self.user_account)           # 該使用者
                self.people = int(self.special_exchange_room.cell(self.room.row, 6).value)    # 房間人數

                # 房間只剩下自己
                if len(self.account) == 1:
                    NTU_Coin.del_worksheet(self.sheet_of_room)    # 刪除該房間的表單
                    self.special_exchange_room.delete_rows(self.room.row)    # 刪除該房間的資訊
                # 房間還有其他使用者
                else:
                    self.sheet_of_room.delete_rows(self.user.row)    # 刪除該使用者的資訊
                    self.special_exchange_room.update_cell(self.room.row, 6, str(self.people - 1))    # 更新房間人數

                special_exchange_page(self)    # 回到特殊交換系統

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


# 進入特殊交換系統
def special_exchange_page(window):
    window.destroy()    # 將原本的畫面刪除
    spec_ex = Exchange_system.Special_exchange()
    spec_ex.master.title("Special Exchange System")
    spec_ex.mainloop()


scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("C:\\Users\\tiffany\\Desktop\\姚冠宇\\商管程式設計\\期末project\\NTU Coin-adba92770851.json", scope)
client = gspread.authorize(creds)
NTU_Coin = client.open('NTU Coin')
sheet = NTU_Coin.get_worksheet(0)  # Open the spreadhseet


account = 'b08701153@ntu.edu.tw'    # 使用者帳號(從登入資訊抓來)
ex_system = Exchange_system()
exchange_homepage(ex_system)
