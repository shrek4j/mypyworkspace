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
    rows = getMorphemes()
    for row in rows:
        calculateScore(row)
        db.commit()


def calculateScore(row):
    totalLogFreq = 0
    wfdict = {}
    wfs = getWordFreqs(row[0])
    for wf in wfs:
        wfdict[wf[2]] = wf[1]
        swfs = getSimilarWordFreqs(wf[0])
        for swf in swfs:
            if wfdict.has_key(swf[2]):
                pass
            else:
                wfdict[swf[2]] = swf[1]

    for k in wfdict.keys():
        totalLogFreq += wfdict[k]

    updateFreqLevel(row[0],totalLogFreq)

def getMorphemes():
    sql = "select id,word_root from wiki_word_root"
    cursor.execute(sql)
    rows = cursor.fetchall()
    return rows

def getSimilarWordFreqs(wordId):
    sql = "SELECT ww.id,ww.log_freq,ww.word FROM wiki_word_rela wwrr LEFT JOIN wiki_word ww ON wwrr.similar_word_id = ww.id WHERE word_id = "+str(wordId)+" AND has_translation = 1"
    cursor.execute(sql)
    rows = cursor.fetchall()
    return rows

def getWordFreqs(wordRootId):
    sql = "SELECT ww.id,ww.log_freq,ww.word  FROM wiki_word_root_rela wwrr LEFT JOIN wiki_word ww ON wwrr.word_id = ww.id WHERE word_root_id = "+str(wordRootId)+" AND has_translation = 1"
    cursor.execute(sql)
    rows = cursor.fetchall()
    return rows

def updateFreqLevel(wordRootId,totalLogFreq):
    sql = "update wiki_word_root set total_log_freq = " + str(totalLogFreq) +" where id=" + str(wordRootId)
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