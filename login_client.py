"""
Time: 2024/11/8
Author: Deng Yifan

It contains the login and register. If register successfully, it will return to the login page. If not, it will show the
 user exit. If user fail to log in, it will show wrong message and repeat login page.
"""
from Message import Message
import Serverinfolist
import socket
import pickle
import sqlite3
import datetime as dt
import pyautogui


def login_page(socket_client):
    # iflogin = True
    account = ""
    while True:
        print("------------Welcome to CUHKSZ food order System------------")
        print("Please login or register to continue.")
        print("1. Login")
        print("2. Register")
        print("3, Exit")
        choice = input("Enter your choice (1/2/3): ")
        check = 0
        if choice == "1":
            pyautogui.hotkey("Alt", "c")
            account, check = login(socket_client)
            if check == 1:
                return account, check
        elif choice == "2":
            pyautogui.hotkey("Alt", "c")
            register(socket_client)
        elif choice == "3":
            mes = pickle.dumps(Message(account, Serverinfolist.exit_mes, "", False, Serverinfolist.Cli))
            socket_client.send(mes)
            return None, -1


# login function, which used to packege a login message
def login(socket_client):
    account = input("Enter your username: ")
    password = input("Enter your password: ")
    content = [account, password]
    # print(content)

    # connect to database and check if username and password match
    # if match, redirect to home page
    # if not, show wrong message and repeat login page
    # if user not exist, show user not exist message and repeat login page

    # send message
    mes = pickle.dumps(Message(account, Serverinfolist.log_mes, content, False, Serverinfolist.Cli))
    # print("Sending data: {}".format(mes))  # 打印发送的数据
    socket_client.send(mes)

    # get result
    mes_r = socket_client.recv(4096)
    mes_rec = pickle.loads(mes_r)

    # respond to the result
    if mes_rec.getloginsuccess() == True:
        pyautogui.hotkey("Alt", "c")
        print(">>> Login successfully! Welcome!")
        print("----------------------------------")
        return account, 1
    else:
        pyautogui.hotkey("Alt", "c")
        print(">>> Wrong username or password. Please try again.")
        return None, 0


# register function
def register(socket_client):
    # get necessary information from user
    account = input("Enter your username: ")
    password = ""
    for_password = False
    while not for_password:
        password = input("Enter your password: ")
        password_confirm = input("Confirm your password: ")
        if password == password_confirm:
            for_password = True
        else:
            print(">>> Passwords do not match. Please try again.")

    phone = input("Enter your phone number: ")
    balance = 0  # default zero

    # the time when user register
    add_time = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    modify_time = add_time

    #send a message
    content = account + "~" + password + "~" + phone + "~" + str(balance) + "~" + add_time + "~" + modify_time
    mes =pickle.dumps(Message(account, Serverinfolist.regis_mes, content, False, Serverinfolist.Cli))
    socket_client.send(mes)

    # get result message
    mes_r = socket_client.recv(4096)
    mes_rec = pickle.loads(mes_r)

    if mes_rec.getcontent() == 1:
        # insert user information into database
        pyautogui.hotkey("Alt", "c")
        print(">>> Register successfully!")
        print("----------------------------------")

    else:
        pyautogui.hotkey("Alt", "c")
        print(">>> The user already exists, please try again!")
        print("----------------------------------")
