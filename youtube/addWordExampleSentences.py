# -*- coding: utf-8 -*
import sys
import regex as re
import time
import re
import MySQLdb
from urllib import urlopen
import urllib2
from bs4 import BeautifulSoup
import nltk
from nltk.text import  Text
from textblob import TextBlob
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords

reload(sys)
sys.setdefaultencoding('utf8')

#db = MySQLdb.connect('localhost', 'root', 'Password123', 'lexi_db', charset="utf8")
db = MySQLdb.connect('101.201.109.96', 'bajiao_dev', '!@34QWerASdf', 'lexi_db', charset="utf8")
cursor = db.cursor()


url = "http://www.youdao.com/w/eng/"


def grab_example_sen(id,word):
    req=urllib2.Request(url+word)
    req.add_header("User-Agent","Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0)")
    page = urllib2.urlopen(req).read()
    soup = BeautifulSoup(page, "html.parser")
    div = soup.select("#bilingual")
    if len(div) == 0:
        return

    ulTags = div[0].select("ul")
    for ulTag in ulTags:
        liTags = ulTag.select("li")
        for liTag in liTags:
            engText = ""
            cnText = ""
            source = ""
            pTags = liTag.select("p")
            for i in range(len(pTags)):
                if i == 0:
                    spanTags = pTags[i].select('span')
                    for spanTag in spanTags:
                        engText += spanTag.text
                elif i == 1:
                    spanTags = pTags[i].select('span')
                    for spanTag in spanTags:
                        cnText += spanTag.text
                elif i == 2:
                    source = pTags[i].select('a')[0].text
            saveExampleSen(id,engText,cnText,source)


def saveExampleSen(wordId,engText,cnText,source):
    try:
        sql = 'insert into wiki_word_sen (word_id,sen_en,sen_cn,source) values('+ str(wordId) +',"' + engText + '","' + cnText + '","' + source +'")'
        print sql
        cursor.execute(sql)
        sql = "update wiki_word set sen_added=1 where id=" + str(wordId)
        cursor.execute(sql)
    except:
        pass

def handleWord(word):
    sql = "select id,sen_added from wiki_word where word='"+ word +"'"
    cursor.execute(sql)
    row = cursor.fetchone()
    if row and row[1] != 1:
        id = row[0]
        grab_example_sen(id,word)
    else:
        pass

def closeDb(cursor, db):
    if cursor:
        cursor.close()
    if db:
        db.close()



def grab_word_mission():
    newfilename = "C:\\Users\Administrator\\Desktop\youtube\\20180925\\HOW_TO_UNDERSTAND_YOUR_CAT_BETTER_English_handled.srt"
    file = open(newfilename)
    lines = file.read()
    all = lines.splitlines()
    stopset = set(stopwords.words('english'))

    wdset = set()
    for line in all:
        sen = line.split('||||')
        if not sen or len(sen) < 2:
            continue

        textblob = TextBlob(sen[1])
        tokens = textblob.words
        for token in tokens:
            if token.lower() not in stopset and token.isalpha():
                wd = token.lower()
                wdset.add(wd)
    file.close()

    count = 0
    for wd in wdset:
        count+=1
        print count
        handleWord(wd)
        db.commit()


#do the mission
if __name__ == '__main__':
    try:
        grab_word_mission()
    finally:
        closeDb(cursor,db)
