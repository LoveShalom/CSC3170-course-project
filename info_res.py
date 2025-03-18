"""
Time: 2024/11/16
Author: Deng Yifan

This is mainly used to show the information of their personal information. The main function is: See personal info,
Modify personal information and add money to users' account

"""
import pickle
import sqlite3
import socket
import pyautogui
import datetime as dt
from Message import Message
import re

import Serverinfolist


def info_check(name, socket1):
    # connect database
    while True:
        # send a message
        mes = pickle.dumps(Message(name, Serverinfolist.get_res_info, " ", True, Serverinfolist.Res))
        socket1.send(mes)

        # receive a message
        mes_r = socket1.recv(4096)
        mes_rec = pickle.loads(mes_r)

        result = mes_rec.getcontent()
        # print(result)

        # print need information
        print("--------------------------------------------")
        print(">>> Restaurant's name: {}".format(result[0]))
        print(">>> Restaurant's Manager: {}".format(result[1]))
        print(">>> Number of employees:{}".format(result[2]))
        print(">>> Number of foods:{}".format(result[4]))
        print(">>> Customer Rating:{}".format(result[3]))
        print(">>> Time to join:{}".format(result[5]))
        # whether come back
        print("--------------------------------------------")
        print("Do you want to return now? Press 1, you will return. ")
        ch = input(">>> Your choice:")
        if ch == "1":
            return 0


def modify_info(name, socket1):
    # name change
    new_name = " "
    print("Need to change restaurant name? Press 1 if you want. If not, press 2")
    name_change = input(">>>")
    if name_change == "1":
        new_name = input(">>> Please enter your new name:")

    # password change
    new_password = " "
    print("Need to change the password? Press 1 if you want. If not, press 2")
    password_change = input(">>>")
    if password_change == "1":
        while True:
            new_password = input(">>> Please enter your new password:")
            comfirm = input(">>> Please enter again to confirm:")
            if new_password != comfirm:
                print(">>> Passwords do not match. Please try again.")
            else:
                break

    # Manager
    new_manager = " "
    print("Need to change restaurant's manager? Press 1 if you want. If not, press 2")
    phone_change = input(">>>")
    if phone_change == "1":
        new_phone = input(">>> Please enter the name of your new manager:")

    modify_time = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # send a message to apply change
    content = [new_name, new_password, new_manager, modify_time]
    print(content)

    mes = pickle.dumps(Message(name, Serverinfolist.modify_res_info, content, True, Serverinfolist.Res))
    socket1.send(mes)

    # receive result
    mes_r = socket1.recv(4096)
    mes_rec = pickle.loads(mes_r)

    account = mes_rec.getsender()

    return account


def food_info(name, socket1):
    # package a message
    mes = pickle.dumps(Message(name, Serverinfolist.get_food_info, " ", True, Serverinfolist.Res))
    socket1.send(mes)

    # Get info
    mes_r = socket1.recv(4096)
    mes_rec = pickle.loads(mes_r)

    # print information
    content = mes_rec.getcontent()
    # print(content)
    length = len(content)
    print("---------------Food list ---------------")
    print("|   Food id   |   Food name   |   Tasty   |   Price   |   cost   |   Type   |   Material   |")

    # print info of food
    while True:
        choice = ''
        if length != 0:
            for i in range(length):
                line = "|   " + str(content[i][0]) + "   |   " + str(content[i][2]) + "   |   " + str(content[i][4]) + "   |   " + str(content[i][5]) + "   |   " +str(content[i][6]) + "   |   " + str(content[i][9]) + "   |   " + str(content[i][3]) + "   |   "
                print(line)
        print("----------Enter q to leave----------")
        choice = input(">>")

        # want to leave now
        if choice == "q":
            break


def modify_food(name, socket1):
    # make choice: add, delete or modify
    print("----------What do you want to do?----------")
    print("--1, Add food")
    print("--2, Delete food")
    print("--3, Modify food")
    choice = input("Please enter (1/2/3)")

    if choice == "1":
        pyautogui.hotkey("Alt", "c")
        num = int(input("How many foods want to add:"))
        content = [name]
        for i in range(0, num):
            pyautogui.hotkey("Alt", "c")
            food_name = input("Food name:")
            material = input("Material:")
            tasty = input("Tasty:")
            price = input("Price:")
            cost = input("Cost:")
            food_type = input("Food Type:")
            add_time = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            modify_time = add_time
            con = [food_name, material, tasty, int(price), int(cost), add_time, modify_time, food_type]
            content.append(con)
        print(content)
        # package message
        mes = pickle.dumps(Message(name, Serverinfolist.add_food_info, content, True, Serverinfolist.Res))
        socket1.send(mes)

    if choice == "2":
        pyautogui.hotkey("Alt", "c")
        ids = input("Please enter the food ID and separate them with spaces")
        id_list = re.split(r'\s+', ids)

        # package message
        mes = pickle.dumps(Message(name, Serverinfolist.delete_food_info, id_list, True, Serverinfolist.Res))
        socket1.send(mes)

    if choice == "3":
        pyautogui.hotkey("Alt", "c")
        print("Please enter the information of food you want to modify")
        food_id = input("id:")

        # name change
        new_name = " "
        print("Need to change food name? Press 1 if you want. If not, press 2")
        name_change = input(">>>")
        if name_change == "1":
            new_name = input(">>> Please enter new name:")

        # age
        new_mar = " "
        print("Need to change employee's age? Press 1 if you want. If not, press 2")
        mar_change = input(">>>")
        if mar_change == "1":
            new_mar = input(">>> Please enter food material:")

        # price
        new_price = " "
        print("Need to change food price? Press 1 if you want. If not, press 2")
        pr_change = input(">>>")
        if pr_change == "1":
            new_price = input(">>> Please enter food price:")

        # cost
        new_cost = " "
        print("Need to change food cost? Press 1 if you want. If not, press 2")
        co_change = input(">>>")
        if co_change == "1":
            new_cost = input(">>> Please enter food cost:")

        # modify_time
        modify_time = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # package message
        content = [food_id, new_name, new_mar, new_price, new_cost, modify_time]
        mes = pickle.dumps(Message(name, Serverinfolist.modify_food_info, content, True, Serverinfolist.Res))
        socket1.send(mes)

    # receive a message
    mes_r = socket1.recv(4096)
    mes_rec = pickle.loads(mes_r)

    print("-----{}! Your request have already completed.-----".format(mes_rec.getsender()))
