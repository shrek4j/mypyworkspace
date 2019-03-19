# -*- coding: utf-8 -*
import sys
reload(sys)
sys.setdefaultencoding('utf8')

import time
import re
import MySQLdb
from urllib import urlopen
import urllib2
import cookielib
from bs4 import BeautifulSoup

db = MySQLdb.connect('localhost', 'root', 'Password123', 'lexi_db', charset="utf8")
cursor = db.cursor()

#url = "https://translate.google.cn/#en/zh-CN/"
url = "http://fanyi.baidu.com/translate?aldtype=16047&query=&keyfrom=baidu&smartresult=dict&lang=auto2zh#en/zh/"
cookie = cookielib.CookieJar()
handler=urllib2.HTTPCookieProcessor(cookie)
opener = urllib2.build_opener(handler)

def grab_word_mission():
    rows = getWordRoots()
    for row in rows:
        grab_translation_and_save(row)
        db.commit()


def grab_translation_and_save(row):
    print row[1]
    req = opener.open(url+row[1])

    #req=urllib2.Request(url+row[1])
    req.add_header("User-Agent","Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0)")
    page = urllib2.urlopen(req).read()
    soup = BeautifulSoup(page, "html.parser")
    span = soup.select(".ordinary-output .target-output .clearfix")
    print span
    #updateTranslation(row[0],text)



def getWordRoots():
    sql = "select id,meaning from wiki_word_root where meaning_cn IS null"
    cursor.execute(sql)
    rows = cursor.fetchall()
    return rows

def updateTranslation(wordRootId,translation):
    sql = "update wiki_word_root set meaning_cn = '" + translation + "' where id=" + str(wordRootId)
    cursor.execute(sql)


def closeDb(cursor, db):
    if cursor:
        cursor.close()
    if db:
        db.close()

#do the mission
if __name__ == '__main__':
    try:
        grab_word_mission()
    finally:
        closeDb(cursor,db)

#UPDATE wiki_word SET has_translation = 1 WHERE translation NOT LIKE ''
#UPDATE wiki_word SET has_translation = 0 WHERE translation LIKE ''