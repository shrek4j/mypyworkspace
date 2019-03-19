# -*- coding: utf-8 -*
import sys
reload(sys)
sys.setdefaultencoding('utf8')

import MySQLdb
import time
import json
import threading
from pyhessian.client import HessianProxy


STATE_NORMAL = 'normal'
#sunguoliang=18910528964
#zhangbinbin=15711107601
#chengxiaoyan=18612932300
fons = ["15718894135","18910528964","15711107601","18612932300"]

lastsend = {}

class MyThread(threading.Thread):

    def __init__(self):
        super(MyThread, self).__init__()

    def sendSms(self,service,content,job):
        if not lastsend.has_key(job):
            print content
            for fon in fons:
                data = {"msgTel" : fon, "msgContent" : content, "msgType" : "HOME"}
                dataJson = json.dumps(data)
                print service.sendMessage(dataJson)
        #already sent
        lastsend[job] = 1


    def run(self):
        service = HessianProxy("http://10.103.16.147:8081/hessian/smsSendService")
        for fon in fons:
            welcomeMsg = {"msgTel" : fon, "msgContent" : 'welcome, ACCOUNT job monitor is running.', "msgType" : "HOME"}
            welcomeJson = json.dumps(welcomeMsg)
            #inform that mission starts, inform only once
            service.sendMessage(welcomeJson)

        while True:
            #check job
            db = MySQLdb.connect('10.103.16.190', 'sf_quartz', 'X2qBcQ0oawr2', 'sf_quartz_db', charset="utf8")
            cursor = db.cursor()
            sql = "SELECT job_name,trigger_state FROM `ACCOUNT_TRIGGERS` WHERE trigger_state = 'BLOCKED' AND next_fire_time + 60*6*1000 < UNIX_TIMESTAMP(NOW())*1000"
            cursor.execute(sql)
            rows = cursor.fetchall()
            if rows:
                print "abnormal job detected!"
                try:
                    print rows
                except:
                    pass

                for row in rows:
                    msg = "job ["+row[0]+"] state is "+row[1]+",please recover it"
                    self.sendSms(service,msg,row[0])
            else:
                print "no abnormal job currently, rest for 5mins..."

            #rest for 6 mins
            time.sleep(60*6)

            #clear lastsend flag
            #1.delete lastsend value=0's key
            for key in lastsend.keys():
                if lastsend.get(key) == 0:
                    lastsend.pop(key)
            #2.set all value = 0
            for key in lastsend.keys():
                lastsend[key] = 0

            #clear db
            if cursor:
                cursor.close()
            if db:
                db.close()

if __name__ == '__main__':
        t = MyThread()
        t.start()
