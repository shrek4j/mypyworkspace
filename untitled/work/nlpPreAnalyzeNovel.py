# -*- coding: utf-8 -*
import sys
reload(sys)
sys.setdefaultencoding('utf8')


import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.stem.lancaster import LancasterStemmer
from nltk.stem import PorterStemmer

from textblob import TextBlob

file = open("C:\\Users\\Administrator\\Desktop\\myfolder\\corpora\\the-old-man-and-the-sea.txt")
raw = file.read()
wordFile = open ("C:\\Users\\Administrator\\Desktop\\myfolder\\corpora\\stats\\the-old-man-and-the-sea-words.txt", 'w' )

lemmatizer = WordNetLemmatizer()
stopset = set(stopwords.words('english'))

try:
    #使用textblob替代nltk
    textblob = TextBlob(raw)
    tokens = textblob.words
    #tokens = nltk.word_tokenize(raw)

    #1 lemmatization
    #ADJ, ADJ_SAT, ADV, NOUN, VERB = 'a', 's', 'r', 'n', 'v'
    all = []
    for pos in tokens:
        origform = ""
        adjform = ""
        adtform = ""
        advform = ""
        nounform = ""
        verbform = ""
        otherform = ""
        if(pos.isalpha()) and pos.lower not in stopset:
            origform = pos.lower()

            adjform = lemmatizer.lemmatize(pos.lower(),'a')
            if adjform != origform and adjform not in stopset:
                all.append((adjform))
                continue

            adtform = lemmatizer.lemmatize(pos.lower(),'s')
            if adtform != origform and adtform not in stopset:
                all.append((adtform))
                continue

            advform = lemmatizer.lemmatize(pos.lower(),'r')
            if advform != origform and advform not in stopset:
                all.append((advform))
                continue

            nounform = lemmatizer.lemmatize(pos.lower(),'n')
            if nounform != origform and nounform not in stopset:
                all.append((nounform))
                continue

            verbform = lemmatizer.lemmatize(pos.lower(),'v')
            if verbform != origform and verbform not in stopset:
                all.append((verbform))
                continue

            otherform = lemmatizer.lemmatize(pos.lower())
            if otherform not in stopset:
                all.append((otherform))

    for word in all:
        wordFile.write (word + ' ')

    #distinctAll = nltk.FreqDist(all).most_common()
    #print distinctAll

finally:
     file.close()
     wordFile.close()
