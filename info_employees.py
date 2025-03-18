"""
Time: 2024/11/16
Author: Deng Yifan

This is use for control employees, some functions may be used in different roles
"""

import pickle
import socket
import datetime as dt
import Serverinfolist
from Message import Message


# show employees' info
def employees_list(name, socket1):
    # send a message
    mes = pickle.dumps(Message(name, Serverinfolist.get_employees_info, "", True, Serverinfolist.Res))
    socket1.send(mes)

    # get content
    mes_r = socket1.recv(4096)
    mes_rec = pickle.loads(mes_r)
    content = mes_rec.getcontent()

    # print the information
    print("---------------Employees list ---------------")
    print("|   id   |   name   |   age   |   sex   |   salary   |   status   |    join time    |")

    while True:
        choice = ""
        for i in range(len(content)):
            line = "|   " + str(content[i][0]) + "   |   " + str(content[i][1]) + "   |   " + str(
                content[i][2]) + "   |   " + str(content[i][3]) + "   |   " + str(content[i][5]) + "   |   " + str(
                content[i][6]) + "   |   " + str(content[i][7]) + "   |"
            print(line)
        print("---------------Enter q to leave----------------")
        choice = input(">>>")
        if choice == "q":
            break


def employees_add(name, socket1):
    print("--------Now, you need enter the information of nwe employees--------")
    e_name = input(">> name:")
    age = input(">> age:")
    sex = input(">> sex:")
    salary = input(">> salary:")
    add_time = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # default data
    modify_time = add_time
    r_type = "restaurant employee"
    status = "working"

    content = [e_name, age, sex, r_type, salary, status, add_time, modify_time]
    mes = pickle.dumps(Message(name, Serverinfolist.add_employees_info, content, True, Serverinfolist.Res))
    socket1.send(mes)

    # receive result
    mes_r = socket1.recv(4096)
    mes_rec = pickle.loads(mes_r)

    print("-----{}! Your request have already completed.-----".format(mes_rec.getsender()))


def employees_delete(name, socket1):
    print("Please enter the id of employees you want to delete!")
    ids = input(">>>")

    # send a message
    mes = pickle.dumps(Message(name, Serverinfolist.delete_employees_info, ids, True, Serverinfolist.Res))
    socket1.send(mes)

    # get message
    # receive result
    mes_r = socket1.recv(4096)
    mes_rec = pickle.loads(mes_r)

    print("-----{}! Your request have already completed.-----".format(mes_rec.getsender()))


def employees_modify(name, socket1):
    print("Please enter the information of food you want to modify")
    e_id = input("id:")

    # name change
    new_name = " "
    print("Need to change employee's name? Press 1 if you want. If not, press 2")
    name_change = input(">>>")
    if name_change == "1":
        new_name = input(">>> Please enter new name:")

    # employees age
    new_age = " "
    print("Need to change employee's age? Press 1 if you want. If not, press 2")
    mar_change = input(">>>")
    if mar_change == "1":
        new_age = input(">>> Please enter employee's age:")

    # salary
    new_salary = " "
    print("Need to change salary? Press 1 if you want. If not, press 2")
    pr_change = input(">>>")
    if pr_change == "1":
        new_salary = input(">>> Please enter salary:")

    # status
    new_status = " "
    print("Need to change status? Press 1 if you want. If not, press 2")
    co_change = input(">>>")
    if co_change == "1":
        new_status = input(">>> Please enter status:")

    # modify_time
    modify_time = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # package message
    content = [e_id, new_name, new_age, new_salary, new_status, modify_time]
    mes = pickle.dumps(Message(name, Serverinfolist.modify_employees_info, content, True, Serverinfolist.Res))
    socket1.send(mes)

    # receive a message
    mes_r = socket1.recv(4096)
    mes_rec = pickle.loads(mes_r)

    print("-----{}! Your request have already completed.-----".format(mes_rec.getsender()))
