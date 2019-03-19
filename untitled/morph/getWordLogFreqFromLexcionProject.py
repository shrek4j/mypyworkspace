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

import csv
from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()
csv_reader = csv.reader(open('D:\\pyworkspace\\datafolder\\I142727.csv'))
wdict = {}
for row in csv_reader:
    w = row[0].lower()
    wdict[w] = row[3]


db = MySQLdb.connect('localhost', 'root', 'Password123', 'lexi_db', charset="utf8")
cursor = db.cursor()


def grab_word_mission():
    rows = getWords()
    for row in rows:
        grab_log_freq_and_save(row)
    db.commit()


def grab_log_freq_and_save(row):
    freq = wdict.get(row[1])
    if freq == None:
        freq = '0'
    print row[0],row[1],freq
    updateFreq(row[0],freq)



def getWords():
    sql = "select id,word from wiki_word where is_similar=1"
    cursor.execute(sql)
    rows = cursor.fetchall()
    return rows

def updateFreq(wordId,freq):
    sql = "update wiki_word set log_freq = " + freq + " where id=" + str(wordId)
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