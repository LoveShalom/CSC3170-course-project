"""
Time: 2024/11/7
Author: Deng Yifan
THis is the base of client platform. We will start to run the project in the file
"""

import pyautogui
import socket
import login_client as lg
import info_client
import order_client


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
            a1, ch = lg.login_page(socket_client)
            account = a1
            iflogin = True
            if ch == -1:
                ifquit = True
        else:
            print("-----------Welcome to CUHKSZ food order system!-----------")
            print("What do you want to do?")
            print("--1, Client Center")
            print("--2, Order Food")
            print("--3, Exit System")
            print("Please enter 1, 2 or 3 ")

            choice = int(input("Your choice:"))
            if choice == 1:
                pyautogui.hotkey("Alt", "c")
                # client center, show infor of client and user can modify personal information
                print("-------------------Hello, {}! Welcome back!-------------------".format(account))
                print("--1, Personal center")
                print("--2, Modify information")
                print("--3, Balance control")

                # make choice
                ch1 = input("Please enter:(1/2/3)")
                if ch1 == "1":
                    pyautogui.hotkey("Alt", "c")
                    if info_client.info_check(account, socket_client) == 0:  # The user want to return main page
                        pyautogui.hotkey("Alt", "c")
                        continue
                elif ch1 == "2":
                    a2 = info_client.modify_info(account, socket_client)  # The account will change if I do change on account
                    account = a2
                    print(account)
                    pyautogui.hotkey("Alt", "c")

                elif ch1 == "3":
                    info_client.balance(account, socket_client)
                    pyautogui.hotkey("Alt", "c")

            elif choice == 2:
                # order food, user can order food and see the status of order
                pyautogui.hotkey("Alt", "c")
                # client center, show infor of client and user can modify personal information
                print("-------------------Hello, {}!-------------------".format(account))
                print("--1, Recent Order")
                print("--2, Order Food")
                print("--3, Today's Order & Refund")

                # make choice
                ch2 = input("Please enter:(1/2/3)")
                if ch2 == "1":
                    pyautogui.hotkey("Alt", "c")
                    order_client.recent_order(account, socket_client)

                if ch2 == "2":
                    pyautogui.hotkey("Alt", "c")
                    order_client.make_order(account, socket_client)

                if ch2 == "3":
                    pyautogui.hotkey("Alt", "c")
                    order_client.today_order(account, socket_client)

            elif choice == 3:
                # exit system.
                ifquit = True
                pyautogui.hotkey("Alt", "c")
                print("-----------Goodbye!-----------")


if __name__ == '__main__':
    host = input("Please enter the host:")
    port = int(input("Please enter the port:"))
    main(host, port)
    # main("localhost",7777)
