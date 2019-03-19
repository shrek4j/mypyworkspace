# -*- coding: utf-8 -*
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import csv
import re


list = []
with open("C:\Users\Administrator\Desktop\words.csv") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        wordandfreq = row['words'].decode('GBK')
        arr = wordandfreq.split(" ")
        if len(arr)==2:
            word = arr[0]
            freq = int(arr[1])
            tup = (word,freq)
            list.append(tup)

list = sorted(list, key=lambda tup: tup[1],reverse=True)
for tup in list:
    print tup[0],tup[1]