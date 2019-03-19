# -*- coding: utf-8 -*
import sys
reload(sys)
sys.setdefaultencoding('utf8')

import re
import nltk
from nltk.corpus import gutenberg

file = open("C:\\Users\\Administrator\\Desktop\\myfolder\\corpora\\the-life-and-adventures-of-robinson-crusoe.txt")
raw = file.read()

#fd = nltk.FreqDist(ch.lower() for ch in raw if ch.isalpha())
#print fd.plot()

words = nltk.word_tokenize(raw)
cvs = [cv for w in words for cv in re.findall(r'[bcdfghjklmnpqrstvwxyz][aeiouy]', w)]
cfd = nltk.ConditionalFreqDist(cvs)
cfd.tabulate()
#cfd.plot()

cv_words = [(cv, w) for w in words for cv in re.findall(r'[bcdfghjklmnpqrstvwxyz][aeiouy]', w)]
cv_index = nltk.Index(cv_words)
print cv_index['wu']
