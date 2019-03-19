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


def grab_translation_and_save(id,word):
    req=urllib2.Request(url+word)
    req.add_header("User-Agent","Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0)")
    page = urllib2.urlopen(req).read()
    soup = BeautifulSoup(page, "html.parser")
    div = soup.select("#phrsListTab .trans-container")
    if len(div) == 0:
        updateTranslation(id,'')
        return

    ul = div[0].select("ul")
    text = ''
    for oneUl in ul:
        li = oneUl.select("li")
        for one in li:
            text += one.text.strip() + '<br/>'
    updateTranslation(id,text)


def updateTranslation(wordId,translation):
    try:
        if translation and translation != "":
            print wordId,translation
            sql = "update wiki_word set translation = '" + translation + "',has_translation=1 where id=" + str(wordId)
            cursor.execute(sql)
    except:
        pass

def handleWord(word):
    print word
    sql = "select id,has_translation from wiki_word where word='"+ word +"'"
    cursor.execute(sql)
    row = cursor.fetchone()
    if row:
        if row[1] == 1:
            return
        else:
           grab_translation_and_save(row[0],word)
    else:
        sql = "insert into wiki_word (word,source) values('" + word + "',1)"
        cursor.execute(sql)
        id = int(cursor.lastrowid)
        grab_translation_and_save(id,word)

def closeDb(cursor, db):
    if cursor:
        cursor.close()
    if db:
        db.close()

def checkExisted(handledWord):
    sql = "SELECT ww.word FROM wiki_word_ext_forms wwef LEFT JOIN wiki_word ww ON wwef.word_id=ww.id WHERE wwef.handled_word = '"+ handledWord +"'"
    cursor.execute(sql)
    row = cursor.fetchone()
    if row:
        return True
    else:
        return False

def updateHandledWord(handledWord,origWord):
    sql = "select id from wiki_word where word='"+ origWord +"'"
    cursor.execute(sql)
    row = cursor.fetchone()
    if row:
        id = row[0]
        sql = "insert into wiki_word_ext_forms (handled_word,word_id) values('" + handledWord + "',"+ str(id) +")"
        cursor.execute(sql)
    else:
        return

def grab_word_mission():
    newfilename = "C:\\Users\Administrator\\Desktop\youtube\\20180925\\HOW_TO_UNDERSTAND_YOUR_CAT_BETTER_English_handled.srt"
    file = open(newfilename)
    lines = file.read()
    all = lines.splitlines()
    stopset = set(stopwords.words('english'))

    wdset = set()
    reladict = {}
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
                if wd != token.lower():
                    reladict[token.lower()] = wd
    file.close()

    for wd in wdset:
        handleWord(wd)
    db.commit()


#do the mission
if __name__ == '__main__':
    try:
        grab_word_mission()
    finally:
        closeDb(cursor,db)
