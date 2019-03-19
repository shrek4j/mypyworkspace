# -*- coding: utf-8 -*
#coding=utf8
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import itchat

itchat.auto_login(hotReload=True)

def send(mymsg,receiver):
    if not receiver:
        uid = 'filehelper'
    if receiver == "her":
        uid = "宝宝,小nun nun,小推子,白揪兔"
    else:
        name = itchat.search_friends(name=receiver)
        uid = name[0]["UserName"]
    itchat.send(mymsg, uid)

if __name__ == '__main__':
    send("宝宝，今天晚上吃什么呀？","her")