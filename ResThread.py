"""
Time: 2024/11/16
Author: Deng Yifan

This is the thread to handle the restaurant user. Functions: login, register, get personal info, modify info and so on.
"""
import re
import sqlite3
import pickle
import socket
import Serverinfolist
from Message import Message


def ResThread(mes, socket1):
    # handle with the type of message
    if mes.getmes_type() == Serverinfolist.log_mes:
        login_handler(mes, socket1)

    if mes.getmes_type() == Serverinfolist.regis_mes:
        register_handler(mes, socket1)

    if mes.getmes_type() == Serverinfolist.get_res_info:
        info_handler(mes, socket1)

    if mes.getmes_type() == Serverinfolist.modify_res_info:
        modify_handler(mes, socket1)

    if mes.getmes_type() == Serverinfolist.get_food_info:
        food_handler(mes, socket1)

    if mes.getmes_type() == Serverinfolist.modify_food_info or mes.getmes_type() == Serverinfolist.add_food_info or mes.getmes_type() == Serverinfolist.delete_food_info:
        food_modify_handler(mes, socket1)

    if mes.getmes_type() == Serverinfolist.get_employees_info:
        employees_handler(mes, socket1)

    if mes.getmes_type() == Serverinfolist.modify_employees_info or mes.getmes_type() == Serverinfolist.add_employees_info or mes.getmes_type() == Serverinfolist.delete_employees_info:
        employees_modify_handler(mes, socket1)

    if mes.getmes_type() == Serverinfolist.recent_order_mes:
        recent_order_handler(mes, socket1)

    if mes.getmes_type() == Serverinfolist.order_status_info:
        order_status_handler(mes, socket1)

    if mes.getmes_type() == Serverinfolist.req_refund:
        refund_handler(mes, socket1)


def login_handler(mes, socket1):
    # get account and password from message
    mes_split = mes.getcontent()
    name = mes_split[0]
    password = mes_split[1]

    # connect to database and match
    # First check whether the user already exist.
    conn = sqlite3.connect('E:/csc3170/csc3170_project/food_order_system/database/csc3170.db')
    c = conn.cursor()
    c.execute("SELECT * FROM restaurants WHERE name =? AND password =?", (name, password))  # Whether the user exit
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


# register for restaurant
def register_handler(mes, socket1):
    # arrange the message
    mes_split = mes.getcontent()
    name = mes_split[0]
    password = mes_split[1]
    store_manager = mes_split[2]
    nums_of_employees = mes_split[3]
    level = mes_split[4]
    nums_of_food = mes_split[5]
    add_time = mes_split[6]
    modify_time = mes_split[7]

    # insert into database
    # First check whether the user already exist.
    conn = sqlite3.connect('E:/csc3170/csc3170_project/food_order_system/database/csc3170.db')
    c = conn.cursor()
    c.execute("SELECT * FROM restaurants WHERE name=?", (name,))  # Whether the user exit
    result = c.fetchone()

    register_success = -1
    if not result:
        # insert user information into database
        c.execute("INSERT INTO restaurants (name, password, store_manager, num_of_employees, level, num_foods, "
                  "add_time, modify_time) VALUES (?,?,?,?,?,?,?,?)",
                  (name, password, store_manager, nums_of_employees, level, nums_of_food, add_time, modify_time))
        conn.commit()
        conn.close()
        register_success = 1

    # send a message to reminder the register is faild
    mes_rec = pickle.dumps(Message(name, Serverinfolist.regis_mes, register_success, False, Serverinfolist.Res))
    socket1.send(mes_rec)
    conn.close()


def info_handler(mes, socket1):
    # get the username of client
    name = mes.getsender()

    # connect db to get result
    conn = sqlite3.connect("E:/csc3170/csc3170_project/food_order_system/database/csc3170.db")
    c = conn.cursor()

    # search the table and get result
    c.execute("SELECT name, store_manager, num_of_employees, level, num_foods, add_time FROM restaurants WHERE "
              "name = (?)",
              (name,))
    result = c.fetchone()
    # print(result)

    # send search result
    mes_rec = pickle.dumps(Message(name, Serverinfolist.get_res_info, result, True, Serverinfolist.Res))
    socket1.send(mes_rec)

    # close
    conn.close()


def modify_handler(mes, socket1):
    # get content
    result = mes.getcontent()
    print(result)
    name = mes.getsender()

    # apply change
    conn = sqlite3.connect("E:/csc3170/csc3170_project/food_order_system/database/csc3170.db")
    c = conn.cursor()
    if result[0] != " ":
        c.execute("UPDATE restaurants SET name = (?) WHERE name = (?)", (result[0], name))
        name = result[0]
        conn.commit()

    if result[1] != " ":
        c.execute("UPDATE restaurants SET password = (?) WHERE name = (?)", (result[1], name))
        conn.commit()

    if result[2] != " ":
        c.execute("UPDATE restaurants SET store_manager = (?) WHERE name = (?)", (result[2], name))
        conn.commit()

    c.execute("UPDATE restaurants SET modify_time = (?) WHERE name = (?)", (result[3], name))
    conn.commit()

    # send a reply message
    mes_rec = pickle.dumps(Message(name, Serverinfolist.modify_res_info, "", True, Serverinfolist.Res))
    socket1.send(mes_rec)

    conn.close()


def food_handler(mes, socket1):
    # get the sender
    name = mes.getsender()

    # connect to db
    conn = sqlite3.connect("E:/csc3170/csc3170_project/food_order_system/database/csc3170.db")
    c = conn.cursor()

    # get restaurant id
    c.execute("SELECT id FROM restaurants WHERE name = (?)", (name,))
    result = c.fetchone()
    res_id = result[0]

    # search all food with res_id
    c.execute("SELECT * FROM food WHERE id_shop = (?)", (res_id,))
    content = c.fetchall()

    # package a message
    mes = pickle.dumps(Message(name, Serverinfolist.get_food_info, content, True, Serverinfolist.Res))
    socket1.send(mes)

    conn.close()


def food_modify_handler(mes, socket1):
    # connect to db
    conn = sqlite3.connect("E:/csc3170/csc3170_project/food_order_system/database/csc3170.db")
    c = conn.cursor()

    if mes.getmes_type() == Serverinfolist.add_food_info:
        print("Start to add food")
        content = mes.getcontent()
        name = content[0]
        c.execute("SELECT id FROM restaurants WHERE name = (?)", (name,))
        result = c.fetchone()
        r_id = result[0]
        content.remove(content[0])
        print(content)
        for f in content:
            print(f)
            food_name = f[0]
            material = f[1]
            tasty = f[2]
            price = f[3]
            cost = f[4]
            food_type = f[7]
            add_time = f[5]
            modify_time = f[6]
            param = (r_id, food_name, material, tasty, price, cost, add_time, modify_time, food_type)
            print(param)
            c.execute("INSERT INTO food(id_shop, name, material, tasty, price, cost, add_time, modify_time, "
                      "food_type) VALUES(?,?,?,?,?,?,?,?,?) ",
                      param)
            conn.commit()

            # update the number of food
            c.execute("UPDATE restaurants SET num_foods = num_foods + (?) WHERE id = (?)", (1, r_id))
            conn.commit()
        # send a message to reminder
        mes_rec = pickle.dumps(Message(mes.getsender(), Serverinfolist.add_food_info, "", True, Serverinfolist.Res))
        socket1.send(mes_rec)

    if mes.getmes_type() == Serverinfolist.delete_food_info:
        print("Start to delete food")
        content = mes.getcontent()
        for f_id in content:
            c.execute("SELECT id_shop FROM food WHERE id = (?)", (f_id,))
            result = c.fetchone()
            r_id = result[0]

            c.execute("DELETE FROM food WHERE id = (?)", (int(f_id),))
            conn.commit()
            # update the number of food
            c.execute("UPDATE restaurants SET num_foods = num_foods - (?) WHERE id = (?)", (1, r_id))
            conn.commit()
        # send a reply message
        mes_rec = pickle.dumps(Message(mes.getsender(), Serverinfolist.delete_food_info, "", True, Serverinfolist.Res))
        socket1.send(mes_rec)

    if mes.getmes_type() == Serverinfolist.modify_food_info:
        print("Start to modify food")
        # get content
        result = mes.getcontent()
        print(result)
        f_id = result[0]

        # apply change
        conn = sqlite3.connect("E:/csc3170/csc3170_project/food_order_system/database/csc3170.db")
        c = conn.cursor()
        if result[1] != " ":
            c.execute("UPDATE food SET name = (?) WHERE id = (?)", (result[1], f_id))
            conn.commit()

        if result[2] != " ":
            c.execute("UPDATE food SET material = (?) WHERE id = (?)", (result[2], f_id))
            conn.commit()

        if result[3] != " ":
            c.execute("UPDATE food SET price = (?) WHERE id = (?)", (result[3], f_id))
            conn.commit()

        if result[4] != " ":
            c.execute("UPDATE food SET cost = (?) WHERE id = (?)", (result[4], f_id))
            conn.commit()

        c.execute("UPDATE food SET modify_time = (?) WHERE id = (?)", (result[5], f_id))
        conn.commit()

        # send a reply message
        mes_rec = pickle.dumps(Message(mes.getsender(), Serverinfolist.modify_food_info, "", True, Serverinfolist.Res))
        socket1.send(mes_rec)

    conn.close()


def employees_handler(mes, socket1):
    print("Start to show employees list")
    name = mes.getsender()

    # connect to db
    conn = sqlite3.connect("E:/csc3170/csc3170_project/food_order_system/database/csc3170.db")
    c = conn.cursor()

    # get id
    c.execute("SELECT id FROM restaurants WHERE name = (?)", (name,))
    result = c.fetchone()
    r_id = result[0]

    # get all employees
    c.execute("SELECT * FROM employees WHERE r_id = (?)", (r_id,))
    content = c.fetchall()

    # package a message
    mes = pickle.dumps(Message(name, Serverinfolist.get_employees_info, content, True, Serverinfolist.Res))
    socket1.send(mes)

    conn.close()


def employees_modify_handler(mes, socket1):
    # connect to db
    conn = sqlite3.connect("E:/csc3170/csc3170_project/food_order_system/database/csc3170.db")
    c = conn.cursor()

    if mes.getmes_type() == Serverinfolist.add_employees_info:
        print("Start to add employees")
        content = mes.getcontent()
        name = mes.getsender()
        c.execute("SELECT id FROM restaurants WHERE name = (?)", (name,))
        result = c.fetchone()
        r_id = result[0]

        print(content)

        e_name = content[0]
        age = content[1]
        sex = content[2]
        r_type = content[3]
        salary = content[4]
        status = content[5]
        add_time = content[6]
        modify_time = content[7]
        param = (e_name, age, sex, r_type, salary, status, add_time, modify_time, r_id)
        print(param)
        c.execute("INSERT INTO employees(name, age, sex, type, salary, status, add_time, modify_time, r_id"
                  ") VALUES(?,?,?,?,?,?,?,?,?) ", param)
        conn.commit()
        # send a message to reminder
        mes_rec = pickle.dumps(
            Message(mes.getsender(), Serverinfolist.add_employees_info, "", True, Serverinfolist.Res))
        socket1.send(mes_rec)

    if mes.getmes_type() == Serverinfolist.delete_employees_info:
        print("Start to delete employees")
        content = mes.getcontent()
        c.execute("DELETE FROM employees WHERE id = (?)", (int(content),))
        conn.commit()
        # send a reply message
        mes_rec = pickle.dumps(
            Message(mes.getsender(), Serverinfolist.delete_employees_info, "", True, Serverinfolist.Res))
        socket1.send(mes_rec)

    if mes.getmes_type() == Serverinfolist.modify_employees_info:
        print("Start to modify  employees")
        # get content
        result = mes.getcontent()
        print(result)
        e_id = result[0]

        # apply change
        conn = sqlite3.connect("E:/csc3170/csc3170_project/food_order_system/database/csc3170.db")
        c = conn.cursor()
        if result[1] != " ":
            c.execute("UPDATE employees SET name = (?) WHERE id = (?)", (result[1], e_id))
            conn.commit()

        if result[2] != " ":
            c.execute("UPDATE employees SET age = (?) WHERE id = (?)", (result[2], e_id))
            conn.commit()

        if result[3] != " ":
            c.execute("UPDATE employees SET salary = (?) WHERE id = (?)", (result[3], e_id))
            conn.commit()

        if result[4] != " ":
            c.execute("UPDATE employees SET status = (?) WHERE id = (?)", (result[4], e_id))
            conn.commit()

        c.execute("UPDATE employees SET modify_time = (?) WHERE id = (?)", (result[5], e_id))
        conn.commit()

        # send a reply message
        mes_rec = pickle.dumps(
            Message(mes.getsender(), Serverinfolist.modify_employees_info, "", True, Serverinfolist.Res))
        socket1.send(mes_rec)

    conn.close()


def recent_order_handler(mes, socket1):
    # connect to db
    conn = sqlite3.connect("E:/csc3170/csc3170_project/food_order_system/database/csc3170.db")
    c = conn.cursor()

    # get restaurant id
    c.execute("SELECT id FROM restaurants WHERE name = (?)", (mes.getcontent(),))
    result = c.fetchone()
    r_id = result[0]

    # select all data
    c.execute("SELECT * FROM orders WHERE id_shop = (?)", (r_id,))
    content = c.fetchall()
    mes_r = pickle.dumps(Message(mes.getsender(), Serverinfolist.recent_order_mes, content, True, Serverinfolist.Res))
    socket1.send(mes_r)


def order_status_handler(mes, socket1):
    # connect to db
    conn = sqlite3.connect("E:/csc3170/csc3170_project/food_order_system/database/csc3170.db")
    c = conn.cursor()

    # get restaurant id
    if mes.getcontent() == "Get order uncompleted!":
        c.execute("SELECT id FROM restaurants WHERE name = (?)", (mes.getsender(),))
        result = c.fetchone()
        r_id = result[0]

        # get info from orders
        ne = "Making"
        c.execute("SELECT id, id_client, status, add_time FROM orders WHERE id_shop = (?) AND status = (?)", (r_id, ne))
        result2 = c.fetchall()
        context = []
        for line in result2:
            con = []
            id_order = line[0]
            c_id = line[1]
            add_time = line[3]

            c.execute("SELECT id_food, price, amount FROM order_info WHERE id_order = (?)",
                      (id_order,))
            result4 = c.fetchone()
            food_list = eval(result4[0])
            price = result4[1]
            amount = result4[2]

            # get client info
            c.execute("SELECT account, phone FROM users WHERE id = (?)",
                      (c_id,))
            result3 = c.fetchone()
            account = result3[0]
            phone = result3[1]

            # get food list
            f_list = []
            for g in food_list:
                g_s = re.split(r'\s?\*\s?', g)
                c.execute("SELECT name FROM food WHERE id = (?)", (int(g_s[0]),))
                result5 = c.fetchone()
                f_name = result5[0]
                f_l = f_name + "*" + g_s[1]
                f_list.append(f_l)

            f_str = str(f_list)

            par = [id_order, f_str, price, amount, account, phone, add_time]
            context.append(par)

        # return a message
        mes_rec = pickle.dumps(
            Message(mes.getsender(), Serverinfolist.order_status_info, context, True, Serverinfolist.Res))
        socket1.send(mes_rec)

    else:
        ids = mes.getcontent()
        ids_s = re.split(",", ids)
        n_status = "Completed"
        for idx in ids_s:
            c.execute("UPDATE orders SET status = (?) WHERE id = (?)", (n_status, int(idx)))
            conn.commit()
            c.execute("UPDATE order_info SET status = (?) WHERE id_order = (?)", (n_status, int(idx)))
            conn.commit()
        conn.close()

        # return a message
        mes_rec = pickle.dumps(Message(mes.getsender(), Serverinfolist.order_status_info, 1, True, Serverinfolist.Res))
        socket1.send(mes_rec)


def refund_handler(mes, socket1):
    # connect to db
    conn = sqlite3.connect("E:/csc3170/csc3170_project/food_order_system/database/csc3170.db")
    c = conn.cursor()
    attribute = mes.getcontent()
    # Get all refund order
    if mes.getcontent() == "Get refund order!":
        # get name of r_id
        c.execute("SELECT id FROM restaurants WHERE name = (?)", (mes.getsender(),))
        result = c.fetchone()
        r_id = result[0]

        # get info from orders
        c.execute("SELECT id, id_client, status, add_time FROM orders WHERE id_shop = (?)", (r_id,))
        result2 = c.fetchall()
        context = []
        for line in result2:
            con = []
            id_order = line[0]
            c_id = line[1]
            add_time = line[3]

            # check if it need refund
            print(id_order)
            st = "Wait for refunding!"
            c.execute("SELECT id, refund_reason FROM order_info WHERE status = (?) AND id_order=(?)", (st, id_order))
            final = c.fetchone()
            print(final)
            if final is None:
                continue

            refund_reason = final[1]
            c.execute("SELECT id_food, price, amount FROM order_info WHERE id_order = (?)",
                      (id_order,))
            result4 = c.fetchone()
            food_list = eval(result4[0])
            price = result4[1]
            amount = result4[2]

            # get client info
            c.execute("SELECT account, phone FROM users WHERE id = (?)",
                      (c_id,))
            result3 = c.fetchone()
            account = result3[0]
            phone = result3[1]

            # get food list
            f_list = []
            for g in food_list:
                g_s = re.split(r'\s?\*\s?', g)
                c.execute("SELECT name FROM food WHERE id = (?)", (int(g_s[0]),))
                result5 = c.fetchone()
                f_name = result5[0]
                f_l = f_name + "*" + g_s[1]
                f_list.append(f_l)

            f_str = str(f_list)

            par = [id_order, f_str, price, amount, account, phone, add_time, refund_reason]
            print(refund_reason)
            context.append(par)

        conn.close()

        # return a message
        mes_rec = pickle.dumps(
            Message(mes.getsender(), Serverinfolist.req_refund, context, True, Serverinfolist.Res))
        socket1.send(mes_rec)

    elif type(attribute) == list:
        print("Start to handle the status！")
        if attribute[1] == "1":
            n_status = "Refund"
            c.execute("UPDATE orders SET status = (?) WHERE id = (?)", (n_status, attribute[0]))
            c.execute("UPDATE order_info SET status = (?) WHERE id_order = (?)", (n_status, attribute[0]))
            c.execute("UPDATE order_info SET refund_result = (?) WHERE id_order = (?)", ("OK", attribute[0]))
            conn.commit()
            conn.close()
        elif attribute[1] == "2":
            c.execute("SELECT status, total_price,id_client FROM orders WHERE id = (?)", (attribute[0],))
            r = c.fetchone()
            print(r)
            n_status = r[0]
            total =r[1]
            c_id = r[2]
            c.execute("UPDATE users SET balance = balance + (?) WHERE account = (?)", (total, c_id))
            c.execute("UPDATE order_info SET status = (?) WHERE id_order = (?)", (n_status, attribute[0]))
            c.execute("UPDATE order_info SET refund_result = (?) WHERE id_order = (?)", ("Refused", attribute[0]))
            conn.commit()
            conn.close()
