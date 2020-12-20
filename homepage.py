import tkinter as tk
from tkinter import ttk
import sys
import os
import re
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint
import datetime
import textwrap
import random
# from func1_png import img as func1
# from pageBackground_png import img as pageBackground
# import base64
"""
顏色代碼：
#283845 夜幕藍
#363636 微黑
#DF9A57 金色
文字大小為微軟正黑58粗體
系統按鍵字體為微軟正黑70粗體
確認鍵字體為22
"""

def login():
    """登入畫面"""
    # 背景頁建立
    global loginWin
    loginWin = tk.Frame(win)
    loginWin.config(width = 1024, height = 699, bg = "#363636")
    loginWin.place(x = 0, y = 0)

    # 標題建立
    global ntuCoinImg
    ntuCoinImg = tk.PhotoImage(file = "ntucoin.png")
    title = tk.Label(loginWin)
    title.config(image = ntuCoinImg, width = 450, height = 88)
    title.place(anchor = "n",x=512, y=50)

    # 用戶輸入欄
    global login_userText
    userTitle = tk.Label(loginWin, text = "電郵地址")
    userTitle.config(font = "微軟正黑體 14 bold", bg = "#363636", fg = "white")
    userTitle.place(anchor = "w", x = 300, y = 200)
    user = tk.Entry(loginWin)
    login_userText = tk.StringVar()
    user.config(textvariable = login_userText, width = 38, font = "arial 14")
    user.place(anchor = "w", x = 300, y = 230)

    global uW
    uW = tk.StringVar()
    uW.set("")
    userWarning = tk.Label(loginWin, textvariable = uW)
    userWarning.config(font = "微軟正黑體 10", bg = "#363636", fg = "red")
    userWarning.place(anchor = "w", x = 300, y = 255)

    # 密碼欄
    global login_passwordText
    passwordTitle = tk.Label(loginWin, text = "密碼")
    passwordTitle.config(font = "微軟正黑體 14 bold", bg = "#363636", fg = "white")
    passwordTitle.place(anchor = "w", x = 300, y = 280)
    password = tk.Entry(loginWin)
    login_passwordText = tk.StringVar()
    password.config(textvariable = login_passwordText, width = 38, font = "arial 14", show = "●")
    password.place(anchor = "w", x = 300, y = 310)

    global pW
    pW = tk.StringVar()
    pW.set("")
    passwordWarning = tk.Label(loginWin, textvariable = pW)
    passwordWarning.config(font = "微軟正黑體 10", bg = "#363636", fg = "red")
    passwordWarning.place(anchor = "w", x = 300, y = 335)

    # 登入鍵
    global loginInImg
    loginInImg = tk.PhotoImage(file = "登入鍵.png")
    loginBtn = tk.Button(loginWin)
    loginBtn.config(image = loginInImg, relief = "flat", width = 450, height = 36)
    loginBtn.config(command = findAccount, cursor = "hand2")
    loginBtn.place(anchor = "center", x = 512, y = 370)

    # 未註冊帳戶提示
    global notSignUpImg
    notSignUpImg = tk.PhotoImage(file = "未註冊帳戶.png")
    loginBtn = tk.Label(loginWin)
    loginBtn.config(image = notSignUpImg, relief = "flat", width = 450, height = 74)
    loginBtn.place(anchor = "center", x = 512, y = 483)

    # 註冊鍵
    global signUpImg
    signUpImg = tk.PhotoImage(file = "註冊鍵.png")
    loginBtn = tk.Button(loginWin)
    loginBtn.config(image = signUpImg, relief = "flat", width = 450, height = 36)
    loginBtn.config(command = signUp, cursor = "hand2")
    loginBtn.place(anchor = "center", x = 512, y = 550)

    # 離開鍵
    exitBtn = tk.Button(loginWin, text = "離開系統\nExit")
    exitBtn.config(font = "微軟正黑體 15 bold", bg = "#363636", fg = "white", relief = "flat")
    exitBtn.config(activebackground = "#363636", activeforeground = "#DF2935")
    exitBtn.config(command = whetherExit, cursor = "hand2")
    exitBtn.place(anchor = "se",x=1024, y=699)


def findAccount():
    global userInfo
    scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("NTU Coin-0555c96087e3.json", scope)
    client = gspread.authorize(creds)
    sheet = client.open("NTU Coin").get_worksheet(0)  # Open the spreadhseet
    mail = sheet.col_values(2)
    # 檢驗信箱
    if login_userText.get() in mail:
        index = mail.index(login_userText.get()) + 1
        userInfo = sheet.row_values(index)
        # 接著檢驗密碼
        if login_passwordText.get() == userInfo[2]:
            pW.set("")
            homepage()
            # print(userInfo)
        else:
            uW.set("")
            pW.set("❕ 密碼錯誤")
    else:
        uW.set("❕ 您尚未註冊")
        pW.set("")


def signUp():
    """註冊頁面"""
    # 背景頁建立
    global signUpWin
    signUpWin = tk.Frame(loginWin)
    signUpWin.config(width = 1024, height = 699, bg = "#363636")
    signUpWin.place(x = 0, y = 0)

    # 標題建立
    global ntuCoinImg
    ntuCoinImg = tk.PhotoImage(file = "ntucoin.png")
    title = tk.Label(signUpWin)
    title.config(image = ntuCoinImg, width = 450, height = 88)
    title.place(anchor = "n",x=512, y=20)

    sign = tk.Label(signUpWin, text = "以電子郵件地址註冊")
    sign.config(font = "微軟正黑體 20 bold", bg = "#363636", fg = "white")
    sign.place(anchor = "center", x = 512, y = 130)

    # 輸入電子信箱欄
    mailTitle = tk.Label(signUpWin, text = "您的電子郵件地址是什麼？")
    mailTitle.config(font = "微軟正黑體 14 bold", bg = "#363636", fg = "white")
    mailTitle.place(anchor = "w", x = 300, y = 180)

    global signUp_mailText
    mail = tk.Entry(signUpWin)
    signUp_mailText = tk.StringVar()
    mail.config(textvariable = signUp_mailText, width = 38, font = "arial 14")
    mail.place(anchor = "w", x = 300, y = 210)

    # 建立密碼
    passwordTitle = tk.Label(signUpWin, text = "建立密碼")
    passwordTitle.config(font = "微軟正黑體 14 bold", bg = "#363636", fg = "white")
    passwordTitle.place(anchor = "w", x = 300, y = 260)

    global signUp_passwordText
    password = tk.Entry(signUpWin)
    signUp_passwordText = tk.StringVar()
    password.config(textvariable = signUp_passwordText, width = 38, font = "arial 14", show = "●")
    password.place(anchor = "w", x = 300, y = 290)

    # 確認密碼
    confirmTitle = tk.Label(signUpWin, text = "確認密碼")
    confirmTitle.config(font = "微軟正黑體 14 bold", bg = "#363636", fg = "white")
    confirmTitle.place(anchor = "w", x = 300, y = 340)

    global signUp_confirmText
    confirm = tk.Entry(signUpWin)
    signUp_confirmText = tk.StringVar()
    confirm.config(textvariable = signUp_confirmText, width = 38, font = "arial 14", show = "●")
    confirm.place(anchor = "w", x = 300, y = 370)

    # 用戶名稱
    userTitle = tk.Label(signUpWin, text = "用戶名稱（12個字元以下，限英文和數字）")
    userTitle.config(font = "微軟正黑體 14 bold", bg = "#363636", fg = "white")
    userTitle.place(anchor = "w", x = 300, y = 420)

    global signUp_userText
    user = tk.Entry(signUpWin)
    signUp_userText = tk.StringVar()
    user.config(textvariable = signUp_userText, width = 38, font = "arial 14")
    user.place(anchor = "w", x = 300, y = 450)

    # 交易密碼
    transactionTitle = tk.Label(signUpWin, text = "8位數字的交易密碼（供之後交易使用）")
    transactionTitle.config(font = "微軟正黑體 14 bold", bg = "#363636", fg = "white")
    transactionTitle.place(anchor = "w", x = 300, y = 500)

    global signUp_transactionText
    transaction = tk.Entry(signUpWin)
    signUp_transactionText = tk.StringVar()
    transaction.config(textvariable = signUp_transactionText, width = 38, font = "arial 14", show = "●")
    transaction.place(anchor = "w", x = 300, y = 530)
    
    # 註冊鍵
    global signUpImg
    signUpImg = tk.PhotoImage(file = "註冊鍵.png")
    loginBtn = tk.Button(signUpWin)
    loginBtn.config(image = signUpImg, relief = "flat", width = 450, height = 36)
    loginBtn.config(command = checkSignUpInfo, cursor = "hand2")
    loginBtn.place(anchor = "center", x = 512, y = 590)


    # 已經有帳戶了？
    haveAnAccountTitle = tk.Label(signUpWin, text = "已經有帳戶了？")
    haveAnAccountTitle.config(font = "微軟正黑體 22 bold", bg = "#363636", fg = "white")
    haveAnAccountTitle.place(anchor = "center", x = 512, y = 640)

    haveAnAccountBtn = tk.Button(signUpWin, text = "登入 > ")
    haveAnAccountBtn.config(font = "微軟正黑體 16 bold underline", bg = "#363636", fg = "#0066CC")
    haveAnAccountBtn.config(relief = "flat", activebackground = "#363636", activeforeground = "white")
    haveAnAccountBtn.config(command = login, cursor = "hand2")
    haveAnAccountBtn.place(anchor = "center", x = 512, y = 680)

    """錯誤信息欄"""
    # 檢查信箱欄
    global mW
    mW = tk.StringVar()
    mW.set("")
    mailWarning = tk.Label(signUpWin, textvariable = mW)
    mailWarning.config(font = "微軟正黑體 10", bg = "#363636", fg = "red")
    mailWarning.place(anchor = "w", x = 300, y = 235)

    # 檢查密碼欄
    global p1W
    p1W = tk.StringVar()
    p1W.set("")
    password1Warning = tk.Label(signUpWin, textvariable = p1W)
    password1Warning.config(font = "微軟正黑體 10", bg = "#363636", fg = "red")
    password1Warning.place(anchor = "w", x = 300, y = 315)

    # 檢查密碼確認欄
    global p2W
    p2W = tk.StringVar()
    p2W.set("")
    password2Warning = tk.Label(signUpWin, textvariable = p2W)
    password2Warning.config(font = "微軟正黑體 10", bg = "#363636", fg = "red")
    password2Warning.place(anchor = "w", x = 300, y = 395)
    
    # 檢查用戶名稱欄
    global nW
    nW = tk.StringVar()
    nW.set("")
    nameWarning = tk.Label(signUpWin, textvariable = nW)
    nameWarning.config(font = "微軟正黑體 10", bg = "#363636", fg = "red")
    nameWarning.place(anchor = "w", x = 300, y = 475)

    # 交易密碼名稱欄
    global tW
    tW = tk.StringVar()
    tW.set("")
    transactionWarning = tk.Label(signUpWin, textvariable = tW)
    transactionWarning.config(font = "微軟正黑體 10", bg = "#363636", fg = "red")
    transactionWarning.place(anchor = "w", x = 300, y = 555)


def checkSignUpInfo():
    """檢查輸入的資訊是否符合規則"""
    scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("NTU Coin-0555c96087e3.json", scope)
    client = gspread.authorize(creds)
    sheet = client.open("NTU Coin").get_worksheet(0)  # Open the spreadhseet
    mails = sheet.col_values(2)
    names = sheet.col_values(4)
    numRows = len(mails)

    mail = signUp_mailText.get()
    password1 = signUp_passwordText.get()
    password2 = signUp_confirmText.get()
    userName = signUp_userText.get()
    state = []  # 最後用來判斷有無錯誤發生
    # 印出錯誤信息
    if mail == "":
        mW.set("❕ 此欄不得為空")
    else:
        data = re.findall(r"^[a-zA-Z0-9][\w\.-]*[a-zA-Z0-9]@ntu.edu.tw", mail)
        if len(data) != 1:
            mW.set("❕ 電郵地址不符合格式")
        else:
            if signUp_mailText.get() in mails:
                mW.set("❕ 此電郵已被註冊")
            else:
                mW.set("")
                state.append(0)

    if password1 == "":
        p1W.set("❕ 此欄不得為空")
    else:
        p1W.set("")
        state.append(0)

    if password2 == "":
        p2W.set("❕ 此欄不得為空")
    else:
        if password1 != password2:
            p2W.set("❕ 兩次密碼不相同")
        else:
            p2W.set("")
            state.append(0)

    if userName == "":
        nW.set("❕ 此欄不得為空")
    else: 
        if len(userName) > 12:
            nW.set("❕ 用戶名稱不符合規範")
        else:
            if signUp_userText.get() in names:
                nW.set("❕ 此用戶名已被註冊")
            else:
                status = True
                for i in range(len(userName)):
                    if "a" <= userName[i] <= "z" or "A" <= userName[i] <= "Z" or "0" <= userName[i] <= "9":
                        pass
                    else:
                        nW.set("❕ 用戶名稱不符合規範")
                        status = False
                        break
                if status == True:
                    nW.set("")
                    state.append(0)

    if signUp_transactionText.get() == "":
        tW.set("❕ 此欄不得為空")
    else:
        if len(signUp_transactionText.get()) != 8:
            tW.set("❕ 交易密碼不符合規範")
        else:
            tW.set("")
            state.append(0)
    if len(state) == 5: # 若回傳四個0即代表五個欄位都符合規格
        ls = [str(numRows + 1), signUp_mailText.get(), signUp_passwordText.get(), signUp_userText.get(), "0", signUp_transactionText.get()]
        sheet.append_row(ls, table_range="A{}".format(numRows + 1))
        login()


def homepage():
    """主畫面"""
    global homeWin
    # 主畫面建立
    homeWin = tk.Frame(win)
    homeWin.config(width = 1024, height = 699, bg = "#363636")
    homeWin.place(x = 0, y = 0)


    # 標題建立
    global ntuCoinImg
    title = tk.PhotoImage(file = "ntucoin.png")
    title = tk.Label(homeWin)
    title.config(image = ntuCoinImg, width = 450, height = 88)
    title.place(anchor = "n",x=512, y=20)

    # 離開鍵建立
    exitBtn = tk.Button(homeWin, text = "離開系統\nExit")
    exitBtn.config(font = "微軟正黑體 15 bold", bg = "#363636", fg = "white", relief = "flat")
    exitBtn.config(activebackground = "#363636", activeforeground = "#DF2935")
    exitBtn.config(command = whetherExit, cursor = "hand2")
    # exitBtn.config(font = "微軟正黑體 15 bold", bg = "#DF9A57", fg = "black", relief = "solid", command = changeFullScreen)
    exitBtn.place(anchor = "se",x=1024, y=699)

    # 功能鍵建立
    global exchangeImg
    global taskImg
    global valueImg
    global recordImg
    exchangeImg = tk.PhotoImage(file = "貨幣交換.png")
    taskImg = tk.PhotoImage(file = "任務.png")
    valueImg = tk.PhotoImage(file = "儲值.png")
    recordImg = tk.PhotoImage(file = "記錄查詢.png")

    exchange = tk.Button(homeWin)
    exchange.config(image = exchangeImg, width = 150, height = 400)
    exchange.config(relief = "flat")
    exchange.config(command = exchangeSys, cursor = "hand2")
    exchange.place(anchor = "w", x = 85, y = 350)

    task = tk.Button(homeWin)
    task.config(image = taskImg, width = 150, height = 400)
    task.config(relief = "flat")
    task.config(command = taskSys, cursor = "hand2")
    task.place(anchor = "w", x = 320, y = 350)

    value = tk.Button(homeWin)
    value.config(image = valueImg, width = 150, height = 400)
    value.config(relief = "flat")
    value.config(command = valueSys, cursor = "hand2")
    value.place(anchor = "w", x = 554, y = 350)

    record = tk.Button(homeWin)
    record.config(image = recordImg, width = 150, height = 400)
    record.config(relief = "flat")
    record.config(command = recordSys, cursor = "hand2")
    record.place(anchor = "w", x = 789, y = 350)


    # 說明鍵建立
    helpBtn = tk.Button(homeWin, text = "功能說明\nHelp")
    helpBtn.config(font = "微軟正黑體 15 bold", bg = "#363636", fg = "white", relief = "flat")
    helpBtn.config(activebackground = "#363636", activeforeground = "#DF2935")
    helpBtn.config(command = helpPage, cursor = "hand2")
    helpBtn.place(anchor = "sw",x=0, y=699)


def changeFullScreen():
    """切換全螢幕"""

    global state
    state = not state
    if state == False:
        win.attributes("-fullscreen", state)
        win.geometry("1024x768+172+0")
        exitBtn.config(text = "打開全螢幕\nExpand")
    else:
        win.attributes("-fullscreen", state)
        exitBtn.config(text = "退出全螢幕\nExit")


def exit():
    """離開系統"""
    sys.exit()


def whetherExit():
    """詢問是否離開"""

    # 確認是否離開畫面
    # whetherExitWin = tk.Label()
    # whetherExitWin.config(text = "您確定要離開系統嗎？\n", font = "微軟正黑體 40 bold", bg = "#99B2DD")
    # whetherExitWin.config(width = 18, height = 4)
    whetherExitWin = tk.Frame(win)
    whetherExitWin.config(width = 600, height = 300, bg = "#99B2DD")
    whetherExitWin.place(anchor = "center", x = 512, y = 350)

    whetherExitText = tk.Label(whetherExitWin)
    whetherExitText.config(text = "您確定要離開系統嗎？\n", font = "微軟正黑體 38 bold", bg = "#99B2DD")
    whetherExitText.config(width = 16, height = 8)
    whetherExitText.place(anchor = "center", x= 300, y = 120)

    # YES鍵
    yesBtn = tk.Button(whetherExitWin, text = "YES")
    yesBtn.config(font = "微軟正黑體 30 bold", bg = "#F3BB91", fg = "red", activebackground = "yellow")
    yesBtn.config(relief = "flat")
    yesBtn.config(command = exit, cursor = "hand2")
    yesBtn.place(anchor = "center", x = 200, y = 200)
    
    # NO鍵
    noBtn = tk.Button(whetherExitWin, text = "NO")
    noBtn.config(font = "微軟正黑體 30 bold", bg = "#F3BB91", fg = "blue", activebackground = "yellow")
    noBtn.config(relief = "flat")
    noBtn.config(command = whetherExitWin.destroy, cursor = "hand2")
    noBtn.place(anchor = "center", x = 390, y = 200)

    whetherExitWin.place(anchor = "center", x = 512, y = 350)


def helpPage():
    """說明頁"""
    # 背景頁建立
    helpWin = tk.Frame(homeWin)
    helpWin.config(width = 1024, height = 699, bg = "#363636")
    helpWin.place(x = 0, y = 0)

    # 返回鍵建立
    backBtn = tk.Button(helpWin, text = "回到首頁\nBack")
    backBtn.config(font = "微軟正黑體 15 bold", bg = "#363636", fg = "white", relief = "flat")
    backBtn.config(activebackground = "#363636", activeforeground = "#DF2935")
    backBtn.config(command = helpWin.destroy, cursor = "hand2")
    backBtn.place(anchor = "se",x=1024, y=699)

    # 說明文字建立
    helpText1 = tk.Label(helpWin, text = "  NTU Coin")
    helpText1.config(font = "微軟正黑體 45 bold", bg = "#363636", fg = "white")

    helpText2 = tk.Label(helpWin, text = """
    NTU Coin 使得臺大教職員生交易更便利！舉凡是\n
    臺大內部需要付錢的地方（學餐、小福、便利商店\n
    、停車費、影印費、販賣機等等），皆可使用NTU \n
    Coin 進行支付。同時，大多數臺大周圍的餐廳、\n
    店家也接受NTU Coin。NTU Coin 由臺大校方負責\n
    發行及兌換，以確保NTU Coin的可流通性。
    """)
    helpText2.config(font = "微軟正黑體 24 bold", bg = "#363636", fg = "white", justify = "left")

    helpText1.place(x = 0, y = 20)
    helpText2.place(x = 0, y = 100)


def exchangeSys():
    """貨幣交換系統"""
    # 背景頁建立
    global exchangeSysWin
    exchangeSysWin = tk.Frame(homeWin)
    exchangeSysWin.config(width = 1024, height = 699, bg = "#363636")
    exchangeSysWin.place(x = 0, y = 0)

    # 返回鍵建立
    backBtn = tk.Button(exchangeSysWin, text = "回到首頁\nBack")
    backBtn.config(font = "微軟正黑體 15 bold", bg = "#363636", fg = "white", relief = "flat")
    backBtn.config(activebackground = "#363636", activeforeground = "#DF2935")
    backBtn.config(command = exchangeSysWin.destroy, cursor = "hand2")
    backBtn.place(anchor = "se",x=1024, y=699)

    # 標題
    title = tk.Label(exchangeSysWin, text = "貨幣交換系統")
    title.config(font = "微軟正黑體 48 bold", bg = "#363636", fg = "white")
    title.place(anchor = "center", x = 512, y = 60)

    # 一般交換
    global Img_exchangeSys_exchange_normal
    Img_exchangeSys_exchange_normal = tk.PhotoImage(file = "一般交換.png")
    exchange_normal_Btn = tk.Button(exchangeSysWin)
    exchange_normal_Btn.config(image = Img_exchangeSys_exchange_normal, width = 790, height = 140)
    exchange_normal_Btn.config(relief = "flat", cursor = "hand2", command = exchangeSys_normal)
    exchange_normal_Btn.place(anchor = "center", x = 512, y = 250)

    # 特殊交換
    global Img_exchangeSys_exchange_special
    Img_exchangeSys_exchange_special = tk.PhotoImage(file = "特殊交換.png")
    exchange_special_Btn = tk.Button(exchangeSysWin)
    exchange_special_Btn.config(image = Img_exchangeSys_exchange_special, width = 790, height = 140)
    exchange_special_Btn.config(relief = "flat", cursor = "hand2")
    exchange_special_Btn.place(anchor = "center", x = 512, y = 440)


def exchangeSys_normal():
    """一般交換系統"""
    # 背景頁建立
    global exchangeSys_normal_Win
    exchangeSys_normal_Win = tk.Frame(exchangeSysWin)
    exchangeSys_normal_Win.config(width = 1024, height = 699, bg = "#363636")
    exchangeSys_normal_Win.place(x = 0, y = 0)

    # 返回鍵建立
    backBtn = tk.Button(exchangeSys_normal_Win, text = "回到上頁\nBack")
    backBtn.config(font = "微軟正黑體 15 bold", bg = "#363636", fg = "white", relief = "flat")
    backBtn.config(activebackground = "#363636", activeforeground = "#DF2935")
    backBtn.config(command = exchangeSys_normal_Win.destroy, cursor = "hand2")
    backBtn.place(anchor = "se",x=1024, y=699)

    # 標題
    title = tk.Label(exchangeSys_normal_Win, text = "一般交換系統")
    title.config(font = "微軟正黑體 48 bold", bg = "#363636", fg = "white")
    title.place(anchor = "center", x = 512, y = 60)

    # 交換帳號欄
    mailTitle = tk.Label(exchangeSys_normal_Win, text = "交易帳號")
    mailTitle.config(font = "微軟正黑體 14 bold", bg = "#363636", fg = "white")
    mailTitle.place(anchor = "w", x = 300, y = 180)

    global exchangeSys_normal_Win_mailText
    mail = tk.Entry(exchangeSys_normal_Win)
    exchangeSys_normal_Win_mailText = tk.StringVar()
    mail.config(textvariable = exchangeSys_normal_Win_mailText, width = 38, font = "arial 14")
    mail.place(anchor = "w", x = 300, y = 210)

    # 交換數量欄
    quantityTitle = tk.Label(exchangeSys_normal_Win, text = "交易數量")
    quantityTitle.config(font = "微軟正黑體 14 bold", bg = "#363636", fg = "white")
    quantityTitle.place(anchor = "w", x = 300, y = 260)

    global exchangeSys_normal_Win_quantityText
    quantity = tk.Entry(exchangeSys_normal_Win)
    exchangeSys_normal_Win_quantityText = tk.StringVar()
    quantity.config(textvariable = exchangeSys_normal_Win_quantityText, width = 38, font = "arial 14")
    quantity.place(anchor = "w", x = 300, y = 290)

    # 交易密碼欄
    passwordTitle = tk.Label(exchangeSys_normal_Win, text = "交易密碼")
    passwordTitle.config(font = "微軟正黑體 14 bold", bg = "#363636", fg = "white")
    passwordTitle.place(anchor = "w", x = 300, y = 340)

    global exchangeSys_normal_Win_passwordText
    password = tk.Entry(exchangeSys_normal_Win)
    exchangeSys_normal_Win_passwordText = tk.StringVar()
    password.config(textvariable = exchangeSys_normal_Win_passwordText, width = 38, font = "arial 14", show = "●")
    password.place(anchor = "w", x = 300, y = 370)

    # 備註欄
    remarkTitle = tk.Label(exchangeSys_normal_Win, text = "備註")
    remarkTitle.config(font = "微軟正黑體 14 bold", bg = "#363636", fg = "white")
    remarkTitle.place(anchor = "w", x = 300, y = 420)

    global exchangeSys_normal_Win_remarkText
    remark = tk.Entry(exchangeSys_normal_Win)
    exchangeSys_normal_Win_remarkText = tk.StringVar()
    remark.config(textvariable = exchangeSys_normal_Win_remarkText, width = 38, font = "arial 14")
    remark.place(anchor = "w", x = 300, y = 450)

    # 確認鍵
    global exchangeSys_normal_Win_sureImg
    exchangeSys_normal_Win_sureImg = tk.PhotoImage(file = "確認.png")
    exchangeSys_normal_Win_sureBtn = tk.Button(exchangeSys_normal_Win)
    exchangeSys_normal_Win_sureBtn.config(image = exchangeSys_normal_Win_sureImg, relief = "flat", width = 450, height = 36)
    exchangeSys_normal_Win_sureBtn.config(command = exchangeSys_normal_check, cursor = "hand2")
    exchangeSys_normal_Win_sureBtn.place(anchor = "center", x = 512, y = 540)

    """建立錯誤信息"""
    # 檢查信箱欄
    global exchangeSys_normal_Win_mW
    exchangeSys_normal_Win_mW = tk.StringVar()
    exchangeSys_normal_Win_mW.set("")
    exchangeSys_normal_Win_mailWarning = tk.Label(exchangeSys_normal_Win, textvariable = exchangeSys_normal_Win_mW)
    exchangeSys_normal_Win_mailWarning.config(font = "微軟正黑體 10", bg = "#363636", fg = "red")
    exchangeSys_normal_Win_mailWarning.place(anchor = "w", x = 300, y = 235)

    # 檢查數量欄
    global exchangeSys_normal_Win_qW
    exchangeSys_normal_Win_qW = tk.StringVar()
    exchangeSys_normal_Win_qW.set("")
    exchangeSys_normal_Win_quantityWarning = tk.Label(exchangeSys_normal_Win, textvariable = exchangeSys_normal_Win_qW)
    exchangeSys_normal_Win_quantityWarning.config(font = "微軟正黑體 10", bg = "#363636", fg = "red")
    exchangeSys_normal_Win_quantityWarning.place(anchor = "w", x = 300, y = 315)

    # 檢查密碼確認欄
    global exchangeSys_normal_Win_pW
    exchangeSys_normal_Win_pW = tk.StringVar()
    exchangeSys_normal_Win_pW.set("")
    exchangeSys_normal_Win_passwordWarning = tk.Label(exchangeSys_normal_Win, textvariable = exchangeSys_normal_Win_pW)
    exchangeSys_normal_Win_passwordWarning.config(font = "微軟正黑體 10", bg = "#363636", fg = "red")
    exchangeSys_normal_Win_passwordWarning.place(anchor = "w", x = 300, y = 395)


def exchangeSys_normal_check():
    """確認輸入資訊正確"""
    scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("NTU Coin-0555c96087e3.json", scope)
    client = gspread.authorize(creds)
    sheet = client.open("NTU Coin").get_worksheet(0)  # Open the spreadhseet

    # 抓取使用者帳戶資訊
    user_account_all = sheet.col_values(2)            # 大家的帳號(Email)
    user_index = user_account_all.index(userInfo[1]) + 1    # 索引值
    user_info = sheet.row_values(user_index)            # 使用者帳戶資訊
    user_balance = int(user_info[4])    # 帳戶餘額

    # 檢查輸入內容
    exchange_account = exchangeSys_normal_Win_mailText.get()    # 交換的帳號

    # 確保交換帳號存在
    if exchange_account == "":
        exchangeSys_normal_Win_mW.set("❕ 此欄不得為空")
        account_accept = False
    else:
        if exchange_account == userInfo[1]:
            exchangeSys_normal_Win_mW.set("❕ 不得和自己交換")
            account_accept = False
        else:
            if exchange_account in user_account_all:
                exchangeSys_normal_Win_mW.set("")
                exchange_index = user_account_all.index(exchange_account) + 1    # 交換帳號的索引值
                account_accept = True
            else:
                exchangeSys_normal_Win_mW.set('❕ 帳號不存在')
                account_accept = False
    
    exchange_amount = exchangeSys_normal_Win_quantityText.get()      # 交換數量
    # 確保交換數量為數字
    if exchange_amount == "":
        exchangeSys_normal_Win_qW.set("❕ 此欄不得為空")
        amount_accepted = False
    else:
        try:
            int(exchange_amount)
        except:
            exchangeSys_normal_Win_qW.set("❕ 請輸入正整數")
            amount_accepted = False
        else:
            exchangeSys_normal_Win_qW.set("")
            exchange_amount = int(exchange_amount)
            
            # 確保交換數量為正
            if exchange_amount > 0:
                exchangeSys_normal_Win_qW.set('')
                amount_accepted = True
                # 確保剩餘硬幣足夠
                if user_balance < exchange_amount:
                    exchangeSys_normal_Win_qW.set('❕ 剩餘硬幣不足')
                    amount_accepted = False
                else:
                    exchangeSys_normal_Win_qW.set('')
                    amount_accepted = True
            else:
                exchangeSys_normal_Win_qW.set('❕ 交易數量需為正')
                amount_accepted = False

    exchange_password = exchangeSys_normal_Win_passwordText.get()    # 交易密碼
    # 確保密碼正確
    if exchange_password == str(user_info[5]):
        exchangeSys_normal_Win_pW.set("")
        password_accepted = True
    else:
        if exchange_password == "":
            exchangeSys_normal_Win_pW.set("❕ 此欄不得為空")
            password_accepted = False
        else:
            exchangeSys_normal_Win_pW.set("❕ 交易密碼錯誤")
            password_accepted = False

    # 輸入內容檢查通過
    if account_accept and amount_accepted and password_accepted:
        exchangeSys_whetherExchange()


def exchangeSys_whetherExchange():
    """確認使用者是否要交易"""
    global exchangeSys_whetherExchangeWin
    exchangeSys_whetherExchangeWin = tk.Frame(exchangeSys_normal_Win)
    exchangeSys_whetherExchangeWin.config(width = 600, height = 300, bg = "#99B2DD")
    exchangeSys_whetherExchangeWin.place(anchor = "center", x = 512, y = 350)

    exchangeSys_whetherExchangeText = tk.Label(exchangeSys_whetherExchangeWin)
    exchangeSys_whetherExchangeText.config(text = "您確定要交換嗎？\n", font = "微軟正黑體 38 bold", bg = "#99B2DD")
    exchangeSys_whetherExchangeText.config(width = 16, height = 8)
    exchangeSys_whetherExchangeText.place(anchor = "center", x= 300, y = 120)

    # YES鍵
    yesBtn = tk.Button(exchangeSys_whetherExchangeWin, text = "YES")
    yesBtn.config(font = "微軟正黑體 30 bold", bg = "#F3BB91", fg = "red", activebackground = "yellow")
    yesBtn.config(relief = "flat")
    yesBtn.config(command = exchangeSys_runExchange, cursor = "hand2")
    yesBtn.place(anchor = "center", x = 200, y = 200)
    
    # NO鍵
    noBtn = tk.Button(exchangeSys_whetherExchangeWin, text = "NO")
    noBtn.config(font = "微軟正黑體 30 bold", bg = "#F3BB91", fg = "blue", activebackground = "yellow")
    noBtn.config(relief = "flat")
    noBtn.config(command = exchangeSys_whetherExchangeWin.destroy, cursor = "hand2")
    noBtn.place(anchor = "center", x = 390, y = 200)

    exchangeSys_whetherExchangeWin.place(anchor = "center", x = 512, y = 345)


def exchangeSys_runExchange():
    """執行交換"""
    scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("NTU Coin-0555c96087e3.json", scope)
    client = gspread.authorize(creds)
    sheet = client.open("NTU Coin").get_worksheet(0)  # Open the spreadhseet

    # 抓取使用者帳戶資訊
    user_account_all = sheet.col_values(2)            # 大家的帳號(Email)
    user_index = user_account_all.index(userInfo[1]) + 1    # 索引值
    user_info = sheet.row_values(user_index)            # 使用者帳戶資訊
    user_balance = int(user_info[4])    # 帳戶餘額
    exchange_account = exchangeSys_normal_Win_mailText.get()    # 交換的帳號
    exchange_index = user_account_all.index(exchange_account) + 1   # 交換帳號index
    exchange_amount = int(exchangeSys_normal_Win_quantityText.get())      # 交換數量
    exchange_password = exchangeSys_normal_Win_passwordText.get()    # 交易密碼
    exchange_info = sheet.row_values(exchange_index)    # 交換帳號帳戶資訊
    exchange_balance = int(exchange_info[4])    # 交換帳號餘額
    exchange_time = datetime.datetime.strftime(datetime.datetime.now(),'%Y-%m-%d %H:%M:%S')  # 交換時間
    exchange_description = exchangeSys_normal_Win_remarkText.get()

    # 更新資訊
    user_balance -= exchange_amount # 扣掉交易數量
    exchange_balance += exchange_amount # 加上交易數量
    sheet.update_cell(userInfo[0], 5, user_balance)
    sheet.update_cell(exchange_index, 5, exchange_balance)

    # 製造明細
    exchangeSys_normal_exchangeDatailWin = tk.Frame(exchangeSys_normal_Win)
    exchangeSys_normal_exchangeDatailWin.config(width = 1024, height = 699, bg = "#363636")
    exchangeSys_normal_exchangeDatailWin.place(x = 0, y = 0)

    # 明細標題
    title = tk.Label(exchangeSys_normal_exchangeDatailWin, text = "交易明細")
    title.config(font = "微軟正黑體 48 bold", bg = "#363636", fg = "white")
    title.place(anchor = "center", x = 512, y = 60)

    # 明細內容
    content = '交換帳號： ' + exchange_account
    lab_account = tk.Label(exchangeSys_normal_exchangeDatailWin, text = content)   # 交換帳號
    lab_account.config(bg = "#363636", fg = "white", font = "微軟正黑體 28 bold")
    lab_account.place(anchor = "w", x = 220, y = 180)

    content = '交換數量： ' + str(exchange_amount)
    lab_amount = tk.Label(exchangeSys_normal_exchangeDatailWin, text=content)    # 交換數量
    lab_amount.config(bg = "#363636", fg = "white", font = "微軟正黑體 28 bold")
    lab_amount.place(anchor = "w", x = 220, y = 280)

    content = '帳戶餘額： ' + str(user_balance)
    lab_balance = tk.Label(exchangeSys_normal_exchangeDatailWin, text=content)   # 帳戶餘額
    lab_balance.config(bg = "#363636", fg = "white", font = "微軟正黑體 28 bold")
    lab_balance.place(anchor = "w", x = 220, y = 380)

    content = '備註： ' + exchange_description
    lab_time = tk.Label(exchangeSys_normal_exchangeDatailWin, text=content)      # 備註
    lab_time.config(bg = "#363636", fg = "white", font = "微軟正黑體 28 bold")
    lab_time.place(anchor = "w", x = 220, y = 480)

    content = '交換時間： ' + exchange_time
    lab_time = tk.Label(exchangeSys_normal_exchangeDatailWin, text=content)      # 交換數量
    lab_time.config(bg = "#363636", fg = "white", font = "微軟正黑體 28 bold")
    lab_time.place(anchor = "w", x = 220, y = 580)

    # 離開鍵
    exitBtn = tk.Button(exchangeSys_normal_exchangeDatailWin, text = "回到首頁\nHome")
    exitBtn.config(font = "微軟正黑體 15 bold", bg = "#363636", fg = "white", relief = "flat")
    exitBtn.config(activebackground = "#363636", activeforeground = "#DF2935")
    exitBtn.config(command = exchangeSysWin.destroy, cursor = "hand2")
    exitBtn.place(anchor = "se",x=1024, y=699)

    """上傳紀錄"""
    exchange_record_sheet = client.open("NTU Coin").get_worksheet(2)    # 交換記錄表單
    num_rows = len(exchange_record_sheet.col_values(1))    # 欄位目前長度
    row1 = [num_rows + 1, 'norm-', userInfo[1], exchange_account, -exchange_amount, user_balance, exchange_time, exchange_description]
    row2 = [num_rows + 2, 'norm+', exchange_account, userInfo[1], exchange_amount, exchange_balance, exchange_time, exchange_description]
    insert_rows = [row1, row2]
    exchange_record_sheet.append_rows(insert_rows)    # 新增紀錄


def taskSys():
    """任務系統"""
    # 背景頁建立
    global taskSysWin
    taskSysWin = tk.Frame(homeWin)
    taskSysWin.config(width = 1024, height = 699, bg = "#363636")
    taskSysWin.place(x = 0, y = 0)

    # 返回鍵建立
    backBtn = tk.Button(taskSysWin, text = "回到首頁\nBack")
    backBtn.config(font = "微軟正黑體 15 bold", bg = "#363636", fg = "white", relief = "flat")
    backBtn.config(activebackground = "#363636", activeforeground = "#DF2935")
    backBtn.config(command = taskSysWin.destroy, cursor = "hand2")
    backBtn.place(anchor = "se",x=1024, y=699)

    # 標題
    title = tk.Label(taskSysWin, text = "任務系統")
    title.config(font = "微軟正黑體 48 bold", bg = "#363636", fg = "white")
    title.place(anchor = "center", x = 512, y = 60)

    # 發佈任務
    global Img_taskSys_releaseTask
    Img_taskSys_releaseTask = tk.PhotoImage(file = "發佈任務.png")
    releaseTask_Btn = tk.Button(taskSysWin)
    releaseTask_Btn.config(image = Img_taskSys_releaseTask, width = 790, height = 140)
    releaseTask_Btn.config(relief = "flat", cursor = "hand2", command = taskSys_releaseTask)
    releaseTask_Btn.place(anchor = "center", x = 512, y = 250)

    # 應徵任務
    global Img_taskSys_applyTask
    Img_taskSys_applyTask = tk.PhotoImage(file = "應徵任務.png")
    applyTask_Btn = tk.Button(taskSysWin)
    applyTask_Btn.config(image = Img_taskSys_applyTask, width = 790, height = 140)
    applyTask_Btn.config(relief = "flat", cursor = "hand2", command = taskSys_searchTask)
    applyTask_Btn.place(anchor = "center", x = 512, y = 440)


def taskSys_releaseTask():
    """發布任務介面"""
    # 背景頁建立
    taskSys_releaseTask_Win = tk.Frame(taskSysWin)
    taskSys_releaseTask_Win.config(width = 1024, height = 699, bg = "#363636")
    taskSys_releaseTask_Win.place(x = 0, y = 0)

    # 返回鍵建立
    backBtn = tk.Button(taskSys_releaseTask_Win, text = "回到上頁\nBack")
    backBtn.config(font = "微軟正黑體 15 bold", bg = "#363636", fg = "white", relief = "flat")
    backBtn.config(activebackground = "#363636", activeforeground = "#DF2935")
    backBtn.config(command = taskSys_releaseTask_Win.destroy, cursor = "hand2")
    backBtn.place(anchor = "se",x=1024, y=699)

    # 標題
    title = tk.Label(taskSys_releaseTask_Win, text = "發佈任務")
    title.config(font = "微軟正黑體 48 bold", bg = "#363636", fg = "white")
    title.place(anchor = "center", x = 512, y = 60)

    # 任務名稱
    taskTitle = tk.Label(taskSys_releaseTask_Win, text = "任務名稱（限10個中文字內）")
    taskTitle.config(font = "微軟正黑體 14 bold", bg = "#363636", fg = "white")
    taskTitle.place(anchor = "w", x = 300, y = 180)

    global taskSys_releaseTask_Win_nameText
    name = tk.Entry(taskSys_releaseTask_Win)
    taskSys_releaseTask_Win_nameText = tk.StringVar()
    name.config(textvariable = taskSys_releaseTask_Win_nameText, width = 38, font = "arial 14")
    name.place(anchor = "w", x = 300, y = 210)

    # 任務內容
    contentTitle = tk.Label(taskSys_releaseTask_Win, text = "任務內容")
    contentTitle.config(font = "微軟正黑體 14 bold", bg = "#363636", fg = "white")
    contentTitle.place(anchor = "w", x = 300, y = 260)

    global taskSys_releaseTask_Win_contentText
    content = tk.Entry(taskSys_releaseTask_Win)
    taskSys_releaseTask_Win_contentText = tk.StringVar()
    content.config(textvariable = taskSys_releaseTask_Win_contentText, width = 38, font = "arial 14")
    content.place(anchor = "w", x = 300, y = 290)

    # 任務報酬
    paymentTitle = tk.Label(taskSys_releaseTask_Win, text = "任務報酬")
    paymentTitle.config(font = "微軟正黑體 14 bold", bg = "#363636",  fg= "white")
    paymentTitle.place(anchor = "w", x = 300, y = 340)

    global taskSys_releaseTask_Win_paymentText
    payment = tk.Entry(taskSys_releaseTask_Win)
    taskSys_releaseTask_Win_paymentText = tk.StringVar()
    payment.config(textvariable = taskSys_releaseTask_Win_paymentText, width = 38, font = "arial 14")
    payment.place(anchor = "w", x = 300, y = 370)

    # 確認鍵
    global taskSys_releaseTask_Win_submitImg
    taskSys_releaseTask_Win_submitImg = tk.PhotoImage(file = "確認.png")
    taskSys_releaseTask_Win_sureBtn = tk.Button(taskSys_releaseTask_Win)
    taskSys_releaseTask_Win_sureBtn.config(image = taskSys_releaseTask_Win_submitImg, relief = "flat", width = 450, height = 36)
    taskSys_releaseTask_Win_sureBtn.config(cursor = "hand2")
    taskSys_releaseTask_Win_sureBtn.place(anchor = "center", x = 512, y = 460)


def taskSys_searchTask():
    """應徵任務介面"""
    # 背景頁建立
    global taskSys_searchTask_Win
    taskSys_searchTask_Win = tk.Frame(taskSysWin)
    taskSys_searchTask_Win.config(width = 1024, height = 699, bg = "#363636")
    taskSys_searchTask_Win.place(x = 0, y = 0)

    # 返回鍵建立
    backBtn = tk.Button(taskSys_searchTask_Win, text = "回到上頁\nBack")
    backBtn.config(font = "微軟正黑體 15 bold", bg = "#363636", fg = "white", relief = "flat")
    backBtn.config(activebackground = "#363636", activeforeground = "#DF2935")
    backBtn.config(command = taskSys_searchTask_Win.destroy, cursor = "hand2")
    backBtn.place(anchor = "se",x=1024, y=699)

    # 標題
    title = tk.Label(taskSys_searchTask_Win, text = "應徵任務")
    title.config(font = "微軟正黑體 48 bold", bg = "#363636", fg = "white")
    title.place(anchor = "center", x = 512, y = 60)

    # 任務總覽
    global Img_taskSys_searchTask_overview
    Img_taskSys_searchTask_overview = tk.PhotoImage(file = "任務總覽.png")
    overview_Btn = tk.Button(taskSys_searchTask_Win)
    overview_Btn.config(image = Img_taskSys_searchTask_overview, width = 790, height = 140)
    overview_Btn.config(relief = "flat", cursor = "hand2", command = taskSys_searchTask_taskOverview)
    overview_Btn.place(anchor = "center", x = 512, y = 250)

    # 查看現有任務
    global Img_taskSys_searchTask_currentTasks
    Img_taskSys_searchTask_currentTasks = tk.PhotoImage(file = "查看現有任務.png")
    currentTasks_Btn = tk.Button(taskSys_searchTask_Win)
    currentTasks_Btn.config(image = Img_taskSys_searchTask_currentTasks, width = 790, height = 140)
    currentTasks_Btn.config(relief = "flat", cursor = "hand2", command = taskSys_searchTask_taskOngoing)
    currentTasks_Btn.place(anchor = "center", x = 512, y = 440)


def taskSys_searchTask_taskOverview():
    """任務總覽介面"""
    # 背景頁建立
    global taskSys_searchTask_taskOverview_Win
    taskSys_searchTask_taskOverview_Win = tk.Frame(taskSys_searchTask_Win)
    taskSys_searchTask_taskOverview_Win.config(width = 1024, height = 699, bg = "#363636")
    taskSys_searchTask_taskOverview_Win.place(x = 0, y = 0)

    # 返回鍵建立
    backBtn = tk.Button(taskSys_searchTask_taskOverview_Win, text = "回到上頁\nBack")
    backBtn.config(font = "微軟正黑體 15 bold", bg = "#363636", fg = "white", relief = "flat")
    backBtn.config(activebackground = "#363636", activeforeground = "#DF2935")
    backBtn.config(command = taskSys_searchTask_taskOverview_Win.destroy, cursor = "hand2")
    backBtn.place(anchor = "se",x=1024, y=699)

    # 標題
    title = tk.Label(taskSys_searchTask_taskOverview_Win, text = "任務總覽")
    title.config(font = "微軟正黑體 48 bold", bg = "#363636", fg = "white")
    title.place(anchor = "center", x = 512, y = 60)

    # 內容顯示框
    global taskSys_searchTask_taskOverviewSection
    taskSys_searchTask_taskOverviewSection = tk.Frame(taskSys_searchTask_taskOverview_Win)
    taskSys_searchTask_taskOverviewSection.config(width = 800, height = 350, bg = "#363636")
    taskSys_searchTask_taskOverviewSection.place(anchor = "n", x= 512,  y = 130)

    # y軸scrollbar
    global taskOverview_Bar
    taskOverview_Bar = tk.Scrollbar(taskSys_searchTask_taskOverviewSection)
    taskOverview_Bar.pack(side = tk.RIGHT, fill = tk.Y)

    # 放入信息
    global taskOverview_listbox
    taskOverview_listbox = tk.Listbox(taskSys_searchTask_taskOverviewSection, yscrollcommand = taskOverview_Bar.set)
    taskOverview_listbox.config(font = "FangSong 20 bold", width = 48, height =18, bg = "#5C5C5C", fg = "white")
    taskOverview_listbox.config(activestyle = "none", cursor = "hand2")

    #先加入header
    header = tk.Label(taskSys_searchTask_taskOverview_Win)
    tplt_header = "{0:<8}      {1:{3}^10}    {2:>10}"
    header.config(text = tplt_header.format("No.", "任務名稱","$", chr(12288)), bg = "#363636")
    header.config(font = "FangSong 20 bold", fg = "white")
    header.place(anchor = "n", x = 502, y = 95)

    # 再加入用戶記錄
    global taskSys_searchTask_taskOverview_ls
    taskSys_searchTask_taskOverview_ls = [["1", "跑腿", "20"], ["2", "幫搶課", "100"], ["3", "徵求高鐵票", "500"], ["4", "徵求水源單人房", "10000"], ["5", "徵求人陪吃飯嗚嗚嗚", "200"], ["6", "托福家教", "10000"], ["7", "醬油膏", "1"], ["8", "睡", "500"], ["9", "徵求人類幫忙簽到民概", "200"]]
    tplt = "{0:<8}      {1:{3}^10}    {2:>10}"
    for i, content in enumerate(taskSys_searchTask_taskOverview_ls):
        taskOverview_listbox.insert("end", tplt.format(content[0], content[1], content[2], chr(12288)))
    taskOverview_listbox.pack(side = tk.LEFT, fill = tk.BOTH)
    taskOverview_Bar.config(command = taskOverview_listbox.yview)

    # 查看任務詳細資訊
    taskOverview_listbox.bind('<Double-Button-1>', lambda event, x = "all": taskSys_showTaskDetails(event, x))

    # 雙擊查看更多信息
    dbclick = tk.Label(taskSys_searchTask_taskOverview_Win, text = "（雙擊可查看更多信息）")
    dbclick.config(bg = "#363636", fg = "white", font = "FangSong 16 bold")
    dbclick.place(anchor = "center", x = 512, y = 660)


def taskSys_searchTask_taskOngoing():
    """任務總覽介面"""
    # 背景頁建立
    global taskSys_searchTask_taskOngoing_Win
    taskSys_searchTask_taskOngoing_Win = tk.Frame(taskSys_searchTask_Win)
    taskSys_searchTask_taskOngoing_Win.config(width = 1024, height = 699, bg = "#363636")
    taskSys_searchTask_taskOngoing_Win.place(x = 0, y = 0)

    # 返回鍵建立
    backBtn = tk.Button(taskSys_searchTask_taskOngoing_Win, text = "回到上頁\nBack")
    backBtn.config(font = "微軟正黑體 15 bold", bg = "#363636", fg = "white", relief = "flat")
    backBtn.config(activebackground = "#363636", activeforeground = "#DF2935")
    backBtn.config(command = taskSys_searchTask_taskOngoing_Win.destroy, cursor = "hand2")
    backBtn.place(anchor = "se",x=1024, y=699)

    # 標題
    title = tk.Label(taskSys_searchTask_taskOngoing_Win, text = "現有任務")
    title.config(font = "微軟正黑體 48 bold", bg = "#363636", fg = "white")
    title.place(anchor = "center", x = 512, y = 60)

    # 內容顯示框
    global taskSys_searchTask_taskOngoingSection
    taskSys_searchTask_taskOngoingSection = tk.Frame(taskSys_searchTask_taskOngoing_Win)
    taskSys_searchTask_taskOngoingSection.config(width = 800, height = 350, bg = "#363636")
    taskSys_searchTask_taskOngoingSection.place(anchor = "n", x= 512,  y = 130)

    # y軸scrollbar
    global taskOngoing_Bar
    taskOngoing_Bar = tk.Scrollbar(taskSys_searchTask_taskOngoingSection)
    taskOngoing_Bar.pack(side = tk.RIGHT, fill = tk.Y)

    # 放入信息
    global taskOngoing_listbox
    taskOngoing_listbox = tk.Listbox(taskSys_searchTask_taskOngoingSection, yscrollcommand = taskOngoing_Bar.set)
    taskOngoing_listbox.config(font = "FangSong 20 bold", width = 48, height =18, bg = "#5C5C5C", fg = "white")
    taskOngoing_listbox.config(activestyle = "none", cursor = "hand2")

    #先加入header
    header = tk.Label(taskSys_searchTask_taskOngoing_Win)
    tplt_header = "{0:<8}      {1:{3}^10}    {2:>10}"
    header.config(text = tplt_header.format("No.", "任務名稱","$", chr(12288)), bg = "#363636")
    header.config(font = "FangSong 20 bold", fg = "white")
    header.place(anchor = "n", x = 502, y = 95)

    # 再加入用戶記錄
    global taskSys_searchTask_taskOngoing_ls
    taskSys_searchTask_taskOngoing_ls = [["1", "跑腿", "20"], ["2", "幫搶課", "100"], ["3", "徵求高鐵票", "500"], ["4", "徵求水源單人房", "10000"], ["5", "徵求人陪吃飯嗚嗚嗚", "200"], ["6", "托福家教", "10000"], ["7", "醬油膏", "1"], ["8", "睡", "500"], ["9", "徵求人類幫忙簽到民概", "200"]]
    tplt = "{0:<8}      {1:{3}^10}    {2:>10}"
    for i, content in enumerate(taskSys_searchTask_taskOngoing_ls):
        taskOngoing_listbox.insert("end", tplt.format(content[0], content[1], content[2], chr(12288)))
    taskOngoing_listbox.pack(side = tk.LEFT, fill = tk.BOTH)
    taskOngoing_Bar.config(command = taskOngoing_listbox.yview)

    # 查看任務詳細資訊
    taskOngoing_listbox.bind('<Double-Button-1>', lambda event, x = "ongoing": taskSys_showTaskDetails(event, x))

    # 雙擊查看更多信息
    dbclick = tk.Label(taskSys_searchTask_taskOngoing_Win, text = "（雙擊可查看更多信息）")
    dbclick.config(bg = "#363636", fg = "white", font = "FangSong 16 bold")
    dbclick.place(anchor = "center", x = 512, y = 660)


def taskSys_showTaskDetails(event, mode):
    if mode == "all":
        selectedTaskIndex = taskOverview_listbox.get(taskOverview_listbox.curselection())[0]
        ls = [selectedTaskIndex, "跑腿", "我這邊有一隻豬，徵求人幫我把它搬運到新體我這邊有一隻豬，徵求人幫我把它搬運到新體我這邊有一隻豬，徵求人幫我把它搬運到新體我這邊有一隻豬，徵求人幫我把它搬運到新體我這邊有一隻豬，徵求人幫我把它搬運到新體我這邊有一隻豬，徵求人幫我把它搬運到新體","20"]
        taskSys_showTaskDetailsWin = tk.Frame()
        # 背景頁建立
        taskSys_showTaskDetailsWin = tk.Frame(taskSys_searchTask_taskOverview_Win)
        taskSys_showTaskDetailsWin.config(width = 1024, height = 699, bg = "#363636")
        taskSys_showTaskDetailsWin.place(x = 0, y = 0)
    elif mode == "ongoing":
        selectedTaskIndex = taskOngoing_listbox.get(taskOngoing_listbox.curselection())[0]
        ls = [selectedTaskIndex, "跑腿", "我這邊有一隻豬，徵求人幫我把它搬運到新體","100"]
        taskSys_showTaskDetailsWin = tk.Frame()
        # 背景頁建立
        taskSys_showTaskDetailsWin = tk.Frame(taskSys_searchTask_taskOngoing_Win)
        taskSys_showTaskDetailsWin.config(width = 1024, height = 699, bg = "#363636")
        taskSys_showTaskDetailsWin.place(x = 0, y = 0)

    # 返回鍵建立
    # backBtn = tk.Button(taskSys_showTaskDetailsWin, text = "回到上頁\nBack")
    # backBtn.config(font = "微軟正黑體 15 bold", bg = "#363636", fg = "white", relief = "flat")
    # backBtn.config(activebackground = "#363636", activeforeground = "#DF2935")
    # backBtn.config(command = taskSys_showTaskDetailsWin.destroy, cursor = "hand2")
    # backBtn.place(anchor = "se",x=1024, y=699)

    # 標題
    title = tk.Label(taskSys_showTaskDetailsWin, text = "任務 No.{}".format(selectedTaskIndex))
    title.config(font = "微軟正黑體 48 bold", bg = "#363636", fg = "white")
    title.place(anchor = "center", x = 512, y = 60)

    # 任務細節
    datail = tk.Label(taskSys_showTaskDetailsWin)
    content = textwrap.wrap(ls[2], 20)
    text = "任務名稱：{}\n\n任務內容：\n".format(ls[1])
    for sentence in content:
        text += sentence
        text += "\n"
    text += "\n任務報酬：{}".format(ls[3])
    datail.config(text = text, font = "微軟正黑體 22 bold", bg = "#363636", fg = "white")
    datail.place(anchor = "n", x = 512, y = 200)

    # 接受按鍵
    global Img_taskSys_showTaskDetails_accept
    Img_taskSys_showTaskDetails_accept = tk.PhotoImage(file = "接受.png")
    acceptBtn = tk.Button(taskSys_showTaskDetailsWin)
    acceptBtn.config(image = Img_taskSys_showTaskDetails_accept, width = 72, height = 32)
    acceptBtn.config(relief = "flat", cursor = "hand2", command = taskSys_showTaskDetailsWin.destroy)
    acceptBtn.place(anchor = "center", x = 400, y = 150)

    # 拒絕按鍵
    global Img_taskSys_showTaskDetails_reject
    Img_taskSys_showTaskDetails_reject = tk.PhotoImage(file = "拒絕.png")
    rejectBtn = tk.Button(taskSys_showTaskDetailsWin)
    rejectBtn.config(image = Img_taskSys_showTaskDetails_reject, width = 72, height = 32)
    rejectBtn.config(relief = "flat", cursor = "hand2", command = taskSys_showTaskDetailsWin.destroy)
    rejectBtn.place(anchor = "center", x = 624, y = 150)


def valueSys():
    """儲值系統"""
    # 背景頁建立
    global valueSysWin
    valueSysWin = tk.Frame(homeWin)
    valueSysWin.config(width = 1024, height = 699, bg = "#363636")
    valueSysWin.place(x = 0, y = 0)

    # 返回鍵建立
    backBtn = tk.Button(valueSysWin, text = "回到首頁\nBack")
    backBtn.config(font = "微軟正黑體 15 bold", bg = "#363636", fg = "white", relief = "flat")
    backBtn.config(activebackground = "#363636", activeforeground = "#DF2935")
    backBtn.config(command = valueSysWin.destroy, cursor = "hand2")
    backBtn.place(anchor = "se",x=1024, y=699)

    # 標題
    title = tk.Label(valueSysWin, text = "儲值系統")
    title.config(font = "微軟正黑體 48 bold", bg = "#363636", fg = "white")
    title.place(anchor = "center", x = 512, y = 60)

    # 儲值NTU Coin
    global Img_valueSys_addValue
    Img_valueSys_addValue = tk.PhotoImage(file = "儲值NTUCoin.png")
    addVauleBtn = tk.Button(valueSysWin)
    addVauleBtn.config(image = Img_valueSys_addValue, width = 790, height = 140)
    addVauleBtn.config(relief = "flat", cursor = "hand2", command = valueSys_moneyEntry_money2coin)
    addVauleBtn.place(anchor = "center", x = 512, y = 250)

    # 兌換成錢
    global Img_valueSys_exchange
    Img_valueSys_exchange = tk.PhotoImage(file = "兌換成錢.png")
    exchangeBtn = tk.Button(valueSysWin)
    exchangeBtn.config(image = Img_valueSys_exchange, width = 790, height = 140)
    exchangeBtn.config(relief = "flat", cursor = "hand2", command = valueSys_moneyEntry_coin2money)
    exchangeBtn.place(anchor = "center", x = 512, y = 440)

    # 顯示餘額
    balance = getBalance()
    balanceText = tk.Label(valueSysWin, text = "剩餘{}元".format(balance))
    balanceText.config(bg = "#363636", fg = "white", font = "微軟正黑體 30 bold")
    balanceText.place(anchor = "center", x = 512, y = 600)


def valueSys_moneyEntry_money2coin():
    """儲值系統_輸入金額"""
    # 背景頁建立
    moneyEntryWin_money2coin = tk.Frame(valueSysWin)
    moneyEntryWin_money2coin.config(width = 1024, height = 699, bg = "#363636")
    moneyEntryWin_money2coin.place(x = 0, y = 0)

    # 返回鍵建立
    backBtn = tk.Button(moneyEntryWin_money2coin, text = "回到上頁\nBack")
    backBtn.config(font = "微軟正黑體 15 bold", bg = "#363636", fg = "white", relief = "flat")
    backBtn.config(activebackground = "#363636", activeforeground = "#DF2935")
    backBtn.config(command = moneyEntryWin_money2coin.destroy, cursor = "hand2")
    backBtn.place(anchor = "se",x=1024, y=699)

    # 標題
    title = tk.Label(moneyEntryWin_money2coin, text = "儲值系統")
    title.config(font = "微軟正黑體 48 bold", bg = "#363636", fg = "white")
    title.place(anchor = "center", x = 512, y = 60)

    # 金額輸入
    money = tk.Label(moneyEntryWin_money2coin, text = "輸入金額")
    money.config(font = "微軟正黑體 30 bold", bg = "#363636", fg = "white")
    money.place(anchor = "center", x = 512, y = 290)

    global moneyEntry_money2coinText
    moneyEntry = tk.Entry(moneyEntryWin_money2coin)
    moneyEntry_money2coinText = tk.StringVar()
    moneyEntry.config(font = "arial 30", width = 20, textvariable = moneyEntry_money2coinText)
    moneyEntry.place(anchor = "center", x= 512, y = 350)

    # 確認鍵
    global sureImg
    sureImg = tk.PhotoImage(file = "確認.png")
    sureBtn = tk.Button(moneyEntryWin_money2coin)
    sureBtn.config(image = sureImg, relief = "flat", width = 450, height = 36)
    sureBtn.config(command = valueSys_moneyEntry_check_money2coin, cursor = "hand2")
    sureBtn.place(anchor = "center", x = 512, y = 430)

    # 錯誤信息
    global moneyEntryW_money2coin
    moneyEntryW_money2coin = tk.StringVar()
    moneyEntryW_money2coin.set("")
    moneyEntryWarning = tk.Label(moneyEntryWin_money2coin, textvariable = moneyEntryW_money2coin)
    moneyEntryWarning.config(font = "微軟正黑體 12", bg = "#363636", fg = "red")
    moneyEntryWarning.place(anchor = "center", x = 512, y = 393)


def valueSys_moneyEntry_coin2money():
    """儲值系統_輸入金額"""
    # 背景頁建立
    moneyEntryWin_coin2money = tk.Frame(valueSysWin)
    moneyEntryWin_coin2money.config(width = 1024, height = 699, bg = "#363636")
    moneyEntryWin_coin2money.place(x = 0, y = 0)

    # 返回鍵建立
    backBtn = tk.Button(moneyEntryWin_coin2money, text = "回到上頁\nBack")
    backBtn.config(font = "微軟正黑體 15 bold", bg = "#363636", fg = "white", relief = "flat")
    backBtn.config(activebackground = "#363636", activeforeground = "#DF2935")
    backBtn.config(command = moneyEntryWin_coin2money.destroy, cursor = "hand2")
    backBtn.place(anchor = "se",x=1024, y=699)

    # 標題
    title = tk.Label(moneyEntryWin_coin2money, text = "儲值系統")
    title.config(font = "微軟正黑體 48 bold", bg = "#363636", fg = "white")
    title.place(anchor = "center", x = 512, y = 60)

    # 金額輸入
    money = tk.Label(moneyEntryWin_coin2money, text = "輸入金額")
    money.config(font = "微軟正黑體 30 bold", bg = "#363636", fg = "white")
    money.place(anchor = "center", x = 512, y = 290)

    global moneyEntryText_coin2moneyText
    moneyEntryText_coin2money = tk.Entry(moneyEntryWin_coin2money)
    moneyEntryText_coin2moneyText = tk.StringVar()
    moneyEntryText_coin2money.config(font = "arial 30", width = 20, textvariable = moneyEntryText_coin2moneyText)
    moneyEntryText_coin2money.place(anchor = "center", x= 512, y = 350)

    # 確認鍵
    global sureImg
    sureImg = tk.PhotoImage(file = "確認.png")
    sureBtn = tk.Button(moneyEntryWin_coin2money)
    sureBtn.config(image = sureImg, relief = "flat", width = 450, height = 36)
    sureBtn.config(command = valueSys_moneyEntry_check_coin2money, cursor = "hand2")
    sureBtn.place(anchor = "center", x = 512, y = 430)

    # 錯誤信息
    global moneyEntryW_coin2money
    moneyEntryW_coin2money = tk.StringVar()
    moneyEntryW_coin2money.set("")
    moneyEntryWarning = tk.Label(moneyEntryWin_coin2money, textvariable = moneyEntryW_coin2money)
    moneyEntryWarning.config(font = "微軟正黑體 12", bg = "#363636", fg = "red")
    moneyEntryWarning.place(anchor = "center", x = 512, y = 393)


def valueSys_moneyEntry_check_money2coin():
    """確認輸入的數字為正整數"""
    data = eval(moneyEntry_money2coinText.get())
    left = data%1
    if left != 0:
        moneyEntryW_money2coin.set("❕ 請輸入正整數")
    else:
        if data > 0:
            valueSysWin.destroy()
        else:
            moneyEntryW_money2coin.set("❕ 請輸入正整數")


def valueSys_moneyEntry_check_coin2money():
    """確認輸入的數字為正整數"""
    balance = eval(getBalance())
    data = eval(moneyEntryText_coin2moneyText.get())
    left = data%1
    if left != 0:
        moneyEntryW_coin2money.set("❕ 請輸入正整數")
    else:
        if data > 0:
            if data > balance:
                moneyEntryW_coin2money.set("❕ 餘額不足")
            else:
                valueSysWin.destroy()
        else:
            moneyEntryW_coin2money.set("❕ 請輸入正整數")


def recordSys():
    """記錄系統"""
    # 背景頁建立
    recordSysWin = tk.Frame(homeWin)
    recordSysWin.config(width = 1024, height = 699, bg = "#363636")
    recordSysWin.place(x = 0, y = 0)

    # 返回鍵建立
    backBtn = tk.Button(recordSysWin, text = "回到首頁\nBack")
    backBtn.config(font = "微軟正黑體 15 bold", bg = "#363636", fg = "white", relief = "flat")
    backBtn.config(activebackground = "#363636", activeforeground = "#DF2935")
    backBtn.config(command = recordSysWin.destroy, cursor = "hand2")
    backBtn.place(anchor = "se",x=1024, y=699)

    # 標題
    title = tk.Label(recordSysWin, text = "記錄查詢")
    title.config(font = "微軟正黑體 48 bold", bg = "#363636", fg = "white")
    title.place(anchor = "center", x = 512, y = 60)

    # 時間選擇欄
    timeLabel1 = tk.Label(recordSysWin, text = "時間")
    timeLabel1.config(font = "微軟正黑體 20 bold", bg = "#363636", fg = "white")
    timeLabel1.place(anchor = "center", x = 150, y = 125)

    timeBox = ttk.Combobox(recordSysWin, font = "微軟正黑體 16 bold")
    timeBox["value"] = ("全部", "過去一週", "過去一月", "過去一年")
    timeBox.config(width = 12, justify = "center")
    timeBox["state"] = "readonly"
    timeBox.current(0)
    timeBox.place(anchor = "center", x = 150, y = 160)
    
    # 類別選擇欄
    classLabel1 = tk.Label(recordSysWin, text = "種類")
    classLabel1.config(font = "微軟正黑體 20 bold", bg = "#363636", fg = "white")
    classLabel1.place(anchor = "center", x = 375, y = 125)

    global recordSys_classBox
    recordSys_classBox = ttk.Combobox(recordSysWin, font = "微軟正黑體 16 bold")
    recordSys_classBox["value"] = ("全部", "貨幣交換", "儲值記錄", "任務記錄")
    recordSys_classBox.config(width = 12, justify = "center")
    recordSys_classBox["state"] = "readonly"
    recordSys_classBox.current(0)
    recordSys_classBox.bind("<<ComboboxSelected>>", recordSys_checkComboboxState)
    recordSys_classBox.place(anchor = "center", x = 375, y = 160)

    # 依據用戶名/內容關鍵字查詢
    typeLabel1 = tk.Label(recordSysWin, text = "依據")
    typeLabel1.config(font = "微軟正黑體 20 bold", bg = "#363636", fg = "white")
    typeLabel1.place(anchor = "center", x = 600, y = 125)

    global recordSys_typeBox
    recordSys_typeBox = ttk.Combobox(recordSysWin, font = "微軟正黑體 16 bold")
    recordSys_typeBox["value"] = ("-無-", "用戶名", "內容關鍵字")
    recordSys_typeBox.config(width = 12, justify = "center")
    recordSys_typeBox["state"] = "readonly"
    recordSys_typeBox.current(0)
    recordSys_typeBox.bind("<<ComboboxSelected>>", recordSys_checkEntryState)
    recordSys_typeBox.place(anchor = "center", x = 600, y = 160)

    # 關鍵字輸入
    keywordLabel1 = tk.Label(recordSysWin, text = "請輸入字詞")
    keywordLabel1.config(font = "微軟正黑體 20 bold", bg = "#363636", fg = "white")
    keywordLabel1.place(anchor = "center", x = 825, y = 125)

    global recordSys_keywordEntry
    global recordSys_keywordEntryText
    recordSys_keywordEntry = tk.Entry(recordSysWin)
    recordSys_keywordEntryText = tk.StringVar()
    recordSys_keywordEntry.config(textvariable = recordSys_keywordEntryText, bg = "#5C5C5C", fg = "white")
    recordSys_keywordEntry.config(font = "微軟正黑體 16 bold", width = 12, justify = "center", state = "disable")
    recordSys_keywordEntry.place(anchor = "center", x = 825, y = 160)

    # 查詢按鍵
    global searchImg
    searchBtn = tk.Button(recordSysWin)
    searchImg = tk.PhotoImage(file = "查詢.png")
    searchBtn.config(width = 72, height = 32, image = searchImg, relief = "flat", cursor = "hand2")
    searchBtn.config(command = recordSys_search)
    searchBtn.place(anchor = "center", x = 960, y = 160)

    # 收入支出選擇
    global recordSys_ckbtn_rev
    global recordSys_ckbtn_exp
    global recordSys_ckbtn_var
    recordSys_ckbtn_rev = tk.Radiobutton(recordSysWin)
    recordSys_ckbtn_var = tk.IntVar()
    recordSys_ckbtn_rev.config(text = "收入", font = "FangSong 16 bold", fg = "white", bg = "#363636")
    recordSys_ckbtn_rev.config(variable = recordSys_ckbtn_var, value = 0, state = "disable")
    recordSys_ckbtn_rev.config(activebackground = "#363636", activeforeground	= "white", selectcolor = "#5C5C5C")
    recordSys_ckbtn_rev.place(anchor = "e", x = 220, y = 250)

    recordSys_ckbtn_exp = tk.Radiobutton(recordSysWin)
    recordSys_ckbtn_exp.config(text = "支出", font = "FangSong 16 bold", fg = "white", bg = "#363636")
    recordSys_ckbtn_exp.config(variable = recordSys_ckbtn_var, value = 1, state = "disable")
    recordSys_ckbtn_exp.config(activebackground = "#363636", activeforeground	= "white", selectcolor = "#5C5C5C")
    recordSys_ckbtn_exp.place(anchor = "w", x = 220, y = 250)

    # 內容顯示框
    global recordSys_revenueSection
    recordSys_revenueSection = tk.Frame(recordSysWin)
    recordSys_revenueSection.config(width = 800, height = 350, bg = "#363636")
    recordSys_revenueSection.place(anchor = "n", x= 512,  y = 270)

    # y軸scrollbar
    global recordSys_revenueBar1
    recordSys_revenueBar1 = tk.Scrollbar(recordSys_revenueSection)
    recordSys_revenueBar1.pack(side = tk.RIGHT, fill = tk.Y)

    # 放入信息
    global recordSys_listbox
    recordSys_listbox = tk.Listbox(recordSys_revenueSection, yscrollcommand = recordSys_revenueBar1.set)
    recordSys_listbox.config(font = "FangSong 20 bold", width = 48, height =13, bg = "#5C5C5C", fg = "white")
    recordSys_listbox.config(selectbackground = "#5C5C5C", activestyle = "none")
    #先加入header
    header = ["日期", "用戶名稱", "內容", "金額"]
    tplt_header = "{0:{4}<3} {1:{4}^6} {2:{4}^10} {3:{4}>4}"
    recordSys_listbox.insert(0, tplt_header.format(header[0], header[1], header[2], header[3], chr(12288)))
    # 再加入用戶記錄
    global recordSys_record_ls
    # recordSys_record_ls = [["12/11", "daniel", "吃飯", "$1"], ["5/12", "l", "幫", "$100000"], ["12/13", "d", "幫", "$1"], ["12/13", "tallllDaniel", "幫道道道到到到道道道", "$100000"], ["5/12", "tallllDaniel", "幫", "$100000"], ["12/13", "dogg", "幫", "$10"], ["12/13", "dogg", "幫道道道到", "$10"], ["5/12", "tallllDaniel", "幫", "$100000"], ["12/13", "dogg", "幫", "$10"], ["12/13", "dogg", "幫道道道到", "$10"], ["5/12", "tallllDaniel", "幫", "$100000"], ["12/13", "dogg", "幫", "$10"], ["12/13", "dogg", "幫道道道到", "$10"]]
    recordSys_record_ls = [[" ", " ", chr(12288), " "]]*10
    tplt = "{0:<6}{1:^12} {2:{4}^10}{3:>8}"
    for i, content in enumerate(recordSys_record_ls):
        recordSys_listbox.insert(i + 1, tplt.format(content[0], content[1], content[2], content[3], chr(12288)))
    recordSys_listbox.pack(side = tk.LEFT, fill = tk.BOTH)
    recordSys_revenueBar1.config(command = recordSys_listbox.yview)
    

def crawler_userInfo():
    scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("NTU Coin-0555c96087e3.json", scope)
    client = gspread.authorize(creds)
    sheet = client.open("NTU Coin").get_worksheet(0)  # Open the spreadhseet
    data = sheet.get_all_records()
    ls = []
    for i in range(2, len(data)):
        info = sheet.row_values(i)
        ls.append("    ".join(info))
    return ls


def recordSys_checkComboboxState(event):
    """當選擇儲值記錄時disable依據...查詢"""
    if recordSys_classBox.get() == "儲值記錄":
        recordSys_typeBox.current(0)
        recordSys_typeBox["state"] = "disable"
        recordSys_keywordEntryText.set("")
        recordSys_keywordEntry.config(state = "disable")
    else:
        recordSys_typeBox["state"] = "readonly"
        if recordSys_typeBox.get() == "-無-":
            recordSys_keywordEntryText.set("")
            recordSys_keywordEntry.config(state = "disable")
        else:
            recordSys_keywordEntry.config(state = "normal")


def recordSys_checkEntryState(event):
    """當選擇-無-時disable輸入關鍵字的地方"""
    if recordSys_typeBox.get() == "-無-":
        recordSys_keywordEntryText.set("")
        recordSys_keywordEntry.config(state = "disable")
    else:
        recordSys_keywordEntry.config(state = "normal")


def recordSys_search():
    """顯示紀錄"""
    recordSys_ckbtn_rev.config(state = "normal")
    recordSys_ckbtn_exp.config(state = "normal")
    recordSys_ckbtn_var.set(0)
    recordSys_listbox.delete(1, "end")
    recordSys_record_ls = [["12/11", "daniel", "吃飯", "$1"], ["5/12", "l", "幫", "$100000"], ["12/13", "d", "幫", "$1"], ["12/13", "tallllDaniel", "幫道道道到到到道道道", "$100000"], ["5/12", "tallllDaniel", "幫", "$100000"], ["12/13", "dogg", "幫", "$10"], ["12/13", "dogg", "幫道道道到", "$10"], ["5/12", "tallllDaniel", "幫", "$100000"], ["12/13", "dogg", "幫", "$10"], ["12/13", "dogg", "幫道道道到", "$10"], ["5/12", "tallllDaniel", "幫", "$100000"], ["12/13", "dogg", "幫", "$10"], ["12/13", "dogg", "幫道道道到", "$10"]]
    tplt = "{0:<6}{1:^12} {2:{4}^10}{3:>8}"
    for i, content in enumerate(recordSys_record_ls):
        recordSys_listbox.insert(i + 1, tplt.format(content[0], content[1], content[2], content[3], chr(12288)))


def getBalance():
    scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("NTU Coin-0555c96087e3.json", scope)
    client = gspread.authorize(creds)
    sheet = client.open("NTU Coin").get_worksheet(0)  # Open the spreadhseet
    balance = sheet.row_values(userInfo[0])[4]
    return balance


# 方便pyinstaller將圖片攜帶
# picData = open('func1.png', 'wb')
# picData.write(base64.b64decode(func1))
# picData.close()
# picData = open('pageBackground.png', 'wb')
# picData.write(base64.b64decode(pageBackground))
# picData.close()

# 建立視窗
win = tk.Tk()
win.title("NTU Coin")
state = False
win.geometry("1024x699+172+0")
win.resizable(False, False)
win.config(bg = "#363636")
login()

# 下拉欄格式
text_font = ('微軟正黑體', '16', "bold")
win.option_add('*TCombobox*Listbox.font', text_font)
combostyle = ttk.Style()
combostyle.theme_create('combostyle', parent='alt',
                        settings={'TCombobox':
                                    {'configure':
                                        {
                                            'foreground': 'white',
                                            'selectbackground': '#5C5C5C',
                                            'fieldbackground': '#5C5C5C',
                                            'background': 'white'
                                        }}}
                        )
combostyle.theme_use('combostyle')

win.mainloop()
