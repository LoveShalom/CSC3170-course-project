"""
Time: 2024/11/9
Author: Deng Yifan

This file is used for the login of canteen managers, if manager want to log in, he should use his work id and password.
If a new manager are assigned to manage the canteen, he should use the work_id (suppose it is offered by school) to
register on system. If the manager resign from canteen, it should use the system to delete his information.
"""
import pickle
import sqlite3
import datetime as dt

import pyautogui

import Serverinfolist
from Message import Message


def login_page(socket1):
    iflogin = True
    while iflogin:
        print("------------Welcome to CUHKSZ canteen manager System------------")
        print("Please login or register to continue.")
        print("1. Login")
        print("2. Register")
        print("3, Resignation")
        print("4, Exit")
        choice = input("Enter your choice (1/2/3/4): ")
        check = 0
        if choice == "1":
            pyautogui.hotkey("Alt", "c")
            account, check = login(socket1)
            if check == 1:
                return account, check
        elif choice == "2":
            pyautogui.hotkey("Alt", "c")
            register(socket1)
        elif choice == "3":
            pyautogui.hotkey("Alt", "c")
            key = resignation(socket1)
            if key == -1:
                return key
        elif choice == "4":
            mes = pickle.dumps(Message(account, Serverinfolist.exit_mes, "", False, Serverinfolist.Cli))
            socket1.send(mes)
            return None, -1


# login function
def login(socket1):
    m_id = input("Enter your work id: ")
    password = input("Enter your password: ")
    content = [m_id, password]

    # connect to database and check if username and password match
    # if match, redirect to home page
    # if not, show wrong message and repeat login page
    # if user not exist, show user not exist message and repeat login page

    # send message
    mes = pickle.dumps(Message(m_id, Serverinfolist.log_mes, content, False, Serverinfolist.Man))
    # print("Sending data: {}".format(mes))  # 打印发送的数据
    socket1.send(mes)

    # get result
    mes_r = socket1.recv(4096)
    mes_rec = pickle.loads(mes_r)

    # respond to the result
    if mes_rec.getloginsuccess() == True:
        pyautogui.hotkey("Alt", "c")
        print(">>> Login successfully! Welcome!")
        print("----------------------------------")
        return m_id, 1
    else:
        pyautogui.hotkey("Alt", "c")
        print(">>> Wrong id or password. Please try again.")
        print(content)
        return None, 0


# register function
def register(socket1):
    # get necessary information from user
    work_id = input("Enter your work_id: ")
    password = ""
    for_password = False
    while not for_password:
        password = input("Enter your password: ")
        password_confirm = input("Confirm your password: ")
        if password == password_confirm:
            for_password = True
        else:
            print(">>> Passwords do not match. Please try again.")

    name = input("Enter your name: ")

    # the time when user register
    add_time = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    modify_time = add_time

    # send a message
    content = [work_id, name, password, add_time, modify_time]
    mes = pickle.dumps(Message(name, Serverinfolist.regis_mes, content, False, Serverinfolist.Man))
    socket1.send(mes)

    # get result message
    mes_r = socket1.recv(4096)
    mes_rec = pickle.loads(mes_r)

    if mes_rec.getcontent() == 1:
        # insert user information into database
        pyautogui.hotkey("Alt", "c")
        print(">>> Register successfully!")
        print("----------------------------------")

    else:
        pyautogui.hotkey("Alt", "c")
        print(">>> The restaurant already exists, please try again!")
        print("----------------------------------")


def resignation(socket1):
    # password for resignation. If the manager is not here to resign, he is not allowed to use this function.
    while True:
        print("Please enter the password to check your right, you can get this from relevant person.")
        password = input(">>>")
        if password != "Welcome to CUHKSZ!":
            print("It's wrong, please try again!")
            print("If you want to try again, enter '1'; Otherwise, enter '2'")
            ch = input(">>>")
            if ch == "2":
                return -1
            elif ch == "1":
                continue
        else:
            break

    print("Please enter your work id.")
    work_id = input(">>>")

    # send a message
    mes = pickle.dumps(Message(work_id, Serverinfolist.resignation_mes, work_id, False, Serverinfolist.Man))
    socket1.send(mes)

    # get a message
    mes_r = socket1.recv(4096)
    mes_rec = pickle.loads(mes_r)

    print("---------You have already delete your information, good luck in the future!---------")
    return -1
