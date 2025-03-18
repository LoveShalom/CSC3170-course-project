"""
Time: 2024/11/15
Author: Deng Yifan

This is the thread to handle the client user. Functions: login, register, get personal info, modify info, balance, make
order, make refund
"""
import pickle
import sqlite3
from Message import Message
import Serverinfolist
import re
import datetime as dt


def ClientThread(mes, socket):
    # handle with the type of message
    if mes.getmes_type() == Serverinfolist.log_mes:
        login_handler(mes, socket)

    if mes.getmes_type() == Serverinfolist.regis_mes:
        register_handler(mes, socket)

    if mes.getmes_type() == Serverinfolist.get_client_info:
        info_handler(mes, socket)

    if mes.getmes_type() == Serverinfolist.modify_client_info:
        modify_handler(mes, socket)

    if mes.getmes_type() == Serverinfolist.balance_info:
        balance_handler(mes, socket)

    if mes.getmes_type() == Serverinfolist.recent_order_mes:
        recent_order_handler(mes, socket)

    if mes.getmes_type() == Serverinfolist.today_order_mas or mes.getmes_type() == Serverinfolist.refund_mes:
        today_order_handler(mes, socket)

    if mes.getmes_type() == Serverinfolist.make_order_mes:
        make_order_handler(mes, socket)
    pass


def login_handler(mes, socket):
    # get account and password from message
    mes_split = mes.getcontent()
    account = mes_split[0]
    password = mes_split[1]

    # connect to database and match
    # First check whether the user already exist.
    conn = sqlite3.connect('E:/csc3170/csc3170_project/food_order_system/database/csc3170.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE account=? AND password =?", (account, password))  # Whether the user exit
    result = c.fetchone()

    # fetch result and return message
    login_success = False
    if result:
        login_success = True

    mes_send = pickle.dumps(Message("Sever", Serverinfolist.log_mes, " ", login_success, mes.getuser_type()))
    # print("send message")
    socket.send(mes_send)
    conn.close()


def register_handler(mes, socket):
    # arrange the message
    mes_split = re.split("~", mes.getcontent())
    print(mes_split)
    account = mes_split[0]
    password = mes_split[1]
    phone = mes_split[2]
    balance = mes_split[3]
    add_time = mes_split[4]
    modify_time = mes_split[5]

    # insert into database
    # First check whether the user already exist.
    conn = sqlite3.connect('E:/csc3170/csc3170_project/food_order_system/database/csc3170.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE account=?", (account,))  # Whether the user exit
    result = c.fetchone()

    register_success = -1
    if not result:
        # insert user information into database
        c.execute("INSERT INTO users (account, password, phone, balance, add_time, modify_time) VALUES (?,?,?, ?,?,?)",
                  (account, password, phone, balance, add_time, modify_time))
        conn.commit()
        conn.close()
        register_success = 1

    # send a message to reminder the register is faild
    mes_rec = pickle.dumps(Message(account, Serverinfolist.regis_mes, register_success, False, Serverinfolist.Cli))
    socket.send(mes_rec)
    conn.close()


# get personal info to show
def info_handler(mes, socket):
    # get the username of client
    account = mes.getsender()

    # connect db to get result
    conn = sqlite3.connect("E:/csc3170/csc3170_project/food_order_system/database/csc3170.db")
    c = conn.cursor()

    # search the table and get result
    c.execute("SELECT account, phone, balance, add_time FROM users WHERE account = (?)", (account,))
    result = c.fetchone()
    # print(result)

    # send search result
    mes_rec = pickle.dumps(Message(account, Serverinfolist.get_client_info, result, True, Serverinfolist.Cli))
    socket.send(mes_rec)

    # close
    conn.close()


def modify_handler(mes, socket):
    # get content
    result = mes.getcontent()
    print(result)
    account = mes.getsender()

    # apply change
    conn = sqlite3.connect("E:/csc3170/csc3170_project/food_order_system/database/csc3170.db")
    c = conn.cursor()
    if result[0] != " ":
        c.execute("UPDATE users SET account = (?) WHERE account = (?)", (result[0], account))
        account = result[0]
        conn.commit()

    if result[1] != " ":
        c.execute("UPDATE users SET password = (?) WHERE account = (?)", (result[1], account))
        conn.commit()

    if result[2] != " ":
        c.execute("UPDATE users SET phone = (?) WHERE account = (?)", (result[2], account))
        conn.commit()

    c.execute("UPDATE users SET modify_time = (?) WHERE account = (?)", (result[3], account))
    conn.commit()

    # send a reply message
    mes_rec = pickle.dumps(Message(account, Serverinfolist.modify_client_info, "", True, Serverinfolist.Cli))
    socket.send(mes_rec)

    conn.close()


def balance_handler(mes, socket):
    # arrange content
    money = mes.getcontent()
    account = mes.getsender()

    # connect to db
    conn = sqlite3.connect("E:/csc3170/csc3170_project/food_order_system/database/csc3170.db")
    c = conn.cursor()
    # add money
    c.execute("UPDATE users SET balance = balance + (?) WHERE account = (?)", (money, account))
    conn.commit()

    # get current money
    c.execute("SELECT balance FROM users WHERE account =(?)", (account,))
    result = c.fetchone()

    # send a result message
    mes_rec = pickle.dumps(Message(account, Serverinfolist.balance_info, result, True, Serverinfolist.Cli))
    socket.send(mes_rec)

    conn.close()


def recent_order_handler(mes, socket1):
    # connect to db
    conn = sqlite3.connect("E:/csc3170/csc3170_project/food_order_system/database/csc3170.db")
    c = conn.cursor()

    # get client id
    c.execute("SELECT id FROM users WHERE account = (?)", (mes.getcontent(),))
    result = c.fetchone()
    c_id = result[0]

    # select all data
    c.execute("SELECT * FROM orders WHERE id_client = (?)", (c_id,))
    content = c.fetchall()
    mes_r = pickle.dumps(Message(mes.getsender(), Serverinfolist.recent_order_mes, content, True, Serverinfolist.Cli))
    socket1.send(mes_r)


def today_order_handler(mes, socket1):
    # connect to db
    conn = sqlite3.connect("E:/csc3170/csc3170_project/food_order_system/database/csc3170.db")
    c = conn.cursor()

    if mes.getmes_type() == Serverinfolist.today_order_mas:
        # get client id
        c.execute("SELECT id FROM users WHERE account = (?)", (mes.getcontent(),))
        result = c.fetchone()
        c_id = result[0]

        # get order id
        c.execute("SELECT * FROM orders WHERE id_client = (?) AND DATE(add_time) = DATE('now')", (c_id, ))
        content = c.fetchall()
        print(content)
        mes_r = pickle.dumps(Message(mes.getsender(), Serverinfolist.today_order_mas, content, True, Serverinfolist.Cli))
        socket1.send(mes_r)

    if mes.getmes_type() == Serverinfolist.refund_mes:
        content = mes.getcontent()
        id_order = content[0]
        reason = content[1]
        n_status = "Wait for refunding!"

        c.execute("UPDATE order_info SET status = (?), refund_reason = (?) WHERE id_order = (?)", (n_status, reason, id_order))
        # c.execute("UPDATE orders SET status = (?) WHERE id = (?)", (n_status, id_order))
        conn.commit()
        conn.close()

        mes_r = pickle.dumps(Message(mes.getsender(), Serverinfolist.refund_mes, 1, True, Serverinfolist.Cli))
        socket1.send(mes_r)



def make_order_handler(mes, socket1):
    # connect to db
    conn = sqlite3.connect("E:/csc3170/csc3170_project/food_order_system/database/csc3170.db")
    c = conn.cursor()
    fd = mes.getcontent()
    print(fd)

    if fd == "get restaurant" and type(fd) == str:
        print('get info of restaurant')
        c.execute("SELECT * FROM restaurants")
        content = c.fetchall()
        mes_r = pickle.dumps(Message(mes.getsender(), Serverinfolist.make_order_mes, content, True, Serverinfolist.Cli))
        socket1.send(mes_r)
        conn.close()
        return

    if type(fd) == int:
        print('get info of food')
        r_id = fd
        c.execute("SELECT * FROM food WHERE id_shop = (?)", (r_id,))
        content = c.fetchall()
        mes_r = pickle.dumps(Message(mes.getsender(), Serverinfolist.make_order_mes, content, True, Serverinfolist.Cli))
        socket1.send(mes_r)
        conn.close()
        return

    elif type(fd) == list:
        print('make order')
        # get id
        account = mes.getsender()
        c.execute("SELECT id FROM users WHERE account = (?)", (account,))
        r = c.fetchone()
        c_id = r[0]

        # default status
        status = "Making"
        pay_status = "Completed"
        add_time = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        modify_time = add_time

        # get total price and r_id
        content = mes.getcontent()
        f_id = str(content)
        p1 = re.split(" * ", content[0])
        print(p1)
        c.execute("SELECT id_shop FROM food WHERE id = (?)", (int(p1[0]),))
        r2 = c.fetchone()
        r_id = r2[0]

        total = 0
        amount = 0
        ok = True
        for l in content:
            l_s = re.split(r'\s?\*\s?', l)
            c.execute("SELECT price FROM food WHERE id = (?)", (int(l_s[0]),))
            r3 = c.fetchone()
            pr = int(r3[0])
            total += pr * int(l_s[1])
            amount += int(l_s[1])

        c.execute("SELECT balance FROM users WHERE account = (?)", (account,))
        result = c.fetchone()
        fee = result[0]
        if fee < total:
            print(" fee is not sufficient!")
            mes_r = pickle.dumps(Message(mes.getsender(), Serverinfolist.make_order_mes, -1, True, Serverinfolist.Cli))
            socket1.send(mes_r)
            return
        else:
            c.execute("UPDATE users SET balance = balance - (?) WHERE account = (?)", (total, account))
            conn.commit()

            # add into table
            para = (r_id, c_id, total, status, pay_status, add_time, modify_time)
            c.execute("INSERT INTO orders (id_shop, id_client, total_price , status, pay_status,add_time, modify_time) "
                      "VALUES (?,?,?,?,?,?,?)", para)
            conn.commit()

            # get order id
            c.execute("SELECT id FROM orders WHERE id_shop = (?) AND id_client =(?) AND add_time =(?)",
                      (r_id, c_id, add_time))
            result2 = c.fetchone()
            o_id = result2[0]

            # inser into order_info table
            para = (o_id, f_id, total, status, amount)
            c.execute("INSERT INTO order_info(id_order, id_food , price, status ,amount) "
                      "VALUES (?,?,?,?,?)", para)
            conn.commit()
            conn.close()
            mes_r = pickle.dumps(Message(mes.getsender(), Serverinfolist.make_order_mes, 1, True, Serverinfolist.Cli))
            socket1.send(mes_r)
            return
