# -*- coding: utf-8 -*
import sys
reload(sys)
sys.setdefaultencoding('utf8')

import os
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from textblob import TextBlob

sourcedirname = "C:\\Users\\Administrator\\Desktop\\myfolder\\corpora\\ielts\\ielts_articles\\"
destdirname = "C:\\Users\\Administrator\\Desktop\\myfolder\\corpora\\ielts\\ielts_articles\\stats\\"

def eachFile(sourcedirname,destdirname):
    sourceFiles = []
    destFiles = []
    filelist =  os.listdir(sourcedirname)
    for filename in filelist:
        sourcefile = os.path.join('%s%s' % (sourcedirname, filename))
        destfile = os.path.join('%s%s' % (destdirname, filename[:-4] + "-freq.txt"))
        sourceFiles.append(sourcefile)
        destFiles.append(destfile)
    print sourceFiles
    print destFiles
    return (sourceFiles,destFiles)


def doLemmatize(source,dest):
    file = open(source)
    writeFile = open(dest,'w')
    lemmatizer = WordNetLemmatizer()
    stopset = set(stopwords.words('english'))

    try:
        raw = file.read()

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

       # for word in all:
        #    writeFile.write (word + ' ')

        distinctAll = nltk.FreqDist(all).most_common()
        writeFile.write(str(distinctAll))

    finally:
         file.close()
         writeFile.close()


if __name__ == '__main__':
    tupleFile = eachFile(sourcedirname,destdirname)
    sourcelist = tupleFile[0]
    destlist = tupleFile[1]

    num = 0
    for source in sourcelist:
        dest = destlist[num]
        doLemmatize(source,dest)
        num+=1
