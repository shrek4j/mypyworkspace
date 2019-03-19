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
    morphCombo = row[4]
    morphIndent = re.sub(r'[^a-z]+',' ', morphCombo)

    if morphIndent[0:1] == ' ':
        morphIndent = morphIndent[1:]
    if morphIndent[-1:] == ' ':
        morphIndent = morphIndent[:-1]

    morphList = re.split(r'\s',morphIndent)
    for morph in morphList:
        if wdict.get(morph) == None:
            wset = set()
        else:
            wset = wdict.get(morph)
        wset.add(w)
        wdict[morph] = wset

db = MySQLdb.connect('localhost', 'root', 'Password123', 'lexi_db', charset="utf8")
cursor = db.cursor()
sql = "select id,word_root from wiki_word_root"
cursor.execute(sql)
rows = cursor.fetchall()


for row in rows:
    id = row[0]
    root = re.sub(r'\-','', row[1])
    if ',' in root:
        rootlist = re.split(r',',root)
        for root1 in rootlist:
            if wdict.has_key(root1):
                print root1
    else:
        if wdict.has_key(root):
            print root

cursor.close()
db.close()

'''
list = sorted(wdict.items(), key=lambda d: len(d[1]),reverse = True)

print len(list)

for item in list:
    print item[0],len(item[1])
'''