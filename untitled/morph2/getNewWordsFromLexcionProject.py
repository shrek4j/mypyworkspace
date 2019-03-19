# -*- coding: utf-8 -*
import sys
reload(sys)
sys.setdefaultencoding('utf8')

import MySQLdb
import csv
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords

lemmatizer = WordNetLemmatizer()
db = MySQLdb.connect('localhost', 'root', 'Password123', 'lexi_db', charset="utf8")
cursor = db.cursor()

def searchWord(word):
    sql = "select id,word from wiki_word where word='"+word+"'"
    cursor.execute(sql)
    rows = cursor.fetchall()
    return rows


def closeDb(cursor, db):
    if cursor:
        cursor.close()
    if db:
        db.close()

#do the mission
if __name__ == '__main__':
    try:
        csv_reader = csv.reader(open('D:\\pyworkspace\\datafolder\\I142727.csv'))
        list = []
        total = 0
        added = 0
        isSkipped = False
        for row in csv_reader:
            if not isSkipped:
                isSkipped = True
                continue

            if int(row[2]) < 40:
                continue

            if "'" in row[0]:
                    continue

            total += 1
            w = row[0].lower()
            result = searchWord(w)
            if not result or len(result) == 0:
                tup = (w,int(row[2]))
                list.append(tup)
                added += 1

       # list = sorted(list, key=lambda tup: tup[1],reverse=True)
        #for tup in list:
         #   print tup[0],tup[1]

        #1 lemmatization
        #ADJ, ADJ_SAT, ADV, NOUN, VERB = 'a', 's', 'r', 'n', 'v'
        aggDict = {}
        stopset = set(stopwords.words('english'))
        for tup in list:
            word = tup[0]
            count = tup[1]
            origform = ""
            adjform = ""
            adtform = ""
            advform = ""
            nounform = ""
            verbform = ""
            otherform = ""
            if(word.isalpha()) and word.lower not in stopset:
                origform = word.lower()

                adjform = lemmatizer.lemmatize(word.lower(),'a')
                if adjform != origform and adjform not in stopset:
                    result = searchWord(adjform)
                    if not result or len(result) == 0:
                        if aggDict.get(adjform):
                            oldCount = aggDict[adjform]
                            aggDict[adjform] = int(oldCount) + int(count)
                        else:
                            aggDict[adjform] = int(count)
                    continue

                adtform = lemmatizer.lemmatize(word.lower(),'s')
                if adtform != origform and adtform not in stopset:
                    result = searchWord(adtform)
                    if not result or len(result) == 0:
                        if aggDict.get(adtform):
                            oldCount = aggDict[adtform]
                            aggDict[adtform] = int(oldCount) + int(count)
                        else:
                            aggDict[adtform] = int(count)
                    continue

                advform = lemmatizer.lemmatize(word.lower(),'r')
                if advform != origform and advform not in stopset:
                    result = searchWord(advform)
                    if not result or len(result) == 0:
                        if aggDict.get(advform):
                            oldCount = aggDict[advform]
                            aggDict[advform] = int(oldCount) + int(count)
                        else:
                            aggDict[advform] = int(count)
                    continue

                nounform = lemmatizer.lemmatize(word.lower(),'n')
                if nounform != origform and nounform not in stopset:
                    result = searchWord(nounform)
                    if not result or len(result) == 0:
                        if aggDict.get(nounform):
                            oldCount = aggDict[nounform]
                            aggDict[nounform] = int(oldCount) + int(count)
                        else:
                            aggDict[nounform] = int(count)
                    continue

                verbform = lemmatizer.lemmatize(word.lower(),'v')
                if verbform != origform and verbform not in stopset:
                    result = searchWord(verbform)
                    if not result or len(result) == 0:
                        if aggDict.get(verbform):
                            oldCount = aggDict[verbform]
                            aggDict[verbform] = int(oldCount) + int(count)
                        else:
                            aggDict[verbform] = int(count)
                    continue

                otherform = lemmatizer.lemmatize(word.lower())
                if otherform not in stopset:
                    result = searchWord(otherform)
                    if not result or len(result) == 0:
                        if aggDict.get(otherform):
                            oldCount = aggDict[otherform]
                            aggDict[otherform] = int(oldCount) + int(count)
                        else:
                            aggDict[otherform] = int(count)

        list1 = aggDict.items()
        list1 = sorted(list1, key=lambda tup: tup[1],reverse=True)
        for tup in list1:
            print tup[0],tup[1]

        print len(list)
        print len(list1)
    finally:
        closeDb(cursor,db)