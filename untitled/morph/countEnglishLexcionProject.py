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
wset = set()
lemmaset = set()
count = 0

for row in csv_reader:
    count+=1
    w = row[0].lower()
    wset.add(w)

    origform = w
    adjform = ""
    adtform = ""
    advform = ""
    nounform = ""
    verbform = ""
    otherform = ""

    adjform = lemmatizer.lemmatize(w,'a')
    if adjform != origform:
        lemmaset.add(adjform)
        continue

    adtform = lemmatizer.lemmatize(w,'s')
    if adtform != origform:
        lemmaset.add(adtform)
        continue

    advform = lemmatizer.lemmatize(w,'r')
    if advform != origform:
        lemmaset.add(advform)
        continue

    nounform = lemmatizer.lemmatize(w,'n')
    if nounform != origform:
        lemmaset.add(nounform)
        continue

    verbform = lemmatizer.lemmatize(w,'v')
    if verbform != origform:
        lemmaset.add(verbform)
        continue

    otherform = lemmatizer.lemmatize(w)
    lemmaset.add(otherform)

print count
print len(wset)
print len(lemmaset)
print lemmaset
