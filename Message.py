"""
Time: 2024/11/15
Author: Deng Yifan

This is a class of message, contain message type, sender name, content, iflogin, user_type
"""


class Message:
    def __init__(self, sender, mes_type, content, loginsuccess, user_type):
        self.sender = sender # string
        self.mes_type = mes_type # message type in different cases
        self.content = content # message content
        self.loginsuccess= loginsuccess # whether already login
        self.user_type = user_type # user type

    def getsender(self):
        return self.sender

    def getmes_type(self):
        return self.mes_type

    def getcontent(self):
        return self.content

    def getloginsuccess(self):
        return self.loginsuccess

    def getuser_type(self):
        return self.user_type