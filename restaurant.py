"""
Time: 2024/11/7
Author: Deng Yifan
THis is the base of restaurant platform. We will start to run the project in the file
"""

import pyautogui
import socket
import login_res as lg
import info_res
import info_employees
import order_res


def main(host, port):
    # some variable
    ifquit = False
    iflogin = False
    account = ""

    # connect to socket
    socket_client = socket.socket()
    socket_client.connect((host, port))

    while not ifquit:
        if iflogin == False:
            account, ch = lg.login_page(socket_client)
            iflogin = True
            if ch == -1:
                ifquit = True
        else:
            # print(account)
            print("-----------Welcome to CUHKSZ food order system!-----------")
            print("What do you want to do?")
            print("--1, Restaurant Center")
            print("--2, Employees center")
            print("--3, Orders center")
            print("--4, Exit System")
            print("Please enter 1, 2, 3 or 4")

            choice = int(input("Your choice:"))
            if choice == 1:
                pyautogui.hotkey("Alt", "c")
                # restaurant  center, show infor of restaurant and user can modify personal information
                print("-------------------Hello, {}! Welcome back!-------------------".format(account))
                print("--1, Restaurant information")
                print("--2, Modify information")
                print("--3, Food information")
                print("--4, Food Modify")

                # make choice
                ch1 = input("Please enter:(1/2/3/4)")
                if ch1 == "1":
                    pyautogui.hotkey("Alt", "c")
                    if info_res.info_check(account, socket_client) == 0:  # The user want to return main page
                        pyautogui.hotkey("Alt", "c")
                        continue
                elif ch1 == "2":
                    account = info_res.modify_info(account, socket_client)  # The account will change if I do change on account
                    # print(account)
                    pyautogui.hotkey("Alt", "c")

                elif ch1 == "3":
                    info_res.food_info(account, socket_client)
                    pyautogui.hotkey("Alt", "c")

                elif ch1 == "4":
                    info_res.modify_food(account, socket_client)
                    pyautogui.hotkey("Alt", "c")

            elif choice == 2:
                # Show info of Employees and can modify
                pyautogui.hotkey("Alt", "c")
                print("---------------Employees center---------------")
                print("--1, Employees list")
                print("--2, Add new Employees")
                print("--3, Delete Employees")
                print("--4, Modify Employees")

                ch2 = input("Please enter:(1/2/3/4)")
                if ch2 == "1":
                    pyautogui.hotkey("Alt", "c")
                    info_employees.employees_list(account, socket_client)
                # print(2)
                if ch2 == "2":
                    pyautogui.hotkey("Alt", "c")
                    info_employees.employees_add(account, socket_client)
                if ch2 == "3":
                    pyautogui.hotkey("Alt", "c")
                    info_employees.employees_delete(account, socket_client)
                if ch2 == "4":
                    pyautogui.hotkey("Alt", "c")
                    info_employees.employees_modify(account, socket_client)

            elif choice == 3:
                # recent order, user can see the recent order history
                pyautogui.hotkey("Alt", "c")
                print("---------------Order center---------------")
                print("--1, Uncompleted Orders")
                print("--2, Recent Orders")
                print("--3, Refund handler")

                ch2 = input("Please enter:(1/2/3)")
                if ch2 == "1":
                    pyautogui.hotkey("Alt", "c")
                    order_res.orders(account, socket_client)
                # print(2)
                if ch2 == "2":
                    pyautogui.hotkey("Alt", "c")
                    order_res.recent_order(account, socket_client)

                if ch2 == "3":
                    pyautogui.hotkey("Alt", "c")
                    order_res.refund_controler(account,socket_client)
            elif choice == 4:
                # exit system.
                ifquit = True
                pyautogui.hotkey("Alt", "c")
                print("-----------Goodbye!-----------")


if __name__ == '__main__':
    host = input("Please enter the host:")
    port = int(input("Please enter the port:"))
    main(host, port)
    # main("localhost",7777)
