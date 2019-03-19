# -*- coding: utf-8 -*
import sys
reload(sys)
sys.setdefaultencoding('utf8')


file = open("C:\\Users\\Administrator\\Desktop\\timeSpent.txt")
line = file.readline()

dict = {}
while line:
    info = line.split("|")
    if len(info) == 3:
        time =  int(info[2])
        if time > 3000:
            ip = info[0]
            date = info[1]
            print ip,date,time
            t = (date,time)
            if dict.has_key(ip):
                dict[ip].append(t)
            else:
                list = [t]
                dict[ip] = list
    line = file.readline()

print dict