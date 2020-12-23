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
from PIL import Image, ImageTk


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
                row2 = [str(num_rows + 2), 'norm+', self.exchange_account, self.user_account, self.exchange_amount, self.exchange_balance, self.exchange_time, self.description]
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
            self.f_title = tk.font.Font(size=30, family='Microsoft JhengHei', weight='bold')    # 標題字形
            self.f_lab = tk.font.Font(size=12, family='Microsoft JhengHei', weight='bold')      # 一般字形
            self.f_con = tk.font.Font(size=10, family='Microsoft JhengHei')    # 內容字形
            self.grid()
            self.create_widgets()

        @staticmethod
        # 設定背景顏色及文字顏色
        def set_bg_fg(widgets_list):
            for widget in widgets_list:
                widget.configure(bg='#363636', fg='white')

        @staticmethod
        # 設定錯誤訊息的背景顏色及文字顏色
        def set_bg_fg_error(widgets_error_list):
            for widget in widgets_error_list:
                widget.configure(bg='#363636', fg='orange')

        @staticmethod
        # 設定使用者資訊的背景顏色及文字顏色
        def set_bg_fg_user(user_info_list):
            for user in user_info_list:
                user.configure(bg='#363636', fg='dark orange2')

        # 設定介面
        def create_widgets(self):
            self.widgets_list = []    # 部件清單

            self.lab_title = tk.Label(self, text='特殊交換系統 - 房間列表', font=self.f_title)     # 標題
            self.lab_title.grid(row=0, column=0, columnspan=3, sticky=tk.SW + tk.NE)
            self.widgets_list.append(self.lab_title)           # 加入部件清單

            self.butn_return = tk.Button(self, text='返回交換主頁', height=1, width=12, font=self.f_lab,
                                         command=lambda: exchange_homepage(self))    # 返回交換主頁按紐
            self.butn_return.grid(row=0, column=0, sticky=tk.SW + tk.NE)
            self.widgets_list.append(self.butn_return)         # 加入部件清單

            self.butn_refresh = tk.Button(self, text='重新整理', height=1, width=12, font=self.f_lab,
                                          command=self.refresh_room_sheet)           # 重新載入房間表單的按紐
            self.butn_refresh.grid(row=1, column=0, sticky=tk.SW + tk.NE)
            self.widgets_list.append(self.butn_refresh)        # 加入部件清單

            self.butn_create_room = tk.Button(self, text='創建房間', height=1, width=12, font=self.f_lab,
                                              command=lambda: self.create_room_page(self.user_account, self.user_name, self.user_balance))    # 創建新房間的按紐
            self.butn_create_room.grid(row=2, column=0, sticky=tk.SW + tk.NE)
            self.widgets_list.append(self.butn_create_room)    # 加入部件清單

            self.lab_blank = tk.Label(self, text='', font=self.f_lab)
            self.lab_blank.grid(row=3, column=0, rowspan=38, sticky=tk.SW + tk.NE)
            self.widgets_list.append(self.lab_blank)           # 加入部件清單

            ttk.Style().configure('Treeview.Heading', background='#363636', font=self.f_lab)
            caption_columns = self.special_exchange_room.row_values(1)[1:7]    # 定義每一列
            self.room_sheet = ttk.Treeview(self, show='headings', columns=caption_columns, height=30)    # 房間表單
            # 調整列距
            self.room_sheet.column('模式', width=105, anchor='center')
            self.room_sheet.column('號碼', width=150, anchor='center')
            self.room_sheet.column('名稱', width=225, anchor='center')
            self.room_sheet.column('是否需要密碼?', width=140, anchor='center')
            self.room_sheet.column('人數', width=105, anchor='center')
            self.room_sheet.column('人數上限', width=150, anchor='center')
            # 製作表頭
            for i in caption_columns:
                self.room_sheet.heading(i, text=i)
            # 顯示房間資訊
            for i in range(1, len(self.special_exchange_room.col_values(1))):
                room_info = self.special_exchange_room.row_values(i + 1)    # 房間資訊
                mode = room_info[1]       # 房間模式
                room_number = room_info[2]    # 房間號碼
                room_name = room_info[3]      # 房間名稱
                need_password_or_not = room_info[4]      # 是否需要密碼?
                people = room_info[5]         # 房間人數
                people_limit = room_info[6]   # 房間人數上限
                tmp = [mode, room_number, room_name, need_password_or_not, people, people_limit]
                self.room_sheet.insert('', 'end', values=tmp, tags=('font'))
                self.room_sheet.tag_configure('font', font=self.f_con)
                self.room_sheet.grid(row=1, column=1, rowspan=40, sticky=tk.SW + tk.NE)

            self.scroll_bar = tk.Scrollbar(self)    # 滑動卷軸
            self.scroll_bar.grid(row=1, column=2, rowspan=40, sticky=tk.SW + tk.NE)
            self.scroll_bar.config(command=self.room_sheet.yview)      # 連動卷軸跟房間資訊表單
            self.scroll_bar.set(self.scroll_bar.get()[0], self.scroll_bar.get()[1])

            self.room_sheet.bind('<Double-1>', self.treeview_click)    # 連動右鍵雙擊跟進入房間

            self.set_bg_fg(self.widgets_list)    # 更改物件的文字顏色跟背景顏色

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
                self.f_title = tk.font.Font(size=30, family='Microsoft JhengHei', weight='bold')    # 標題字形
                self.f_lab = tk.font.Font(size=12, family='Microsoft JhengHei', weight='bold')      # 一般字形
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
                self.widgets_list = []    # 部件清單
                self.widgets_error_list = []    # 錯誤訊息清單

                self.lab_blank1 = tk.Label(self, text='', width=58, height=10)    # 空白區域
                self.lab_blank1.grid(row=0, column=0, columnspan=4, sticky=tk.SE + tk.NW)
                self.widgets_list.append(self.lab_blank1)    # 加入部件清單

                self.lab_blank2 = tk.Label(self, text='', width=58, height=15)    # 空白區域
                self.lab_blank2.grid(row=1, column=0, rowspan=4, sticky=tk.SE + tk.NW)
                self.widgets_list.append(self.lab_blank2)    # 加入部件清單

                self.lab_password = tk.Label(self, text='房間密碼', font=self.f_title)        # 房間密碼
                self.password_entry = tk.Entry(self, show='*', font=self.f_lab)    # 讓使用者輸入房間密碼
                self.lab_password_entry_error = tk.Label(self, text='', font=self.f_lab)    # 房間密碼錯誤訊息
                self.lab_password.grid(row=1, column=1, columnspan=2, sticky=tk.SE + tk.NW)
                self.password_entry.grid(row=2, column=1, columnspan=2, sticky=tk.SE + tk.NW)
                self.lab_password_entry_error.grid(row=3, columnspan=2, column=1, sticky=tk.SE + tk.NW)
                # 加入部件清單
                self.widgets_list.append(self.lab_password)
                self.widgets_error_list.append(self.lab_password_entry_error)

                self.butn_commit = tk.Button(self, text='確認', font=self.f_lab,
                                             command=self.password_comfirm)    # 確認按鈕
                self.butn_cancel = tk.Button(self, text='返回', font=self.f_lab,
                                             command=lambda: special_exchange_page(self))    # 返回按鈕
                self.butn_commit.grid(row=4, column=1, sticky=tk.SE + tk.NW)
                self.butn_cancel.grid(row=4, column=2, sticky=tk.SE + tk.NW)
                # 加入部件清單
                self.widgets_list.append(self.butn_commit)
                self.widgets_list.append(self.butn_cancel)

                Exchange_system.Special_exchange.set_bg_fg(self.widgets_list)    # 更改物件的文字顏色跟背景顏色
                Exchange_system.Special_exchange.set_bg_fg_error(self.widgets_error_list)    # 更改錯誤訊息的文字顏色跟背景顏色

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
                self.f_title = tk.font.Font(size=20, family='Microsoft JhengHei', weight='bold')    # 標題字形
                self.f_b_title = tk.font.Font(size=35, family='Microsoft JhengHei', weight='bold')  # 大標題字形
                self.f_lab = tk.font.Font(size=12, family='Microsoft JhengHei', weight='bold')      # 一般字形
                self.special_exchange_room = NTU_Coin.get_worksheet(3)    # 特殊交換的房間表單
                self.user_account = user_account     # 使用者帳號
                self.user_name = user_name    # 使用者帳戶名稱
                self.user_balance = user_balance     # 使用者餘額
                self.grid()
                self.create_widgets()

            # 設定介面
            def create_widgets(self):
                self.widgets_list = []    # 部件清單
                self.widgets_error_list = []    # 錯誤訊息清單

                self.lab_title = tk.Label(self, text='創建房間', width=25, height=3, font=self.f_b_title)
                self.lab_title.grid(row=0, column=1, columnspan=3, sticky=tk.SE + tk.NW)
                self.widgets_list.append(self.lab_title)     # 加入部件清單

                self.lab_blank2 = tk.Label(self, text='', width=20, height=5)
                self.lab_blank2.grid(row=0, column=0, rowspan=10, sticky=tk.SE + tk.NW)
                self.widgets_list.append(self.lab_blank2)     # 加入部件清單

                self.lab_blank3 = tk.Label(self, text='', width=20, height=25)
                self.lab_blank3.grid(row=1, column=2, rowspan=9, sticky=tk.SE + tk.NW)
                self.widgets_list.append(self.lab_blank3)     # 加入部件清單

                self.lab_blank4 = tk.Label(self, text='')
                self.lab_blank4.grid(row=3, column=1, sticky=tk.SE + tk.NW)
                self.widgets_list.append(self.lab_blank4)     # 加入部件清單

                self.lab_room_number = tk.Label(self, text='房間號碼', width=15, font=self.f_title)    # 房間號碼
                number = random.randint(1, 10000)        # 亂數產生號碼
                self.number = "{:0>5d}".format(number)   # 不足五位數則前方補零
                # 避免重複房間號碼
                while self.number in self.special_exchange_room.col_values(3):
                    number = random.randint(1, 10000)
                    self.number = "{:0>5d}".format(number)
                self.lab_number = tk.Label(self, text=self.number, font=self.f_lab)        # 以亂數為房間號碼
                self.lab_room_number.grid(row=1, column=1, sticky=tk.SE + tk.NW)
                self.lab_number.grid(row=2, column=1, sticky=tk.SE + tk.NW)
                # 加入部件清單
                self.widgets_list.append(self.lab_room_number)
                self.widgets_list.append(self.lab_number)

                self.lab_room_name = tk.Label(self, text='房間名稱', font=self.f_title)    # 房間名稱
                self.room_name_entry = tk.Entry(self, font=self.f_lab)    # 讓使用者輸入房間名稱
                self.lab_room_name.grid(row=4, column=1, sticky=tk.SE + tk.NW)
                self.room_name_entry.grid(row=5, column=1, sticky=tk.SE + tk.NW)
                # 加入部件清單
                self.widgets_list.append(self.lab_room_name)

                self.lab_room_name_error = tk.Label(self, text='', font=self.f_lab)        # 房間名稱錯誤訊息
                self.lab_room_name_error.grid(row=6, column=1, sticky=tk.SE + tk.NW)
                self.widgets_error_list.append(self.lab_room_name_error)        # 加入部件清單

                self.lab_room_mode = tk.Label(self, text='房間模式', font=self.f_title)    # 房間模式
                self.radioValue = tk.IntVar()
                self.room_mode1 = tk.Radiobutton(self, text='麻將', variable=self.radioValue, value=1, command=self.choose_mode, font=self.f_lab)    # 房間模式-麻將
                self.room_mode2 = tk.Radiobutton(self, text='分錢', variable=self.radioValue, value=2, command=self.choose_mode, font=self.f_lab)    # 房間模式-分錢
                self.room_mode = ''    # 預設為無
                self.lab_room_mode.grid(row=7, column=1, sticky=tk.SE + tk.NW)
                self.room_mode1.grid(row=8, column=1, sticky=tk.SE + tk.NW)
                self.room_mode2.grid(row=9, column=1, sticky=tk.SE + tk.NW)
                # 加入部件清單
                self.widgets_list.append(self.lab_room_mode)
                self.widgets_list.append(self.room_mode1)
                self.widgets_list.append(self.room_mode2)

                self.lab_people_limit = tk.Label(self, text='人數上限', width=15, font=self.f_title)    # 房間人數上限
                self.people_limit_entry = tk.Entry(self, font=self.f_lab)    # 讓使用者輸入人數上限
                self.lab_people_limit.grid(row=1, column=3, sticky=tk.SE + tk.NW)
                self.people_limit_entry.grid(row=2, column=3, sticky=tk.SE + tk.NW)
                # 加入部件清單
                self.widgets_list.append(self.lab_people_limit)

                self.lab_people_limit_error = tk.Label(self, text='', font=self.f_lab)      # 房間人數上限錯誤訊息
                self.lab_people_limit_error.grid(row=3, column=3, sticky=tk.SE + tk.NW)
                self.widgets_error_list.append(self.lab_people_limit_error)      # 加入部件清單

                self.checkVar = tk.IntVar()
                self.check_box_password = tk.Checkbutton(self, text='設定密碼', variable=self.checkVar, command=self.set_password, font=self.f_lab)    # 讓使用者選擇是否要設密碼
                self.lab_password = tk.Label(self, text='密碼', font=self.f_title)          # 密碼
                self.password_entry = tk.Entry(self, state='disable', font=self.f_lab)      # 輸入密碼的欄位，預設為不開啟
                self.password_or_not = '否'    # 預設為沒有密碼
                self.check_box_password.grid(row=5, column=3, sticky=tk.SE + tk.NW)
                self.lab_password.grid(row=4, column=3, sticky=tk.SE + tk.NW)
                self.password_entry.grid(row=6, column=3, sticky=tk.SE + tk.NW)
                # 加入部件清單
                self.widgets_list.append(self.check_box_password)
                self.widgets_list.append(self.lab_password)

                self.lab_password_entry_error = tk.Label(self, text='', font=self.f_lab)    # 密碼輸入錯誤訊息
                self.lab_password_entry_error.grid(row=7, column=3, sticky=tk.SE + tk.NW)
                self.widgets_error_list.append(self.lab_password_entry_error)    # 加入部件清單

                self.butn_create = tk.Button(self, text='創建', command=self.create_room, font=self.f_lab)    # 創建按紐
                self.butn_cancel = tk.Button(self, text='取消', command=lambda: special_exchange_page(self), font=self.f_lab)    # 取消按紐
                self.butn_create.grid(row=8, column=3, sticky=tk.SE + tk.NW)
                self.butn_cancel.grid(row=9, column=3, sticky=tk.SE + tk.NW)
                # 加入部件清單
                self.widgets_list.append(self.butn_create)
                self.widgets_list.append(self.butn_cancel)

                Exchange_system.Special_exchange.set_bg_fg(self.widgets_list)    # 更改物件的文字顏色跟背景顏色
                Exchange_system.Special_exchange.set_bg_fg_error(self.widgets_error_list)    # 更改錯誤訊息的文字顏色跟背景顏色

            # 選擇房間模式
            def choose_mode(self):
                # 使願者選擇麻將模式
                if self.radioValue.get() == 1:
                    self.room_mode = '麻將'    # 房間模式
                    self.people_limit_entry = tk.Label(self, text=4, font=self.f_lab)       # 強制設定人數上限
                    self.people_limit_entry.grid(row=2, column=3, sticky=tk.SE + tk.NW)
                    Exchange_system.Special_exchange.set_bg_fg([self.people_limit_entry])    # 更改物件的文字顏色跟背景顏色
                # 使願者選擇分錢模式:
                else:
                    self.room_mode = '分錢'    # 房間模式
                    self.people_limit_entry = tk.Entry(self)    # 讓使用者輸入人數上限
                    self.people_limit_entry.grid(row=2, column=3, sticky=tk.SE + tk.NW)

            # 是否設定密碼
            def set_password(self):
                # 是
                if self.checkVar.get() == 1:
                    self.password_or_not = '是'    # 是否需要密碼?
                    self.password_entry = tk.Entry(self, show='*')    # 開啟設定密碼的欄位
                    self.password_entry.grid(row=6, column=3, sticky=tk.SE + tk.NW)
                # 否
                else:
                    self.password_or_not = '否'    # 是否需要密碼?
                    self.lab_password_entry_error.configure(text='')
                    self.password_entry = tk.Entry(self, state='disable')    # 關閉設定密碼的欄位
                    self.password_entry.grid(row=6, column=3, sticky=tk.SE + tk.NW)

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

                try:
                    self.sheet_of_room = NTU_Coin.worksheet('Room %s' % (room_number))    # 該房間的表單
                # 房間已被關閉
                except Exception as error:
                    tk.messagebox.showwarning(title='強制離開房間', message='房間已結算')
                    special_exchange_page(self)    # 導回特殊交換主頁
                # 房間未被關閉
                else:
                    self.f_title = tk.font.Font(size=16, family='Microsoft JhengHei', weight='bold')    # 標題字形
                    self.f_b_title = tk.font.Font(size=45, family='Viner Hand ITC', weight='bold')      # 大標題字形
                    self.f_bbb_title = tk.font.Font(size=90, family='Viner Hand ITC', weight='bold')    # 超大標題字形
                    self.f_lab = tk.font.Font(size=12, family='Microsoft JhengHei', weight='bold')      # 一般字形
                    self.f_b_lab = tk.font.Font(size=16, family='Microsoft JhengHei', weight='bold')    # 較大字形
                    self.special_exchange_room = NTU_Coin.get_worksheet(3)      # 特殊交換的房間表單
                    self.sheet_of_room = NTU_Coin.worksheet('Room %s' % (room_number))    # 該房間的表單
                    self.room = self.special_exchange_room.find(room_number)    # 該房間
                    self.user_account = user_account    # 使用者帳號
                    self.room_mode = room_mode          # 房間模式
                    self.room_name = room_name          # 房間名稱
                    self.room_number = room_number      # 房間號碼
                    self.people_limit = people_limit    # 房間人數上限
                    self.grid()
                    # 選擇介面
                    if self.room_mode == '麻將':
                        self.grid()
                        self.create_widgets_mj()        # 麻將介面
                        self.member = self.sheet_of_room.col_values(2)[3:]        # 房間成員帳戶名稱名單
                        self.point = self.sheet_of_room.col_values(3)[3:]         # 房間成員分數表單
                        # 將房間成員帳戶名稱名單&分數表單調整順序
                        self.member_ordered = []           # 房間成員帳戶名稱名單(已排序)
                        self.point_ordered = []            # 房間成員分數表單(已排序)
                        self.user_row = self.sheet_of_room.find(self.user_account).row    # 使用者帳號位置
                        for i in range(self.user_row, self.user_row + 4):
                            if i > 7:
                                i -= 4
                            self.member_ordered.append(self.sheet_of_room.cell(i, 2).value)
                            self.point_ordered.append(self.sheet_of_room.cell(i, 3).value)

                    elif self.room_mode == '分錢':
                        self.create_widgets_share()     # 分錢介面

            # 設定麻將介面
            def create_widgets_mj(self):
                self.widgets_list = []     # 部件清單
                self.user_info_list = []   # 使用者資訊清單

                self.lab_blank1 = tk.Label(self)    #　空白部分
                self.lab_blank1.grid(row=0, column=0, rowspan=39, columnspan=34, sticky=tk.NW + tk.SE)
                self.widgets_list.append(self.lab_blank1)    # 加入部件清單

                content = '房間號碼: ' + self.room_number
                self.lab_room_number = tk.Label(self, text=content, font=self.f_lab)    # 房間號碼
                self.lab_room_number.grid(row=0, column=0, sticky=tk.W)
                self.widgets_list.append(self.lab_room_number)    # 加入部件清單

                content = '房間名稱: ' + self.room_name
                self.lab_room_name = tk.Label(self, text=content, font=self.f_lab)      # 房間名稱
                self.lab_room_name.grid(row=1, column=0, sticky=tk.W)
                self.widgets_list.append(self.lab_room_name)    # 加入部件清單

                content = '房間模式: ' + self.room_mode
                self.lab_room_mode = tk.Label(self, text=content, font=self.f_lab)      # 房間模式
                self.lab_room_mode.grid(row=2, column=0, sticky=tk.W)
                self.widgets_list.append(self.lab_room_mode)    # 加入部件清單

                self.lab_title = tk.Label(self, text='MAHJONG', font=self.f_b_title, width=20)    # 房間標題
                self.lab_title.grid(row=0, column=1, rowspan=3, columnspan=32, sticky=tk.NW + tk.SE)
                self.widgets_list.append(self.lab_title)    # 加入部件清單


                self.butn_refresh = tk.Button(self, text='重整房間', command=self.refresh_room,
                                              font=self.f_lab, width=10)    # 重整房間按鈕
                self.butn_refresh.grid(row=0, column=33, sticky=tk.NW + tk.SE)
                self.widgets_list.append(self.butn_refresh)    # 加入部件清單

                self.butn_leave = tk.Button(self, text='離開房間', command=self.leave_room, font=self.f_lab)        # 離開房間按鈕
                self.butn_leave.grid(row=1, column=33, sticky=tk.NW + tk.SE)
                self.widgets_list.append(self.butn_leave)    # 加入部件清單

                load = Image.open('C:\\Users\\tiffany\\Desktop\\姚冠宇\\商管程式設計\\期末project\\NTU-Coin\\麻將4.jpg')
                render = ImageTk.PhotoImage(load)
                self.lab_mj_table = tk.Label(self, image=render)    # 麻將桌
                self.image = render
                self.lab_mj_table.grid(row=5, column=2, rowspan=30, columnspan=30, sticky=tk.NW + tk.SE)
                self.widgets_list.append(self.lab_mj_table)    # 加入部件清單

                self.user1_point = tk.Label(self, text=self.point_ordered[0], font=self.f_title)    # 使用者一的分數
                self.user1_point.grid(row=36, column=17, sticky=tk.NW + tk.SE)
                # 加入使用者資訊清單
                self.user_info_list.append(self.user1_point)

                self.lab_user2 = tk.Label(self, text=self.member_ordered[1] if self.member_ordered[1] != '' else '', font=self.f_b_lab)     # 使用者二
                self.lab_user2.grid(row=20, column=32, sticky=tk.NW + tk.SE)
                self.user2_point = tk.Label(self, text=self.point_ordered[1] if self.point_ordered[1] != '' else '', font=self.f_b_lab)    # 使用者二
                self.user2_point.grid(row=21, column=32, sticky=tk.NW + tk.SE)
                # 加入使用者資訊清單
                self.user_info_list.append(self.lab_user2)
                self.user_info_list.append(self.user2_point)

                self.lab_user3 = tk.Label(self, text=self.member_ordered[2] if self.member_ordered[2] != '' else '', font=self.f_b_lab)     # 使用者三
                self.lab_user3.grid(row=3, column=17, sticky=tk.NW + tk.SE)
                self.user3_point = tk.Label(self, text=self.point_ordered[2] if self.point_ordered[2] != '' else '', font=self.f_b_lab)    # 使用者三
                self.user3_point.grid(row=4, column=17, sticky=tk.NW + tk.SE)
                # 加入使用者資訊清單
                self.user_info_list.append(self.lab_user3)
                self.user_info_list.append(self.user3_point)

                self.lab_user4 = tk.Label(self, text=self.member_ordered[3] if self.member_ordered[3] != '' else '', font=self.f_b_lab)     # 使用者四
                self.lab_user4.grid(row=20, column=1, sticky=tk.NW + tk.SE)
                self.user4_point = tk.Label(self, text=self.point_ordered[3] if self.point_ordered[3] != '' else '', font=self.f_b_lab)    # 使用者四
                self.user4_point.grid(row=21, column=1, sticky=tk.NW + tk.SE)
                # 加入使用者資訊清單
                self.user_info_list.append(self.lab_user4)
                self.user_info_list.append(self.user4_point)

                # 製作下拉選單的內容
                value_list = ['']
                for user in self.member_ordered[1:]:
                    if user != '':
                        value_list.append(user)
                self.combo_user = ttk.Combobox(self, values=value_list, state="readonly")    # 選擇使用者的下拉選單
                self.combo_user.grid(row=37, column=17, sticky=tk.NW + tk.SE)  

                self.butn_end = tk.Button(self, text='結算', font=self.f_lab, command=self.end)    # 結算的按鈕
                self.butn_end.grid(row=38, column=16, sticky=tk.NW + tk.SE)
                self.butn_end.configure(bg='orange red4', fg='white')    

                self.amount_entry = tk.Entry(self)    # 讓使用者輸入金額
                self.amount_entry.grid(row=38, column=17, sticky=tk.NW + tk.SE)

                self.butn_pay = tk.Button(self, text='付錢', font=self.f_lab, command=self.pay)    # 付錢的按紐
                self.butn_pay.grid(row=38, column=18, sticky=tk.NW + tk.SE)
                self.widgets_list.append(self.butn_pay)    # 加入部件清單

                Exchange_system.Special_exchange.set_bg_fg(self.widgets_list)    # 更改物件的文字顏色跟背景顏色
                Exchange_system.Special_exchange.set_bg_fg_user(self.user_info_list)    # 更改使用者資訊的文字顏色跟背景顏色                

            # 付錢
            def pay(self):
                # 避免錯誤
                try:
                    self.sheet_of_room = NTU_Coin.worksheet('Room %s' % (self.room_number))
                # 房間已被關閉
                except Exception as error:
                    self.refresh_room()
                # 房間未被關閉
                else:
                    self.sheet_of_room = NTU_Coin.worksheet('Room %s' % (self.room_number))    # 該房間的表單
                    self.exchange_user = self.combo_user.get()        # 交換帳戶名稱
                    
                    # 確認交換數量為數字
                    self.exchange_amount = self.amount_entry.get()    # 交換數量
                    try:
                        int(self.exchange_amount)
                    except Exception as error:
                        amount_accepted = False
                    else:
                        # 確認家換數量為正值
                        self.exchange_amount = int(self.exchange_amount)
                        if self.exchange_amount > 0:
                            amount_accepted = True
                        else:
                            amount_accepted = False

                    if (self.exchange_user != '') and amount_accepted:
                        self.exchange_user_row = self.sheet_of_room.find(self.exchange_user).row    # 交換帳號位置
                        self.exchange_user_point = int(self.sheet_of_room.acell('C%d' % (self.exchange_user_row)).value)    # 交換帳戶分數
                        self.user_row = self.sheet_of_room.find(self.member_ordered[0]).row         # 使用者帳號位置
                        self.user_point = int(self.point_ordered[0])    # 使用者分數
                        self.user_balance = int(self.sheet_of_room.acell('D%d' % (self.user_row)).value)    # 使用者帳戶餘額

                        # 更新分數
                        self.update_exchange_user_point = self.exchange_user_point + self.exchange_amount      # 欲更新之交換帳戶分數
                        self.update_user_point = self.user_point - self.exchange_amount    # 欲更新之使用者分數
                        # 使用者帳戶餘額不足支付
                        if (-self.update_user_point) > self.user_balance:
                            self.user_rest = self.user_balance + self.user_point    # 使用者剩下的錢
                            self.sheet_of_room.update('C%d' % (self.exchange_user_row), str(self.exchange_user_point + self.user_rest))
                            self.sheet_of_room.update('C%d' % (self.user_row), str(self.user_point - self.user_rest))
                            tk.messagebox.showwarning(title='強制結算', message='您已破產了')
                            self.end()
                        # 足以支付
                        else:
                            self.sheet_of_room.update('C%d' % (self.exchange_user_row), str(self.update_exchange_user_point))
                            self.sheet_of_room.update('C%d' % (self.user_row), str(self.update_user_point))
                            self.refresh_room()    # 重整頁面

            # 結算
            def end(self):
                # 避免錯誤
                try:
                    self.sheet_of_room = NTU_Coin.worksheet('Room %s' % (self.room_number))
                # 房間已被關閉
                except Exception as error:
                    self.refresh_room()
                # 房間未被關閉
                else:
                    self.end_time = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')  # 結算時間
                    # 更新使用者帳戶餘額
                    self.sheet_of_room = NTU_Coin.worksheet('Room %s' % (self.room_number))    # 該房間的表單
                    self.user_balance = self.sheet_of_room.acell('D%d' % (self.user_row)).value    # 使用者帳戶餘額
                    self.user_point = self.sheet_of_room.acell('C%d' % (self.user_row)).value      # 使用者分數
                    self.user_info_row = sheet.find(self.user_account).row    # 使用者資訊位置
                    self.update_user_balance = int(self.user_balance) + int(self.user_point)
                    sheet.update_cell(self.user_info_row, 5, str(self.update_user_balance))

                    # 更新其他使用者之帳戶餘額
                    self.user2_row = self.sheet_of_room.find(self.member_ordered[1]).row    # 使用者二帳號位置
                    self.user2_balance = self.sheet_of_room.acell('D%d' % (self.user2_row)).value    # 使用者二帳戶餘額
                    self.user2_point = self.sheet_of_room.acell('C%d' % (self.user2_row)).value      # 使用者二分數
                    self.user2_account = self.sheet_of_room.acell('A%d' % (self.user2_row)).value    # 使用者二帳號
                    self.user2_info_row = sheet.find(self.member_ordered[1]).row    # 使用者二資訊位置
                    self.update_user2_balance = int(self.user2_balance) + int(self.user2_point)
                    sheet.update_cell(self.user2_info_row, 5, str(self.update_user2_balance))

                    self.user3_row = self.sheet_of_room.find(self.member_ordered[2]).row    # 使用者三帳號位置
                    self.user3_balance = self.sheet_of_room.acell('D%d' % (self.user3_row)).value    # 使用者三帳戶餘額
                    self.user3_point = self.sheet_of_room.acell('C%d' % (self.user3_row)).value      # 使用者三分數
                    self.user3_account = self.sheet_of_room.acell('A%d' % (self.user3_row)).value    # 使用者三帳號
                    self.user3_info_row = sheet.find(self.member_ordered[2]).row    # 使用者三資訊位置
                    self.update_user3_balance = int(self.user3_balance) + int(self.user3_point)
                    sheet.update_cell(self.user3_info_row, 5, str(self.update_user3_balance))

                    self.user4_row = self.sheet_of_room.find(self.member_ordered[3]).row    # 使用者四帳號位置
                    self.user4_balance = self.sheet_of_room.acell('D%d' % (self.user4_row)).value    # 使用者四帳戶餘額
                    self.user4_point = self.sheet_of_room.acell('C%d' % (self.user4_row)).value      # 使用者四分數
                    self.user4_account = self.sheet_of_room.acell('A%d' % (self.user4_row)).value    # 使用者四帳號
                    self.user4_info_row = sheet.find(self.member_ordered[3]).row    # 使用者四資訊位置
                    self.update_user4_balance = int(self.user4_balance) + int(self.user4_point)
                    sheet.update_cell(self.user4_info_row, 5, str(self.update_user4_balance))

                    self.upload_record()    # 上傳紀錄
                    NTU_Coin.del_worksheet(self.sheet_of_room)    # 刪除該房間的表單
                    self.special_exchange_room.delete_rows(self.room.row)    # 刪除該房間的資訊
                    special_exchange_page(self)    # 導回主畫面

            # 設定分錢介面
            def create_widgets_share(self):
                self.widgets_list = []     # 部件清單

                self.lab_blank1 = tk.Label(self)    #　空白部分
                self.lab_blank1.grid(row=0, column=0, rowspan=3, sticky=tk.NW + tk.SE)
                self.widgets_list.append(self.lab_blank1)    # 加入部件清單
                
                self.lab_title = tk.Label(self, text='COMING SOON', font=self.f_b_title, width=27, height=6)    # 房間標題
                self.lab_title.grid(row=0, column=0, sticky=tk.NW + tk.SE)
                self.widgets_list.append(self.lab_title)     # 加入部件清單

                self.butn_leave = tk.Button(self, text='離開房間', command=self.leave_room, font=self.f_lab)    # 離開房間按鈕
                self.butn_leave.grid(row=1, column=0, rowspan=2, sticky=tk.W)
                self.widgets_list.append(self.butn_leave)    # 加入部件清單

                Exchange_system.Special_exchange.set_bg_fg(self.widgets_list)    # 更改物件的文字顏色跟背景顏色

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
                    self.sheet_of_room.add_rows(0)

                special_exchange_page(self)    # 回到特殊交換系統

            # 上傳紀錄
            def upload_record(self):
                self.exchange_record_sheet = NTU_Coin.get_worksheet(2)    # 交換記錄表單
                num_rows = len(self.exchange_record_sheet.col_values(1))
                row1 = [str(num_rows + 1), 'spec', self.user_account, '', self.user_point, self.user_balance, self.end_time, '麻將']
                row2 = [str(num_rows + 2), 'spec', self.user2_account, '', self.user2_point, self.user2_balance, self.end_time, '麻將']
                row3 = [str(num_rows + 3), 'spec', self.user3_account, '', self.user3_point, self.user3_balance, self.end_time, '麻將']
                row4 = [str(num_rows + 4), 'spec', self.user4_account, '', self.user4_point, self.user4_balance, self.end_time, '麻將']
                insert_rows = [row1, row2, row3, row4]
                self.exchange_record_sheet.append_rows(insert_rows)    # 新增紀錄


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
    spec_ex.master.geometry('1024x699')
    spec_ex.master.configure(bg='#363636')
    spec_ex.master.resizable(False, False)
    spec_ex.mainloop()


scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("C:\\Users\\tiffany\\Desktop\\姚冠宇\\商管程式設計\\期末project\\NTU Coin-adba92770851.json", scope)
client = gspread.authorize(creds)
NTU_Coin = client.open('NTU Coin')
sheet = NTU_Coin.get_worksheet(0)  # Open the spreadhseet


account = 'admin@gmail.com'    # 使用者帳號(從登入資訊抓來)
ex_system = Exchange_system()
exchange_homepage(ex_system)
