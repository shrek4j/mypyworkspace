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

# prepare data
csv_reader = csv.reader(open('D:\\pyworkspace\\datafolder\\I142727.csv'))
wdict = {}
for row in csv_reader:
    w = row[0].lower()
    morphCombo = row[4]
    morphIndent = re.findall(r'\{.*\}', morphCombo)

    for morph in morphIndent:
        if wdict.get(morph) == None:
            wset = set()
        else:
            wset = wdict.get(morph)
        wset.add(w)
        wdict[morph] = wset

for k in wdict.keys():
     if len(wdict[k])<2:
        wdict.pop(k)


db = MySQLdb.connect('localhost', 'root', 'Password123', 'lexi_db', charset="utf8")
cursor = db.cursor()

#get similar words
sql = "select id,word from wiki_word"
cursor.execute(sql)
rows = cursor.fetchall()

count = 0
for row in rows:
    wId = row[0]
    word = row[1]
    for k in wdict.keys():
        if word in wdict[k]:
            #save words and build connection
            for sw in wdict[k]:
                if "'" in sw:
                    continue
                #1.如果没有相似词，就添加
                sql = "select id from wiki_word where word='"+sw+"'"
                cursor.execute(sql)
                rows1 = cursor.fetchall()
                if len(rows1) < 1:
                    sql = "insert into wiki_word (word,is_similar) values('"+sw+"',1)"
                    cursor.execute(sql)

                #2.建立单词和相似词的关联
                sql = "select id from wiki_word where word='"+sw+"'"
                cursor.execute(sql)
                row1 = cursor.fetchone()
                sql = "insert into wiki_word_rela (word_id,similar_word_id) values("+str(wId)+","+str(row1[0])+")"
                cursor.execute(sql)

db.commit()
cursor.close()
db.close()

