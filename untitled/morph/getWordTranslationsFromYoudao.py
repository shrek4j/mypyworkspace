# -*- coding: utf-8 -*
import sys
reload(sys)
sys.setdefaultencoding('utf8')

import time
import re
import MySQLdb
from urllib import urlopen
import urllib2
from bs4 import BeautifulSoup

db = MySQLdb.connect('localhost', 'root', 'Password123', 'lexi_db', charset="utf8")
cursor = db.cursor()

url = "http://www.youdao.com/w/eng/"

def grab_word_mission():
    rows = getWords()
    for row in rows:
        grab_translation_and_save(row)
        db.commit()


def grab_translation_and_save(row):
    print row[1]
    req=urllib2.Request(url+row[1])
    req.add_header("User-Agent","Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0)")
    page = urllib2.urlopen(req).read()
    soup = BeautifulSoup(page, "html.parser")
    div = soup.select("#phrsListTab .trans-container")
    if len(div) == 0:
        updateTranslation(row[0],'')
        return

    ul = div[0].select("ul")
    text = ''
    for oneUl in ul:
        li = oneUl.select("li")
        for one in li:
            text += one.text.strip() + '<br/>'
    print text
    updateTranslation(row[0],text)



def getWords():
    sql = "select id,word from wiki_word where translation IS null and is_similar = 1"
    cursor.execute(sql)
    rows = cursor.fetchall()
    return rows

def updateTranslation(wordId,translation):
    sql = "update wiki_word set translation = '" + translation + "' where id=" + str(wordId)
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