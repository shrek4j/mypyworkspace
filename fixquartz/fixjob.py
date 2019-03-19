# -*- coding: utf-8 -*
import requests
import time
from bs4 import BeautifulSoup
import json

count = 0
while True:
    try:
        #login
        headers = {'User-agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}
        login_url = 'http://soamonitor.sfbest.com/ServiceManagement/login.do?loginName=778732&loginPwd=111111'
        session = requests.session()
        session.post(login_url, headers=headers)
        #check HandleIndexMsgJob status
        resp = session.get('http://soamonitor.sfbest.com/ServiceManagement/quartz/triggerList.do?resId=177&page=1&pageSize=20&search_name=HandleIndexMsgJob&search_group=solr')
        soup = BeautifulSoup(resp.text, 'lxml')
        soup = soup.find_all('tr', attrs={'rel': 'name=HandleIndexMsgJob&group=solr'})[0]
        #reset if nessessary
        status = soup.find_all('td')[3].text.strip()
        if status == 'BLOCKED':
            resp = session.get('http://soamonitor.sfbest.com/ServiceManagement/quartz/edit.do?name=HandleIndexMsgJob&group=solr&cronExpression=0+0%2F2+*+*+*+%3F+')
            decode_json = json.loads(resp.content.decode('utf-8'))
            message = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) + ' |  ' + status + '  |  operation resultCode: ' + str(decode_json['statusCode'])
            print message
            count+=1
            print "Blocked count:" + str(count)
            url = "http://pushbear.ftqq.com/sub?sendkey=2748-604ec2ad00808e9ca4345f2682eef17f&" + "text="+ message +"&desp="+message
            requests.get(url)
        else:
            message = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) + ' ' + status
            print message
    except Exception as e:
        print time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) + ' operation failure, due to:'
        print e
    #sleep for half an hour
    time.sleep(60*30)