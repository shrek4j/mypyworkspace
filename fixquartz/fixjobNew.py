# -*- coding: utf-8 -*
import requests
import time
from bs4 import BeautifulSoup
import json

#new monitor system
count = 0
print "new job..."
while True:
    try:
        #login
        session = requests.session()
        #check HandleIndexMsgJob status
        resp = session.get('http://10.102.27.157:8080/quartzmgr/trigger/list?group=solr')
        soup = BeautifulSoup(resp.text, 'lxml')
        trs = soup.find_all('tr')
        for tr in trs:
            if tr.find_all('td') and tr.find_all('td')[0].text.strip() == 'HandleIndexMsgJob':
                #reset if nessessary
                status = tr.find_all('td')[2].text.strip()
                if status == 'BLOCKED':
                    resp = session.get('http://10.102.27.157:8080/quartzmgr/trigger/modifyQuartz?name=HandleIndexMsgJob&group=solr&cronExpression=0+0%2F1+*+*+*+%3F')
                    decode_json = json.loads(resp.content.decode('utf-8'))
                    message = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) + ' |  ' + status + '  |  operation resultCode: ' + str(decode_json['code'])
                    print message
                    count+=1
                    print "Blocked count:" + str(count)
                    url = "http://pushbear.ftqq.com/sub?sendkey=2748-604ec2ad00808e9ca4345f2682eef17f&" + "text="+ message +"&desp="+message
                   # requests.get(url)
                else:
                    message = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) + ' ' + status
                    print message
    except Exception as e:
        print time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) + ' operation failure, due to:'
        print e
    #sleep for half an hour
    time.sleep(60*5)