"""
Time: 2024/11/9
Author: Deng Yifan

This is main page of the use of canteen manager. The canteen manager mainly control the information of restaurant and
foods, And they should control the restaurants' information and can help client refunds and permit users to change
personal information......
"""
import pyautogui
import info_man
import login_man as lg
import socket

def main(host, port):
    ifquit = False
    iflogin = False
    m_id = ""
    # connect to socket
    socket_client = socket.socket()
    socket_client.connect((host, port))
    while not ifquit:  # since it is used by manager, it can connect to database directly
        if iflogin == False:
            m_id, ch = lg.login_page(socket_client)
            iflogin = True
            if ch == -1:
                ifquit = True
        else:

            # main page
            print("-----------Welcome back to the Canteen Management System.-----------")
            print("What do you want to do?")
            print("--1, Information Center")
            print("--2, Work-study students list")
            print("--3, Exit System")
            print("Please enter 1, 2 or 3")

            choice = int(input("Your choice:"))
            if choice == 1:
                pyautogui.hotkey("Alt", "c")
                # restaurant  center, show infor of restaurant and user can modify personal information
                print("-------------------Hello, manager! Welcome back!-------------------")
                print("--1, Restaurant information")
                print("--2, Food information")
                print("--3, Employees information")
                print("--4, Order information")
                print("--5, Managers information")

                # make choice
                ch1 = input("Please enter:(1/2/3/4/5)")
                if ch1 == "1":
                    pyautogui.hotkey("Alt", "c")
                    info_man.res_info(m_id, socket_client)   # The user want to return main page

                elif ch1 == "2":
                    pyautogui.hotkey("Alt", "c")
                    info_man.food_info(m_id, socket_client)  # The account will change if I do change on account
                    # print(account)

                elif ch1 == "3":
                    pyautogui.hotkey("Alt", "c")
                    info_man.em_info(m_id, socket_client)

                elif ch1 == "4":
                    pyautogui.hotkey("Alt", "c")
                    info_man.order_info(m_id, socket_client)

                elif ch1 == "5":
                    pyautogui.hotkey("Alt", "c")
                    info_man.managers_info(m_id, socket_client)

            elif choice == 2:
                # order food, user can order food and see the status of order
                print(2)
            elif choice == 3:
                # exit system.
                ifquit = True
                print("-----------Goodbye!-----------")


if __name__ == '__main__':
    host = input("Please enter the host:")
    port = int(input("Please enter the port:"))
    main(host, port)
    # main("localhost",7777)

