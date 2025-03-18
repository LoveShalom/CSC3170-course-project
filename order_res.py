"""
Time: 2024/11/17
Author: Deng Yifan
Handle the recent order and make an order, show order need to complete and make complete
"""
import socket
import pickle
import Serverinfolist
from Message import Message


def recent_order(name, socket1):
    # send a message
    mes = pickle.dumps(Message(name, Serverinfolist.recent_order_mes, name, True, Serverinfolist.Res))
    socket1.send(mes)

    # get content
    mes_r = socket1.recv(4096)
    mes_rec = pickle.loads(mes_r)
    content = mes_rec.getcontent()

    # print the information
    print("---------------Order list ---------------")
    print("|   id   |   client id   |   total price   |   status   |   pay status   |   time   |")

    while True:
        choice = ""
        for i in range(len(content)):
            line = "|   " + str(content[i][0]) + "   |   " + str(
                content[i][2]) + "   |   " + str(content[i][3]) + "   |   " + str(content[i][4]) + "   |   " + str(
                content[i][5]) + "   |   " + str(content[i][6]) + "   |"
            print(line)
        print("---------------Enter q to leave----------------")
        choice = input(">>>")
        if choice == "q":
            break
    pass


def orders(name, socket1):
    # first, show current order
    # then, enter the order have finished,and send a message
    # finally, the status will change
    while True:
        # send a message
        mes = pickle.dumps(Message(name, Serverinfolist.order_status_info, "Get order uncompleted!", True, Serverinfolist.Res))
        socket1.send(mes)

        # get result
        mes_r = socket1.recv(4096)
        mes_rec = pickle.loads(mes_r)
        content = mes_rec.getcontent()

        # print the information
        print("---------------Order list ---------------")
        print("|   id   |   food list   |   total price   |   amount   |   user   |   phone   |   add time   |")

        for i in range(len(content)):
            line = "|   " + str(content[i][0]) + "   |   " + str(
                content[i][1]) + "   |   " + str(content[i][2]) + "   |   " + str(content[i][3]) + "   |   " + str(
                content[i][4]) + "   |   " + str(content[i][5]) + "   |   " + str(content[i][6]) + "   |"
            print(line)

        print("--Enter the id of order if it completed. If you want to leave, then enter q")
        print("--If more than one order have been completed, enter in this form: id,id,id,...")
        ids = input(">>>")

        if ids == "q":
            break

        else:
            mes2 = pickle.dumps(Message(name, Serverinfolist.order_status_info, ids, True, Serverinfolist.Res))
            socket1.send(mes2)

            # receive a mes
            mes_r2 = socket1.recv(4096)
            mes_rec2 = pickle.loads(mes_r2)

            if mes_rec2.getcontent == 1:
                print("----------Successfully! Please continue to complete other orders.")




def refund_controler(name,socket1):
    # first, print all order need to refund
    # make decision, and send to handler
    # update table
    while True:
        # send a message
        mes = pickle.dumps(Message(name, Serverinfolist.req_refund, "Get refund order!", True, Serverinfolist.Res))
        socket1.send(mes)

        # get result
        mes_r = socket1.recv(4096)
        mes_rec = pickle.loads(mes_r)
        content = mes_rec.getcontent()

        # print the information
        print("--------------- Refund Order list ---------------")
        print("|   id   |   food list   |   total price   |   amount   |   user   |   phone   |   add time   |   "
              "refund reason   |")
        for i in range(len(content)):
            line = "|   " + str(content[i][0]) + "   |   " + str(
                content[i][1]) + "   |   " + str(content[i][2]) + "   |   " + str(content[i][3]) + "   |   " + str(
                content[i][4]) + "   |   " + str(content[i][5]) + "   |   " + str(content[i][6]) + "   |   " + str(content[i][7])
            print(line)

        print("--Enter the id of order to continue. If you want to leave, then enter q")
        o_id = input(">>>")
        if o_id == "q":
            break
        else:
            result = input(">>>Decision(1: agree/2: disagree): ")
            reason = input(">>>Reason:")
            attri = [o_id, result, reason]
            mes2 = pickle.dumps(Message(name, Serverinfolist.req_refund, attri, True, Serverinfolist.Res))
            socket1.send(mes2)

