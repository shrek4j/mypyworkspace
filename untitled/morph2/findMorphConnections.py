# -*- coding: utf-8 -*
import sys
reload(sys)
sys.setdefaultencoding('utf8')

import re
import csv
import urllib2
import cookielib
from bs4 import BeautifulSoup

url = "http://www.youdict.com/root/search?wd="
cookie = cookielib.CookieJar()
handler=urllib2.HTTPCookieProcessor(cookie)
opener = urllib2.build_opener(handler)

csv_reader = csv.reader(open('C:\\Users\\Administrator\\Desktop\\raw_words.csv'))
for row in csv_reader:
    word = row[0]
    if len(word) < 4:
        continue
    req=urllib2.Request(url+word)
    print word
    req.add_header("User-Agent","Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0)")
    page = urllib2.urlopen(req).read()
    soup = BeautifulSoup(page, "html.parser")
    tags = soup.find_all(href=re.compile("\/root\/id\/"))

    if len(tags) > 3:
        continue
    for tag in soup.find_all(href=re.compile("\/root\/id\/")):
        print tag.parent