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
    wdict[w] = row[2]

