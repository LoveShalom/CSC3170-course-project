"""
Time: 2024/11/17
Author: Deng Yifan
Handle the recent order and make a order
"""
import pickle
import re

import Serverinfolist
from Message import Message


def recent_order(account, socket1):
    # send a message
    mes = pickle.dumps(Message(account, Serverinfolist.recent_order_mes, account, True, Serverinfolist.Cli))
    socket1.send(mes)

    # get content
    mes_r = socket1.recv(4096)
    mes_rec = pickle.loads(mes_r)
    content = mes_rec.getcontent()

    # print the information
    print("---------------Order list ---------------")
    print("|   id   |   shop id   |   client id   |   total price   |   status   |   pay status   |   time   |")

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


def make_order(account, socket1):
    # get restaurant
    mes1 = pickle.dumps(Message(account, Serverinfolist.make_order_mes, "get restaurant", True, Serverinfolist.Cli))
    socket1.send(mes1)

    # get content
    mes_r1 = socket1.recv(4096)
    mes_rec1 = pickle.loads(mes_r1)
    content = mes_rec1.getcontent()

    # print the information
    print("---------------Restaurant list ---------------")
    print("|   id   |   name   |   store manager   |   num of employees   |   level   |   num of food   |    join "
          "time    |")

    r_id = ""
    while True:
        for i in range(len(content)):
            line = "|   " + str(content[i][0]) + "   |   " + str(content[i][1]) + "   |   " + str(
                content[i][3]) + "   |   " + str(content[i][5]) + "   |   " + str(
                content[i][6]) + "   |   " + str(content[i][7]) + "   |"
            print(line)
        print("Enter the id of restaurant:")
        ch = input(">>>")
        r_id = int(ch)
        if ch != "":
            break

    # get food of restaurant
    # get restaurant
    # print(r_id)
    # print("start to check food!")
    mes2 = pickle.dumps(Message(account, Serverinfolist.make_order_mes, r_id, True, Serverinfolist.Cli))
    test = pickle.loads(mes2)
    # print(test.getcontent())
    socket1.send(mes2)

    # get content
    mes_r2 = socket1.recv(4096)
    mes_rec2 = pickle.loads(mes_r2)
    content2 = mes_rec2.getcontent()

    # print the information
    print("---------------Food list ---------------")
    print("|   id   |   shop id   |   name   |   material   |   tasty   |   food type   |   price   |   cost   |    "
          "add time    |")

    while True:
        for i in range(len(content2)):
            line = "|   " + str(content2[i][0]) + "   |   " + str(content2[i][1]) + "   |   " + str(
                content2[i][2]) + "   |   " + str(content2[i][3]) + "   |   " + str(content2[i][4]) + "   |   " + str(
                content2[i][9]) + "   |   " + str(content2[i][5]) + "   |   " + str(content2[i][6]) + "   |   " + str(
                content2[i][7]) + "   |"
            print(line)
        print("Enter the food you want in this form: 'food1_id * num1, food2_id * num2,...'")
        ch1 = input(">>>")
        if ch1 != "":
            break

    # make order
    content = re.split(", ", ch1)
    mes3 = pickle.dumps(Message(account, Serverinfolist.make_order_mes, content, True, Serverinfolist.Cli))
    socket1.send(mes3)

    # get result message
    mes_r = socket1.recv(4096)
    mes_rec = pickle.loads(mes_r)

    if mes_rec.getcontent() == -1:
        print("------Your account balance is insufficient, please recharge as soon as possible")

    elif mes_rec.getcontent() == 1:
        print("------The order is successful, please wait for the food to be prepared")



def today_order(account, socket1):
    # send a message
    mes = pickle.dumps(Message(account, Serverinfolist.today_order_mas, account, True, Serverinfolist.Cli))
    socket1.send(mes)

    # get content
    mes_r = socket1.recv(4096)
    mes_rec = pickle.loads(mes_r)
    content = mes_rec.getcontent()

    # print the information
    print("---------------Order list ---------------")
    print("|   id   |   shop id   |   client id   |   total price   |   pay status   |   time   |")

    while True:
        choice = ""
        for i in range(len(content)):
            line = "|   " + str(content[i][0]) + "   |   " + str(content[i][1]) + "   |   " + str(
                content[i][2]) + "   |   " + str(content[i][3]) + "   |   " + str(
                content[i][5]) + "   |   " + str(content[i][6]) + "   |"
            print(line)
        print("---------------Enter 1 if you want refund----------------")
        print("---------------Enter q to leave----------------")
        choice = input(">>>")
        if choice == "1":
            id_order = input(">>> The order id which you want to refund:")
            reason = input(">> >why you want to refund:")
            content = [id_order, reason]
            # send a mes
            mes = pickle.dumps(Message(account, Serverinfolist.refund_mes, content, True, Serverinfolist.Cli))
            socket1.send(mes)

            #get result
            mes_r = socket1.recv(4096)
            mes_rec = pickle.loads(mes_r)
            if mes_rec.getcontent() == 1:
                print("A refund request has been sent, please wait patiently for the result")
                print("---------------------------------------------------------------------")
                break

        if choice == "q":
            break
