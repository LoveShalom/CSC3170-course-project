"""
Time: 2024/11/17
Author: Deng Yifan

This is use for information center, manager can see the information of different role
"""
import pickle
import socket
import Serverinfolist
from Message import Message


def em_info(name, socket1):
    # send a message
    mes = pickle.dumps(Message(name, Serverinfolist.req_info_employees, "", True, Serverinfolist.Man))
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


def res_info(name, socket1):
    # send a message
    mes = pickle.dumps(Message(name, Serverinfolist.req_info_res, "", True, Serverinfolist.Man))
    socket1.send(mes)

    # get content
    mes_r = socket1.recv(4096)
    mes_rec = pickle.loads(mes_r)
    content = mes_rec.getcontent()

    # print the information
    print("---------------Restaurant list ---------------")
    print("|   id   |   name   |   store manager   |   num of employees   |   level   |   num of food   |    join "
          "time    |")

    while True:
        choice = ""
        for i in range(len(content)):
            line = "|   " + str(content[i][0]) + "   |   " + str(content[i][1]) + "   |   " + str(content[i][3]) + "   |   " + str(content[i][5]) + "   |   " + str(
                content[i][6]) + "   |   " + str(content[i][7]) + "   |"
            print(line)
        print("---------------Enter q to leave----------------")
        choice = input(">>>")
        if choice == "q":
            break


def food_info(name, socket1):
    # send a message
    mes = pickle.dumps(Message(name, Serverinfolist.req_info_food, "", True, Serverinfolist.Man))
    socket1.send(mes)

    # get content
    mes_r = socket1.recv(4096)
    mes_rec = pickle.loads(mes_r)
    content = mes_rec.getcontent()

    # print the information
    print("---------------Food list ---------------")
    print("|   id   |   shop id   |   name   |   material   |   tasty   |   food type   |   price   |   cost   |    "
          "add time    |")

    while True:
        choice = ""
        for i in range(len(content)):
            line = "|   " + str(content[i][0]) + "   |   " + str(content[i][1]) + "   |   " + str(
                content[i][2]) + "   |   " + str(content[i][3]) + "   |   " + str(content[i][4]) + "   |   " + str(
                content[i][9]) + "   |   " + str(content[i][5]) + "   |   " + str(content[i][6]) + "   |   " + str(
                content[i][7]) + "   |"
            print(line)
        print("---------------Enter q to leave----------------")
        choice = input(">>>")
        if choice == "q":
            break


def order_info(name, socket1):
    # send a message
    mes = pickle.dumps(Message(name, Serverinfolist.req_info_order, "", True, Serverinfolist.Man))
    socket1.send(mes)

    # get content
    mes_r = socket1.recv(4096)
    mes_rec = pickle.loads(mes_r)
    content = mes_rec.getcontent()

    # print the information
    print("---------------Order list ---------------")
    print("|   id   |   shop if   |   client id   |   total price   |   status   |   pay status   |   time   |")

    while True:
        choice = ""
        for i in range(len(content)):
            line = "|   " + str(content[i][0]) + "   |   " + str(content[i][1]) + "   |   " + str(
                content[i][2]) + "   |   " + str(content[i][3]) + "   |   " + str(content[i][4]) + "   |   " + str(
                content[i][5]) + "   |   " + str(content[i][6]) + "   |"
            print(line)
        print("---------------Enter q to leave----------------")
        choice = input(">>>")
        if choice == "q":
            break


def managers_info(name, socket1):
    # send a message
    mes = pickle.dumps(Message(name, Serverinfolist.req_info_manager, "", True, Serverinfolist.Man))
    socket1.send(mes)

    # get content
    mes_r = socket1.recv(4096)
    mes_rec = pickle.loads(mes_r)
    content = mes_rec.getcontent()

    # print the information
    print("---------------Manager list ---------------")
    print("|   id   |   work id   |   name   |   join time   |")

    while True:
        choice = ""
        for i in range(len(content)):
            line = "|   " + str(content[i][0]) + "   |   " + str(content[i][1]) + "   |   " + str(
                content[i][2]) + "   |   " + str(content[i][3]) + "   |   " + str(content[i][4]) + "   |"
            print(line)
        print("---------------Enter q to leave----------------")
        choice = input(">>>")
        if choice == "q":
            break