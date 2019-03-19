# -*- coding: utf-8 -*
import sys
reload(sys)
sys.setdefaultencoding('utf8')

import os
import MySQLdb
import urllib2
from bs4 import BeautifulSoup

prefix = "https://www.shanbay.com"
suffixs = []
total = 0

req=urllib2.Request("https://www.shanbay.com/wordbook/34/")
req.add_header("User-Agent","Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0)")
page = urllib2.urlopen(req).read()
soup = BeautifulSoup(page, "html.parser")
tds = soup.select(".wordbook-wordlist-name a")
for td in tds:
    suffixs.append(td.attrs.get('href'))

for suffix in suffixs:
    count = 1
    while True:
        url = prefix + suffix + "?page="+ str(count)
        count += 1
        req=urllib2.Request(url)
        req.add_header("User-Agent","Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0)")
        page = urllib2.urlopen(req).read()
        soup = BeautifulSoup(page, "html.parser")
        strongs = soup.select("tr .span2 strong")
        if not strongs:
            count = 0
            break
        for strong in strongs:
            print strong.text
            total += 1

print total