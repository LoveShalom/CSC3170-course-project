"""
Date: 2024/11/14
Author: Deng Yifan

This is the server for the whole program, it will be used to handle the message among restaurant, client and manager.
"""

import socket
import threading
import Serverinfolist
import ClientThread
import ResThread
import ManaThread
import Message
import pickle


def create_server_socket(host, port):
    socket_server = socket.socket()
    socket_server.bind((host, port))
    socket_server.listen()
    print("The server start now with host{} and port{}".format(host,port))
    print("Waiting for connection...")
    # start multi_threading
    num = 0  # the id of client
    while True:
        num += 1
        conn, address = socket_server.accept()
        print("client id{}，client info：{}".format(num,address))
        client_handler = threading.Thread(target=handle_client, args=(conn, address, num))
        client_handler.start()


# handle threading and modify class
def handle_client(conn, address, num):
    while True:
        # receive class info
        data_from_client = conn.recv(4096)
        mes = pickle.loads(data_from_client)
        print(mes.getcontent())
        print("data from client is {}".format(mes))
        print("client port {}:{}send a message which is ：{}".format(num, address, mes))

        # make class
        if mes.getuser_type() == Serverinfolist.Cli:
            print("a client connect to server")
            ClientThread.ClientThread(mes,conn)

        if mes.getuser_type() == Serverinfolist.Res:
            print("a restaurant connect to server")
            ResThread.ResThread(mes, conn)

        if mes.getuser_type() == Serverinfolist.Man:
            print("a manager connect to server")
            print("data from client is {}".format(mes))
            ManaThread.ManaThread(mes, conn)

        if mes.getuser_type() == Serverinfolist.exit_mes:
            print("Client {} will exit the system".format(mes.getsender()))
            break

    conn.close()


if __name__ == '__main__':
    host = input("Please enter the host:")
    port = int(input("Please enter the port:"))
    create_server_socket(host, port)
    # create_server_socket("localhost", 7777)