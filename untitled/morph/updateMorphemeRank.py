# -*- coding: utf-8 -*
import sys
reload(sys)
sys.setdefaultencoding('utf8')

import math
import time
import re
import MySQLdb
from urllib import urlopen
import urllib2
from bs4 import BeautifulSoup

db = MySQLdb.connect('localhost', 'root', 'Password123', 'lexi_db', charset="utf8")
cursor = db.cursor()

def grab_word_mission():
    rows = getMorphemeRanks()
    for row in rows:
        updateRank(row[0],row[1])
        db.commit()

def getMorphemeRanks():
    sql = "SELECT @rownum:=@rownum+1 rownum,t.id FROM (SELECT @rownum:=0,wiki_word_root.* FROM wiki_word_root ORDER BY total_log_freq DESC) t"
    cursor.execute(sql)
    rows = cursor.fetchall()
    return rows


def updateRank(rank,id):
    sql = "update wiki_word_root set rank = " + str(rank) +" where id=" + str(id)
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