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
import time
import tkinter.font
import tkinter.messagebox
import tkinter.scrolledtext
from PIL import Image, ImageTk
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
    client = getClient()
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
    client = getClient()
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
    exchange_special_Btn.config(relief = "flat", cursor = "hand2", command = exchangeSys_special)
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
    remarkTitle = tk.Label(exchangeSys_normal_Win, text = "備註（限10個中文字內）")
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

    # 檢查密碼確認欄
    global exchangeSys_normal_Win_rW
    exchangeSys_normal_Win_rW = tk.StringVar()
    exchangeSys_normal_Win_rW.set("")
    exchangeSys_normal_Win_remarkWarning = tk.Label(exchangeSys_normal_Win, textvariable = exchangeSys_normal_Win_rW)
    exchangeSys_normal_Win_remarkWarning.config(font = "微軟正黑體 10", bg = "#363636", fg = "red")
    exchangeSys_normal_Win_remarkWarning.place(anchor = "w", x = 300, y = 475)


def exchangeSys_normal_check():
    """確認輸入資訊正確"""
    client = getClient()
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

    exchange_remark = exchangeSys_normal_Win_remarkText.get()
    if is_all_chinese(exchange_remark):
        if len(exchange_remark) > 10:
            exchangeSys_normal_Win_rW.set("❕ 備註過長")
            remark_accepted = False
        else:
            remark_accepted = True
    else:
        exchangeSys_normal_Win_rW.set("❕ 備註不符合格式")
        remark_accepted = False

    # 輸入內容檢查通過
    if account_accept and amount_accepted and password_accepted and remark_accepted:
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
    client = getClient()
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


def exchangeSys_special():
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

            ttk.Style().configure('Treeview.Heading', background='#363636', foreground='white', font=self.f_lab)
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
                self.room_sheet.insert('', 'end', values=tmp, tags=('font', 'bg', 'fg'))
                self.room_sheet.tag_configure('font', font=self.f_con)
                self.room_sheet.tag_configure('bg', background='white')
                self.room_sheet.tag_configure('fg', foreground='#363636')
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
                self.password_entry = tk.Entry(self, show='●', font=self.f_lab)    # 讓使用者輸入房間密碼
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

                Special_exchange.set_bg_fg(self.widgets_list)    # 更改物件的文字顏色跟背景顏色
                Special_exchange.set_bg_fg_error(self.widgets_error_list)    # 更改錯誤訊息的文字顏色跟背景顏色

            # 檢查密碼
            def password_comfirm(self):
                # 密碼正確
                if self.password_entry.get() == self.room_password:
                    self.destroy()
                    self.sheet_of_room.append_row([self.user_account, self.user_name, 0, self.user_balance])    # 將使用者資料加入房間的表單
                    self.special_exchange_room.update_cell(self.room_index, 6, str(self.people + 1))    # 更新房間人數
                    Special_exchange.room_page(self.room_mode, self.room_name, self.room_number,
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
                self.room_mode1 = tk.Radiobutton(self, text='麻將', variable=self.radioValue, value=1, command=self.choose_mode, font=self.f_lab, activebackground = "#363636", activeforeground	= "white", selectcolor = "#5C5C5C")    # 房間模式-麻將
                self.room_mode2 = tk.Radiobutton(self, text='分錢', variable=self.radioValue, value=2, command=self.choose_mode, font=self.f_lab, activebackground = "#363636", activeforeground	= "white", selectcolor = "#5C5C5C")    # 房間模式-分錢
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
                self.check_box_password = tk.Checkbutton(self, text='設定密碼', variable=self.checkVar, command=self.set_password, font=self.f_lab, activebackground = "#363636", activeforeground	= "white", selectcolor = "#5C5C5C")    # 讓使用者選擇是否要設密碼
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

                Special_exchange.set_bg_fg(self.widgets_list)    # 更改物件的文字顏色跟背景顏色
                Special_exchange.set_bg_fg_error(self.widgets_error_list)    # 更改錯誤訊息的文字顏色跟背景顏色

            # 選擇房間模式
            def choose_mode(self):
                # 使願者選擇麻將模式
                if self.radioValue.get() == 1:
                    self.room_mode = '麻將'    # 房間模式
                    self.people_limit_entry = tk.Label(self, text=4, font=self.f_lab)       # 強制設定人數上限
                    self.people_limit_entry.grid(row=2, column=3, sticky=tk.SE + tk.NW)
                    Special_exchange.set_bg_fg([self.people_limit_entry])    # 更改物件的文字顏色跟背景顏色
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
                    Special_exchange.room_page(self.room_mode, self.room_name, self.room_number,
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
            room_page = Special_exchange.Room(room_mode, room_name, room_number, people_limit, user_account)
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
                        # 將房間成員帳戶名稱名單&分數表單調整順序
                        self.member_ordered = []           # 房間成員帳戶名稱名單(已排序)
                        self.point_ordered = []            # 房間成員分數表單(已排序)
                        self.user_row = self.sheet_of_room.find(self.user_account).row    # 使用者帳號位置
                        for i in range(self.user_row, self.user_row + 4):
                            if i > 7:
                                i -= 4
                            self.member_ordered.append(self.sheet_of_room.cell(i, 2).value)
                            self.point_ordered.append(self.sheet_of_room.cell(i, 3).value)
                        self.create_widgets_mj()        # 麻將介面

                    elif self.room_mode == '分錢':
                        self.create_widgets_share()     # 分錢介面

            # 設定麻將介面
            def create_widgets_mj(self):
                self.widgets_list = []     # 部件清單
                self.user_info_list = []   # 使用者資訊清單

                self.lab_blank1 = tk.Label(self)    #　空白部分
                self.lab_blank1.grid(row=0, column=0, rowspan=40, columnspan=34, sticky=tk.NW + tk.SE)
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

                for point in self.point_ordered:
                    # 還有分數未結算
                    if not str(point) == ('0' or ''):
                        self.command = self.cant_leave
                        break
                    # 分數皆為0
                    else:
                        self.command = self.leave_room
                self.butn_leave = tk.Button(self, text='離開房間', command=self.command, font=self.f_lab)        # 離開房間按鈕
                self.butn_leave.grid(row=1, column=33, sticky=tk.NW + tk.SE)
                self.widgets_list.append(self.butn_leave)    # 加入部件清單

                load = Image.open('麻將4.jpg')
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

                self.lab_amount_error = tk.Label(self, text='', font=self.f_lab)
                self.lab_amount_error.grid(row=39, column=17, sticky=tk.NW + tk.SE)
                Special_exchange.set_bg_fg_error([self.lab_amount_error])    # 更改錯誤提示的文字顏色跟背景顏色

                Special_exchange.set_bg_fg(self.widgets_list)    # 更改物件的文字顏色跟背景顏色
                Special_exchange.set_bg_fg_user(self.user_info_list)    # 更改使用者資訊的文字顏色跟背景顏色                

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
                        self.lab_amount_error.configure(text='請輸入數字')
                    else:
                        # 確認家換數量為正值
                        self.exchange_amount = int(self.exchange_amount)
                        if self.exchange_amount > 0:
                            amount_accepted = True
                        else:
                            amount_accepted = False
                            self.lab_amount_error.configure(text='輸入值須為正')

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
                            self.end(bankrupt=True)
                        # 足以支付
                        else:
                            self.sheet_of_room.update('C%d' % (self.exchange_user_row), str(self.update_exchange_user_point))
                            self.sheet_of_room.update('C%d' % (self.user_row), str(self.update_user_point))
                            self.refresh_room()    # 重整頁面

            # 結算
            def end(self , bankrupt=False):
                # 避免錯誤
                try:
                    self.sheet_of_room = NTU_Coin.worksheet('Room %s' % (self.room_number))
                # 房間已被關閉
                except Exception as error:
                    self.refresh_room()
                # 房間未被關閉
                else:
                    self.point_list = []    # 分數清單

                    self.end_time = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')  # 結算時間
                    # 更新使用者帳戶餘額
                    self.sheet_of_room = NTU_Coin.worksheet('Room %s' % (self.room_number))    # 該房間的表單
                    self.user_balance = self.sheet_of_room.acell('D%d' % (self.user_row)).value    # 使用者帳戶餘額
                    self.user_point = self.sheet_of_room.acell('C%d' % (self.user_row)).value      # 使用者分數
                    self.user_info_row = sheet.find(self.user_account).row    # 使用者資訊位置
                    self.update_user_balance = int(self.user_balance) + int(self.user_point)
                    sheet.update_cell(self.user_info_row, 5, str(self.update_user_balance))
                    self.point_list.append(self.user_point)    # 加入分數清單

                    # 更新其他使用者之帳戶餘額
                    self.user2_row = self.sheet_of_room.find(self.member_ordered[1]).row    # 使用者二帳號位置
                    self.user2_balance = self.sheet_of_room.acell('D%d' % (self.user2_row)).value    # 使用者二帳戶餘額
                    self.user2_point = self.sheet_of_room.acell('C%d' % (self.user2_row)).value      # 使用者二分數
                    self.user2_account = self.sheet_of_room.acell('A%d' % (self.user2_row)).value    # 使用者二帳號
                    self.user2_info_row = sheet.find(self.member_ordered[1]).row    # 使用者二資訊位置
                    self.update_user2_balance = int(self.user2_balance) + int(self.user2_point)
                    sheet.update_cell(self.user2_info_row, 5, str(self.update_user2_balance))
                    self.point_list.append(self.user2_point)    # 加入分數清單

                    self.user3_row = self.sheet_of_room.find(self.member_ordered[2]).row    # 使用者三帳號位置
                    self.user3_balance = self.sheet_of_room.acell('D%d' % (self.user3_row)).value    # 使用者三帳戶餘額
                    self.user3_point = self.sheet_of_room.acell('C%d' % (self.user3_row)).value      # 使用者三分數
                    self.user3_account = self.sheet_of_room.acell('A%d' % (self.user3_row)).value    # 使用者三帳號
                    self.user3_info_row = sheet.find(self.member_ordered[2]).row    # 使用者三資訊位置
                    self.update_user3_balance = int(self.user3_balance) + int(self.user3_point)
                    sheet.update_cell(self.user3_info_row, 5, str(self.update_user3_balance))
                    self.point_list.append(self.user3_point)    # 加入分數清單

                    self.user4_row = self.sheet_of_room.find(self.member_ordered[3]).row    # 使用者四帳號位置
                    self.user4_balance = self.sheet_of_room.acell('D%d' % (self.user4_row)).value    # 使用者四帳戶餘額
                    self.user4_point = self.sheet_of_room.acell('C%d' % (self.user4_row)).value      # 使用者四分數
                    self.user4_account = self.sheet_of_room.acell('A%d' % (self.user4_row)).value    # 使用者四帳號
                    self.user4_info_row = sheet.find(self.member_ordered[3]).row    # 使用者四資訊位置
                    self.update_user4_balance = int(self.user4_balance) + int(self.user4_point)
                    sheet.update_cell(self.user4_info_row, 5, str(self.update_user4_balance))
                    self.point_list.append(self.user4_point)    # 加入分數清單

                    self.upload_record()    # 上傳紀錄
                    # 未破產
                    if not bankrupt:
                        # 分數歸零
                        self.sheet_of_room.update('C%d' % (self.user_row), '0')
                        self.sheet_of_room.update('C%d' % (self.user2_row), '0')
                        self.sheet_of_room.update('C%d' % (self.user3_row), '0')
                        self.sheet_of_room.update('C%d' % (self.user4_row), '0')
                        tk.messagebox.showinfo(title='結算完畢', message='分數已歸零!')
                        self.refresh_room()
                    # 有使用者破產
                    else:
                        NTU_Coin.del_worksheet(self.sheet_of_room)    # 刪除該房間的表單
                        self.special_exchange_room.delete_rows(self.room.row)    # 刪除該房間的資訊
                        special_exchange_page(self)    # 導回特殊交換介面

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

                Special_exchange.set_bg_fg(self.widgets_list)    # 更改物件的文字顏色跟背景顏色

            # 重整房間頁面
            def refresh_room(self):
                self.destroy()
                Special_exchange.room_page(self.room_mode, self.room_name, self.room_number,
                                           self.people_limit, self.user_account)

            # 離開房間
            def leave_room(self):
                # 避免錯誤
                try:
                    self.sheet_of_room = NTU_Coin.worksheet('Room %s' % (self.room_number))
                # 房間已被關閉
                except Exception as error:
                    self.refresh_room()
                # 房間未被關閉
                else:
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

            # 還沒付錢，不能離開
            def cant_leave(self):
                tk.messagebox.showerror(title='無法離開房間', message='尚有餘款未結算')

            # 上傳紀錄
            def upload_record(self):
                self.exchange_record_sheet = NTU_Coin.get_worksheet(2)    # 交換記錄表單
                num_rows = len(self.exchange_record_sheet.col_values(1))
                # 依據輸/贏錢來決定紀錄樣式
                spec = []    # 樣式清單
                for point in self.point_list:
                    # 贏錢
                    if int(point) >= 0:
                        spec.append('spec+')
                    # 輸錢
                    else:
                        spec.append('spec-')

                row1 = [str(num_rows + 1), spec[0], self.user_account, '', self.user_point, self.user_balance, self.end_time, '麻將']
                row2 = [str(num_rows + 2), spec[1], self.user2_account, '', self.user2_point, self.user2_balance, self.end_time, '麻將']
                row3 = [str(num_rows + 3), spec[2], self.user3_account, '', self.user3_point, self.user3_balance, self.end_time, '麻將']
                row4 = [str(num_rows + 4), spec[3], self.user4_account, '', self.user4_point, self.user4_balance, self.end_time, '麻將']
                insert_rows = [row1, row2, row3, row4]
                self.exchange_record_sheet.append_rows(insert_rows)    # 新增紀錄


    # 進入交換主頁
    def exchange_homepage(window):
        window.destroy()    # 將原本的畫面刪除
        exchangeSys_special_Win.destroy()


    # 進入特殊交換系統
    def special_exchange_page(window):
        window.destroy()    # 將原本的畫面刪除
        spec_ex = Special_exchange()
        spec_ex.master.title("NTU Coin")
        spec_ex.master.geometry('1024x699')
        spec_ex.master.configure(bg='#363636')
        spec_ex.master.resizable(False, False)
        spec_ex.mainloop()



    client = getClient()
    NTU_Coin = client.open('NTU Coin')
    sheet = NTU_Coin.get_worksheet(0)  # Open the spreadhseet

    global exchangeSys_special_Win
    exchangeSys_special_Win = tk.Frame(exchangeSysWin)
    exchangeSys_special_Win.config(width = 1024, height = 699, bg = "#363636")
    exchangeSys_special_Win.place(x = 0, y = 0)

    account = userInfo[1]    # 使用者帳號(從登入資訊抓來)
    spec_system = Special_exchange()
    special_exchange_page(spec_system)


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
    contentTitle = tk.Label(taskSys_releaseTask_Win, text = "任務內容（限140個字元內）")
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
    taskSys_releaseTask_Win_sureBtn.config(cursor = "hand2", command = taskSys_releaseTaskCheck)
    taskSys_releaseTask_Win_sureBtn.place(anchor = "center", x = 512, y = 460)

    """錯誤信息欄"""
    # 檢查名稱欄
    global taskSys_releaseTask_Win_nameWarning
    taskSys_releaseTask_Win_nameWarning = tk.StringVar()
    taskSys_releaseTask_Win_nameWarning.set("")
    nameWarning = tk.Label(taskSys_releaseTask_Win, textvariable = taskSys_releaseTask_Win_nameWarning)
    nameWarning.config(font = "微軟正黑體 10", bg = "#363636", fg = "red")
    nameWarning.place(anchor = "w", x = 300, y = 235)

    # 檢查內容欄
    global taskSys_releaseTask_Win_contentWarning
    taskSys_releaseTask_Win_contentWarning = tk.StringVar()
    taskSys_releaseTask_Win_contentWarning.set("")
    contentWarning = tk.Label(taskSys_releaseTask_Win, textvariable = taskSys_releaseTask_Win_contentWarning)
    contentWarning.config(font = "微軟正黑體 10", bg = "#363636", fg = "red")
    contentWarning.place(anchor = "w", x = 300, y = 315)

    # 檢查報酬欄
    global taskSys_releaseTask_Win_paymentWarning
    taskSys_releaseTask_Win_paymentWarning = tk.StringVar()
    taskSys_releaseTask_Win_paymentWarning.set("")
    paymentWarning = tk.Label(taskSys_releaseTask_Win, textvariable = taskSys_releaseTask_Win_paymentWarning)
    paymentWarning.config(font = "微軟正黑體 10", bg = "#363636", fg = "red")
    paymentWarning.place(anchor = "w", x = 300, y = 395)


def taskSys_releaseTaskCheck():
    name = taskSys_releaseTask_Win_nameText.get()
    content = taskSys_releaseTask_Win_contentText.get()
    payment = taskSys_releaseTask_Win_paymentText.get()
    taskSys_releaseTask_Win_nameWarning.set("")
    rightName = False
    rightContent = False
    rightPayment = False

    # 檢查名稱
    if name == "":
        taskSys_releaseTask_Win_nameWarning.set("❕ 此欄不得為空")
    else:
        if len(name) > 10:
            taskSys_releaseTask_Win_nameWarning.set("❕ 名稱過長")
            rightName = False
        else:
            if is_all_chinese(name):
                taskSys_releaseTask_Win_nameWarning.set("")
                rightName = True
            else:
                taskSys_releaseTask_Win_nameWarning.set("❕ 名稱不符合格式")
                rightName = False

    # 檢查內容
    if content == "":
        taskSys_releaseTask_Win_contentWarning.set("❕ 此欄不得為空")
    else:
        if len(content) > 140:
            taskSys_releaseTask_Win_contentWarning.set("❕ 內容過長")
            rightContent = False
        else:
            taskSys_releaseTask_Win_contentWarning.set("")
            rightContent = True

    # 檢查報酬
    try:
        data = eval(payment)
        left = data%1
        if left != 0:
            taskSys_releaseTask_Win_paymentWarning.set("❕ 請輸入正整數")
            rightPayment = False
        else:
            if data > 0:
                taskSys_releaseTask_Win_paymentWarning.set("")
                rightPayment = True
            else:
                taskSys_releaseTask_Win_paymentWarning.set("❕ 請輸入正整數")
                rightPayment = False
    except:
        taskSys_releaseTask_Win_paymentWarning.set("❕ 請輸入正整數")
    
    if rightName and rightContent and rightPayment:
        taskSys_establish_mission(userInfo[1], name, content, payment)
        taskSysWin.destroy()


def taskSys_establish_mission(submitter_account, mission_name, mission_content, payment):
    client = getClient()
    sheet = client.open("NTU Coin").worksheet("Missions")
    sub_time_create = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
    mission_index = int(len(sheet.col_values(1)))+1
    status = "on-going"
    account = submitter_account
    lst = [mission_index, account, mission_name, mission_content, payment, status, sub_time_create, "N/A"]
    sheet.append_row(lst)


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
    taskSys_searchTask_taskOverview_ls = taskSys_get_all_tasks()
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
    taskSys_searchTask_taskOngoing_ls = taskSys_get_users_tasks()
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
    global taskSys_showTaskDetailsWin
    if mode == "all":
        data = taskOverview_listbox.get(taskOverview_listbox.curselection())
        index = re.findall(r"^[0-9]*", data)
        ls = taskSys_get_tasks_details(index[0])
        taskSys_showTaskDetailsWin = tk.Frame()

        # 背景頁建立
        taskSys_showTaskDetailsWin = tk.Frame(taskSys_searchTask_taskOverview_Win)
        taskSys_showTaskDetailsWin.config(width = 1024, height = 699, bg = "#363636")
        taskSys_showTaskDetailsWin.place(x = 0, y = 0)

        # 接受按鍵
        global Img_taskSys_showTaskDetails_accept
        Img_taskSys_showTaskDetails_accept = tk.PhotoImage(file = "接受.png")
        acceptBtn = tk.Button(taskSys_showTaskDetailsWin)
        acceptBtn.config(image = Img_taskSys_showTaskDetails_accept, width = 72, height = 32)
        acceptBtn.config(relief = "flat", cursor = "hand2", command =lambda x = index[0]: taskSys_accept_mission(x))
        acceptBtn.place(anchor = "center", x = 400, y = 150)

        # 拒絕按鍵
        global Img_taskSys_showTaskDetails_reject
        Img_taskSys_showTaskDetails_reject = tk.PhotoImage(file = "拒絕.png")
        rejectBtn = tk.Button(taskSys_showTaskDetailsWin)
        rejectBtn.config(image = Img_taskSys_showTaskDetails_reject, width = 72, height = 32)
        rejectBtn.config(relief = "flat", cursor = "hand2", command = taskSys_showTaskDetailsWin.destroy)
        rejectBtn.place(anchor = "center", x = 624, y = 150)
    elif mode == "ongoing":
        data = taskOngoing_listbox.get(taskOngoing_listbox.curselection())
        index = re.findall(r"^[0-9]*", data)
        ls = taskSys_get_tasks_details(index[0])
        taskSys_showTaskDetailsWin = tk.Frame()

        # 背景頁建立
        taskSys_showTaskDetailsWin = tk.Frame(taskSys_searchTask_taskOngoing_Win)
        taskSys_showTaskDetailsWin.config(width = 1024, height = 699, bg = "#363636")
        taskSys_showTaskDetailsWin.place(x = 0, y = 0)

        # 完成按鈕
        global Img_taskSys_showTaskDetails_finish
        Img_taskSys_showTaskDetails_finish = tk.PhotoImage(file = "完成任務.png")
        finishBtn = tk.Button(taskSys_showTaskDetailsWin)
        finishBtn.config(image = Img_taskSys_showTaskDetails_finish, width = 152, height = 32)
        finishBtn.config(relief = "flat", cursor = "hand2", command = lambda x = index[0]: taskSys_finish_mission(x))
        finishBtn.place(anchor = "center", x = 400, y = 150)

        # 放棄按鈕
        global Img_taskSys_showTaskDetails_giveUp
        Img_taskSys_showTaskDetails_giveUp = tk.PhotoImage(file = "放棄任務.png")
        giveUpBtn = tk.Button(taskSys_showTaskDetailsWin)
        giveUpBtn.config(image = Img_taskSys_showTaskDetails_giveUp, width = 152, height = 32)
        giveUpBtn.config(relief = "flat", cursor = "hand2", command = lambda x = index[0]: taskSys_abort_mission(x))
        giveUpBtn.place(anchor = "center", x = 624, y = 150)
    
    # 標題
    title = tk.Label(taskSys_showTaskDetailsWin, text = "任務 No.{}".format(index[0]))
    title.config(font = "微軟正黑體 48 bold", bg = "#363636", fg = "white")
    title.place(anchor = "center", x = 512, y = 60)

    # 返回鍵建立
    backBtn = tk.Button(taskSys_showTaskDetailsWin, text = "回到上頁\nBack")
    backBtn.config(font = "微軟正黑體 15 bold", bg = "#363636", fg = "white", relief = "flat")
    backBtn.config(activebackground = "#363636", activeforeground = "#DF2935")
    backBtn.config(command = taskSys_showTaskDetailsWin.destroy, cursor = "hand2")
    backBtn.place(anchor = "se",x=1024, y=699)

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


def taskSys_get_all_tasks():
    display_list = []
    client = getClient()
    mission_summary = client.open("NTU Coin").worksheet("Missions")
    for i in range(len(mission_summary.col_values(1))):
        if mission_summary.cell(i + 1,6).value == 'on-going':
            ls = mission_summary.row_values(i + 1)
            lst = [ls[0], ls[2], ls[4]]
            display_list.append(lst)
    return display_list


def taskSys_get_users_tasks():
    client = getClient()
    sheet = client.open("NTU Coin").worksheet("Missions")

    accepter_account = userInfo[1]
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


def taskSys_accept_mission(mission_index):
    client = getClient()
    sheet = client.open("NTU Coin").worksheet("Missions")

    accepter_account = userInfo[1]
    #因為有mission_index所以就有一個任務裡面的所有要件了
    sub_time_accept = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
    row = sheet.find(mission_index).row
    status = "taken"
    sheet.update_cell(row,6,status)
    sheet.update_cell(row,7,sub_time_accept)
    sheet.update_cell(row,8,accepter_account)
    ## 一旦標籤不是ongoing的時候，任務總覽裡面就不能有這任務
    taskSysWin.destroy()


def taskSys_abort_mission(mission_index):
    client = getClient()
    sheet = client.open("NTU Coin").worksheet("Missions")

    mission_row = sheet.find(mission_index).row
    if sheet.cell(mission_row, 6).value == "taken":
        status = "on-going"
        sheet.update_cell(mission_row, 6, status)
        sheet.update_cell(mission_row, 8, "N/A")
    taskSysWin.destroy()


def taskSys_get_tasks_details(mission_index):
    mission_index = str(mission_index)
    client = getClient()
    ficher = client.open("NTU Coin").worksheet("Missions")
    mission_row = ficher.find(mission_index).row
    row_list = ficher.row_values(mission_row)
    index = row_list[0]
    name = row_list[2]
    content = row_list[3]
    payment = row_list[4]
    lst = [index, name, content, payment]
    return lst


def taskSys_finish_mission(mission_index):
    client = getClient()
    sheet = client.open("NTU Coin").worksheet("Missions")
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
        client = getClient()
        user_info = client.open("NTU Coin").worksheet("User_Info")
        mission_records = client.open("NTU Coin").worksheet("Mission Record")

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
    taskSysWin.destroy()


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
    global moneyEntryWin_coin2money
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
    try:
        data = eval(moneyEntry_money2coinText.get())
        left = data%1
        if left != 0:
            moneyEntryW_money2coin.set("❕ 請輸入正整數")
        else:
            if data > 0:
                valueSys_runMoney2coin()
                valueSysWin.destroy()
            else:
                moneyEntryW_money2coin.set("❕ 請輸入正整數")
    except:
        moneyEntryW_money2coin.set("❕ 請輸入正整數")


def valueSys_moneyEntry_check_coin2money():
    """確認輸入的數字為正整數"""
    try:
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
                    valueSys_runCoin2money()
                    valueSysWin.destroy()
            else:
                moneyEntryW_coin2money.set("❕ 請輸入正整數")
    except:
        moneyEntryW_coin2money.set("❕ 請輸入正整數")


def valueSys_runMoney2coin():
    client = getClient()

    sheet_coin_money = client.open ("NTU Coin").get_worksheet(4)  # Open the spreadhseet
    sheet_userInfo = client.open ("NTU Coin").get_worksheet(0)

    money = eval(moneyEntry_money2coinText.get())  # 改成輸入的數字

    banlance = eval(getBalance())
    newBalance = str(banlance + money)

    sheet_userInfo.update_cell(userInfo[0], 5, newBalance)  #　更改userInfo 的 Balance

    now = datetime.datetime.now()
    dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
    index = int(len(sheet_coin_money.col_values(1)))
    record = [index, 'norm+', userInfo[1], userInfo[1], money, dt_string, "儲值"]
    sheet_coin_money.append_row(record)


def valueSys_runCoin2money():    
    client = getClient()

    sheet_coin_money = client.open ("NTU Coin").get_worksheet(4)  # Open the spreadhseet
    sheet_userInfo = client.open ("NTU Coin").get_worksheet(0)

    money = -eval(moneyEntryText_coin2moneyText.get())  # 要改成負的

    balance = eval(getBalance())
    newBalance = str(balance + money)

    sheet_userInfo.update_cell(userInfo[0], 5, newBalance)  #　更改userInfo 的 Balance

    now = datetime.datetime.now()
    dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
    index = int(len(sheet_coin_money.col_values(1)))
    record = [index, 'norm-', userInfo[1], userInfo[1], money, dt_string, "提領"]
    sheet_coin_money.append_row(record)


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

    global recordSys_timeBox
    recordSys_timeBox = ttk.Combobox(recordSysWin, font = "微軟正黑體 16 bold")
    recordSys_timeBox["value"] = ("全部", "過去一週", "過去一月", "過去一年")
    recordSys_timeBox.config(width = 12, justify = "center")
    recordSys_timeBox["state"] = "readonly"
    recordSys_timeBox.current(0)
    recordSys_timeBox.place(anchor = "center", x = 150, y = 160)
    
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
    recordSys_ckbtn_rev.config(text = "收入", font = "FangSong 20 bold", fg = "white", bg = "#363636")
    recordSys_ckbtn_rev.config(variable = recordSys_ckbtn_var, value = 0, state = "disable")
    recordSys_ckbtn_rev.config(activebackground = "#363636", activeforeground	= "white", selectcolor = "#5C5C5C")
    recordSys_ckbtn_rev.config(command = recordSys_search_changeType)
    recordSys_ckbtn_rev.place(anchor = "e", x = 145, y = 230)

    recordSys_ckbtn_exp = tk.Radiobutton(recordSysWin)
    recordSys_ckbtn_exp.config(text = "支出", font = "FangSong 20 bold", fg = "white", bg = "#363636")
    recordSys_ckbtn_exp.config(variable = recordSys_ckbtn_var, value = 1, state = "disable")
    recordSys_ckbtn_exp.config(activebackground = "#363636", activeforeground	= "white", selectcolor = "#5C5C5C")
    recordSys_ckbtn_exp.config(command = recordSys_search_changeType)
    recordSys_ckbtn_exp.place(anchor = "w", x = 145, y = 230)

    # 內容顯示框
    global recordSys_revenueSection
    recordSys_revenueSection = tk.Frame(recordSysWin)
    recordSys_revenueSection.config(width = 800, height = 350, bg = "#363636")
    recordSys_revenueSection.place(anchor = "n", x= 512,  y = 250)

    # y軸scrollbar
    global recordSys_revenueBar1
    recordSys_revenueBar1 = tk.Scrollbar(recordSys_revenueSection)
    recordSys_revenueBar1.pack(side = tk.RIGHT, fill = tk.Y)

    # 放入信息
    global recordSys_listbox
    recordSys_listbox = tk.Listbox(recordSys_revenueSection, yscrollcommand = recordSys_revenueBar1.set)
    recordSys_listbox.config(font = "FangSong 20 bold", width = 60, height =13, bg = "#5C5C5C", fg = "white")
    recordSys_listbox.config(selectbackground = "#5C5C5C", activestyle = "none")
    #先加入header
    header = ["日期", "用戶號", "種類", "內容", "金額"]
    tplt_header = "{0:{5}^6}{1:{5}^5}   {2:{5}^4}{3:{5}^10} {4:{5}>4}"
    recordSys_listbox.insert(0, tplt_header.format(header[0], header[1], header[2], header[3], header[4], chr(12288)))
    # 再加入用戶記錄
    global recordSys_record_ls
    # recordSys_record_ls = [["12/11", "daniel", "吃飯", "$1"], ["5/12", "l", "幫", "$100000"], ["12/13", "d", "幫", "$1"], ["12/13", "tallllDaniel", "幫道道道到到到道道道", "$100000"], ["5/12", "tallllDaniel", "幫", "$100000"], ["12/13", "dogg", "幫", "$10"], ["12/13", "dogg", "幫道道道到", "$10"], ["5/12", "tallllDaniel", "幫", "$100000"], ["12/13", "dogg", "幫", "$10"], ["12/13", "dogg", "幫道道道到", "$10"], ["5/12", "tallllDaniel", "幫", "$100000"], ["12/13", "dogg", "幫", "$10"], ["12/13", "dogg", "幫道道道到", "$10"]]
    recordSys_record_ls = [[" ", " ", chr(12288), chr(12288), " "]]*10
    tplt = "{0:^12}{1:^10}{5}{2:{5}^4}{3:{5}^10}{4:^8}"
    for i, content in enumerate(recordSys_record_ls):
        recordSys_listbox.insert(i + 1, tplt.format(content[0], content[1], content[2], content[3], content[4],chr(12288)))
    recordSys_listbox.pack(side = tk.LEFT, fill = tk.BOTH)
    recordSys_revenueBar1.config(command = recordSys_listbox.yview)
    

def crawler_userInfo():
    client = getClient()
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
    recordSys_record_ls = recordSys_getList(1)
    tplt = "{0:^12}{1:^10}{5}{2:{5}^4}{3:{5}^10}{4:>8}"
    for i, content in enumerate(recordSys_record_ls):
        recordSys_listbox.insert(1, tplt.format(content[0], content[1], content[2], content[3], content[4], chr(12288)))


def recordSys_search_changeType():
    recordSys_listbox.delete(1, "end")
    if recordSys_ckbtn_var.get() == 0:
        recordSys_record_ls = recordSys_getList(1)
    else:
        recordSys_record_ls = recordSys_getList(2)
    tplt = "{0:^12}{1:^10}{5}{2:{5}^4}{3:{5}^10}{4:>8}"
    for i, content in enumerate(recordSys_record_ls):
        recordSys_listbox.insert(1, tplt.format(content[0], content[1], content[2], content[3], content[4], chr(12288)))


def recordSys_getList(mode):
    client = getClient()

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
            if int(i[j].get("Amount")) == 0:
                pass
            else:
                data.append(i[j])

    # print(data)
    # 更改日期格式
    def trans_time(adict):
        origin_time = adict.get('Time')
        new_time = origin_time[:10]
        adict['Time'] = new_time
        return adict

    user = userInfo[1]

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
        if all_user_records[i].get('Status') == 'norm-' or all_user_records[i].get("Status") == "spec-":
            payment_records.append(all_user_records[i])
        else:
            income_records.append(all_user_records[i])

    # print(payment_records)

    # 時間篩選器

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
                if records[i].get('category') == param2:
                    new_records.append(records[i])
        
        return new_records

    # 關鍵字篩選器
    def select_key(records, param3, param4):
        new_records = []
        for i in range(len(records)):
            if param3 == '用戶名':
                if param4 in re.findall(r"^[A-Za-z0-9]*", records[i].get('Exchange Account'))[0]:
                    new_records.append(records[i])
            elif param3 == '內容關鍵字':
                if param4 in records[i].get('Description'):
                    new_records.append(records[i])
            else:
                pass

        return new_records

    # 與GUI連結，讓使用者自訂查詢依據
    button1 = recordSys_timeBox.get()
    button2 = recordSys_classBox.get()
    button3 = recordSys_typeBox.get()
    button4 = recordSys_keywordEntryText.get()

    # [篩選後的收入記錄，篩選後的支出記錄]
    selected = []
    # print(income_records)
    for i in (income_records, payment_records):
        
        time_records = select_time(i, button1)
        # print("TIME", time_records)
        category_records = select_category(time_records, button2)
        # print("CATE", category_records)

        if button2 == '儲值記錄':
            selected.append(category_records)
        else:
            if button3 == '-無-':
                selected.append(category_records)
            else:
                key_records = select_key(category_records, button3, button4)
                selected.append(key_records)
    # print(time_records)
    # print(selected[0])

    # 將篩選結果轉換為清單儲存
    def output_records(records):
        output = []

        for i in range(len(records)):
            date = records[i].get('Time')
            # account = records[i].get('Exchange Account')[:9]
            account = re.findall(r"^[A-Za-z0-9]*", records[i].get('Exchange Account'))[0]
            category = records[i].get('category')
            description = records[i].get('Description')
            amount = int(records[i].get('Amount'))
            temp = [date, account, category, description, amount]
            output.append(temp)
        
        return output
    

    if mode == 1:
        result_income = output_records(selected[0])  # 檢索結果：收入
        return result_income
    elif mode == 2:
        result_payment = output_records(selected[1]) # 檢索結果：支出
        return result_payment


def getBalance():
    scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("NTU Coin-0555c96087e3.json", scope)
    client = gspread.authorize(creds)
    sheet = client.open("NTU Coin").get_worksheet(0)  # Open the spreadhseet
    balance = sheet.row_values(userInfo[0])[4]
    return balance


def is_all_chinese(string):
    for word in string:
        if not '\u4e00' <= word <= '\u9fa5':
            return False
    return True


def getClient():
    scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("NTU Coin-0555c96087e3.json", scope)
    client = gspread.authorize(creds)
    return client


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
