# -*- coding: utf-8 -*
import sys
reload(sys)
sys.setdefaultencoding('utf8')

import os
import MySQLdb
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from textblob import TextBlob

def eachFile(sourcedirname):
    sourceFiles = []
    filelist = os.listdir(sourcedirname)
    for filename in filelist:
        sourcefile = os.path.join('%s%s' % (sourcedirname, filename))
        sourceFiles.append(sourcefile)
    return sourceFiles


all = []
lemmatizer = WordNetLemmatizer()
stopset = set(stopwords.words('english'))

def doLemmatize(source):

    file = open(source)
    try:
        raw = file.read()

        #使用textblob替代nltk
        textblob = TextBlob(raw)
        tokens = ''
        try:
            tokens = textblob.words
        except:
            print source
        #tokens = nltk.word_tokenize(raw)

        #1 lemmatization
        #ADJ, ADJ_SAT, ADV, NOUN, VERB = 'a', 's', 'r', 'n', 'v'

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

    finally:
         file.close()


if __name__ == '__main__':
    sourcedirname = "D:\pyworkspace\datafolder\corpora\ielts\ielts_articles\\"
    sourcelist = eachFile(sourcedirname)


    for source in sourcelist:
        doLemmatize(source)

    distinctAll = nltk.FreqDist(all).most_common()

    db = MySQLdb.connect('localhost', 'root', 'Password123', 'lexi_db', charset="utf8")
    cursor = db.cursor()

    #get similar words
    sql = "select id,word from wiki_word"
    cursor.execute(sql)
    rows = cursor.fetchall()

    for row in rows:
        word = row[1]
        for tuple in distinctAll:
            if tuple[0] == word:
                sql = "update wiki_word set ielts_freq = "+ str(tuple[1]) +" where id="+str(row[0])
                cursor.execute(sql)

    db.commit()
    cursor.close()
    db.close()