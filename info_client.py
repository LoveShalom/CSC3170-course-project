"""
Time: 2024/11/9
Author: Deng Yifan

This is mainly used to show the information of their personal information. The main function is: See personal info,
Modify personal information and add money to users' account

"""
import pickle
import sqlite3
import socket
import datetime as dt
from Message import Message

import Serverinfolist


# Show their personal info
def info_check(account, socket):
    # connect database
    while True:
        # send a message
        mes = pickle.dumps(Message(account, Serverinfolist.get_client_info, " ", True, Serverinfolist.Cli))
        socket.send(mes)

        # receive a message
        mes_r = socket.recv(4096)
        mes_rec = pickle.loads(mes_r)

        result = mes_rec.getcontent()
        # print(result)

        # print need information
        print("--------------------------------------------")
        print(">>> Your name: {}".format(result[0]))
        print(">>> Your phone: {}".format(result[1]))
        print(">>> Your current balance:{}".format(result[2]))
        print(">>> The time you register:{}".format(result[3]))
        # whether come back
        print("--------------------------------------------")
        print("Do you want to return now? Press 1, you will return. ")
        ch = input(">>> Your choice:")
        if ch == "1":
            return 0


# Modify personal information
def modify_info(account, socket):  # Modify the personal information
    # name change
    new_name = " "
    print("Need to change your name? Press 1 if you want. If not, press 2")
    name_change = input(">>>")
    if name_change == "1":
        new_name = input(">>> Please enter your new name:")

    # password change
    new_password = " "
    print("Need to change your password? Press 1 if you want. If not, press 2")
    password_change = input(">>>")
    if password_change == "1":
        while True:
            new_password = input(">>> Please enter your new password:")
            comfirm = input(">>> Please enter again to confirm:")
            if new_password != comfirm:
                print(">>> Passwords do not match. Please try again.")
            else:
                break


    # phone change
    new_phone = " "
    print("Need to change your phone? Press 1 if you want. If not, press 2")
    phone_change = input(">>>")
    if phone_change == "1":
        new_phone = input(">>> Please enter your new phone:")

    modify_time = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # send a message to apply change
    content = [new_name, new_password, new_phone, modify_time]
    print(content)

    mes = pickle.dumps(Message(account, Serverinfolist.modify_client_info, content, True, Serverinfolist.Cli))
    socket.send(mes)

    # receive result
    mes_r = socket.recv(4096)
    mes_rec = pickle.loads(mes_r)

    new_account = mes_rec.getsender()
    print(new_account)

    return new_account


# Add money to balance. To simplify, I skipped the WeChat or Alipay transfer step.
def balance(account, socket):
    print("----------------------------------------------")
    print("Please enter the amount of money to add:")
    money = input(">>>")

    # send a message
    mes = pickle.dumps(Message(account, Serverinfolist.balance_info, money,True,Serverinfolist.Cli))
    socket.send(mes)

    # get result
    mes_r = socket.recv(4096)
    mes_rec = pickle.loads(mes_r)

    print("----------------Successfully! Current balance is {}-----------------".format(mes_rec.getcontent()))

