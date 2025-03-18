"""
Time: 2024/11/17
Author: Deng Yifan

Handle the request from manager, and the main function including get info of restaurant, food, employees, order and
allocate job for work-study students.
"""
import pickle
import sqlite3

import Serverinfolist
import socket

from Message import Message


def ManaThread(mes, socket1):
    if mes.getmes_type() == Serverinfolist.log_mes:
        login_handler(mes, socket1)

    if mes.getmes_type() == Serverinfolist.regis_mes:
        register_handler(mes, socket1)

    if mes.getmes_type() == Serverinfolist.resignation_mes:
        resignation_handler(mes, socket1)

    if mes.getmes_type() == Serverinfolist.req_info_res or mes.getmes_type() == Serverinfolist.req_info_order or mes.getmes_type() == Serverinfolist.req_info_food or mes.getmes_type() == Serverinfolist.req_info_employees or mes.getmes_type() == Serverinfolist.req_info_manager:
        info_handler(mes, socket1)


def login_handler(mes, socket1):
    # get account and password from message
    mes_split = mes.getcontent()
    m_id = mes_split[0]
    password = mes_split[1]

    # connect to database and match
    # First check whether the user already exist.
    conn = sqlite3.connect('E:/csc3170/csc3170_project/food_order_system/database/csc3170.db')
    c = conn.cursor()
    c.execute("SELECT * FROM canteen_managers WHERE work_id=? AND password=?", (m_id, password))
    result = c.fetchone()
    print(result)

    # fetch result and return message
    login_success = False
    if result:
        login_success = True

    mes_send = pickle.dumps(Message("Sever", Serverinfolist.log_mes, " ", login_success, mes.getuser_type()))
    # print("send message")
    socket1.send(mes_send)
    conn.close()


def register_handler(mes, socket1):
    # arrange the message
    mes_split = mes.getcontent()
    m_id = mes_split[0]
    name = mes_split[1]
    password = mes_split[2]
    add_time = mes_split[3]
    modify_time = mes_split[4]

    # insert into database
    # First check whether the user already exist.
    conn = sqlite3.connect('E:/csc3170/csc3170_project/food_order_system/database/csc3170.db')
    c = conn.cursor()
    c.execute("SELECT * FROM canteen_managers WHERE work_id=?", (m_id,))  # Whether the user exit
    result = c.fetchone()

    register_success = -1
    if not result:
        # insert user information into database
        c.execute("INSERT INTO canteen_managers (work_id, name, password, add_time, modify_time) VALUES (?,?,?,?,?"
                  ")", (m_id, name, password, add_time, modify_time))
        conn.commit()
        conn.close()
        register_success = 1

    # send a message to reminder the register is faild
    mes_rec = pickle.dumps(Message(name, Serverinfolist.regis_mes, register_success, False, Serverinfolist.Res))
    socket1.send(mes_rec)
    conn.close()


def resignation_handler(mes, socket1):
    work_id = mes.getsender()
    conn = sqlite3.connect('E:/csc3170/csc3170_project/food_order_system/database/csc3170.db')
    c = conn.cursor()
    # Delete the information of user
    c.execute("DELETE FROM canteen_managers WHERE work_id = (?)", (work_id,))
    conn.commit()

    # return a result message
    mes_rec = pickle.dumps(Message(work_id, Serverinfolist.regis_mes, "", False, Serverinfolist.Res))
    socket1.send(mes_rec)
    conn.close()


def info_handler(mes, socket1):
    # connect to db
    conn = sqlite3.connect("E:/csc3170/csc3170_project/food_order_system/database/csc3170.db")
    c = conn.cursor()

    if mes.getmes_type() == Serverinfolist.req_info_res:
        c.execute("SELECT * FROM restaurants")
        content = c.fetchall()
        mes_r = pickle.dumps(Message(mes.getsender(), Serverinfolist.req_info_res, content, True, Serverinfolist.Man))
        socket1.send(mes_r)

    if mes.getmes_type() == Serverinfolist.req_info_order:
        c.execute("SELECT * FROM orders")
        content = c.fetchall()
        mes_r = pickle.dumps(Message(mes.getsender(), Serverinfolist.req_info_order, content, True, Serverinfolist.Man))
        socket1.send(mes_r)

    if mes.getmes_type() == Serverinfolist.req_info_food:
        c.execute("SELECT * FROM food")
        content = c.fetchall()
        mes_r = pickle.dumps(Message(mes.getsender(), Serverinfolist.req_info_food, content, True, Serverinfolist.Man))
        socket1.send(mes_r)

    if mes.getmes_type() == Serverinfolist.req_info_employees:
        c.execute("SELECT * FROM employees")
        content = c.fetchall()
        mes_r = pickle.dumps(Message(mes.getsender(), Serverinfolist.req_info_employees, content, True, Serverinfolist.Man))
        socket1.send(mes_r)

    if mes.getmes_type() == Serverinfolist.req_info_manager:
        c.execute("SELECT * FROM canteen_managers")
        content = c.fetchall()
        mes_r = pickle.dumps(Message(mes.getsender(), Serverinfolist.req_info_manager, content, True, Serverinfolist.Man))
        socket1.send(mes_r)

    conn.close()

