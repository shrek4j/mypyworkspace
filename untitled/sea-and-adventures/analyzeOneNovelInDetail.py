# -*- coding: utf-8 -*
import sys
reload(sys)
sys.setdefaultencoding('utf8')

import nltk
from nltk.text import  Text
from textblob import TextBlob

#分析单词
def analyzeWords(tokens):
    lfdict = {}
    for t in tokens:
        t = t.lower()
        if  lfdict.has_key(len(t)):
            lfdict.get(len(t))[0].append(t)
            lfdict.get(len(t))[1].add(t)
        else:
            lflist = []
            lfset = set()
            lflist.append(t)
            lfset.add(t)
            lfdict[len(t)] = (lflist,lfset)

    tw = 0
    twd = 0
    items = lfdict.items()
    for item in items:
        tw+=len(item[1][0])
        twd+=len(item[1][1])
        print 'word len:'
        print item[0]
        print 'word count:'
        print len(item[1][0])
        print 'word distinct count:'
        print len(item[1][1])
        print 'word distinct:'
        print item[1][1]
        print

    print 'total word count:'+str(tw)
    print 'total word distinct count:'+str(twd)

#分析句子
def analyzeSents(sents):
    print 'total sentence count:'
    print len(sents)

    lfdict = {}
    for s in sents:
        wordcount = len(s.words)
        if  lfdict.has_key(wordcount):
            lfdict.get(wordcount).append(s.raw)
        else:
            lflist = []
            lflist.append(s.raw)
            lfdict[wordcount] = lflist

    tw = 0
    items = lfdict.items()
    list1 = []
    for item in items:
        tw+=len(item[1])
        print 'sentence word count:'
        print item[0]
        print 'sentence count:'
        print len(item[1])
        print 'sentence list:'
        print item[1]
        print
        list1.append("{value:"+str(len(item[1]))+",name:'句长"+str(item[0])+"'}")

    print list1

file = open("D:\\pyworkspace\\datafolder\\sea-and-adventures\\the-old-man-and-the-sea.txt")
raw = file.read()

textblob = TextBlob(raw)

tokens = textblob.words
analyzeWords(tokens)

sents = textblob.sentences
analyzeSents(sents)



text = Text(tokens)
#text.collocations(num=30,window_size=3)
'''
bgrams = nltk.bigrams(text)
bgfdist = nltk.FreqDist(list(bgrams))
print [t for t in bgfdist.most_common() if t[0][0].isalpha() and t[0][1].isalpha()]
trigrams = nltk.trigrams(text)
tgfdist = nltk.FreqDist(list(trigrams))
print [t for t in tgfdist.most_common() if t[0][0].isalpha() and t[0][1].isalpha() and t[0][2].isalpha()]
'''

#text.concordance(word='shoulder',width=200,lines=75)



#weightfile = open("D:\\pyworkspace\\datafolder\\corpora\\stats\\the-old-man-and-the-sea-weight.txt")
#weightraw = weightfile.read()
#words = [w2 for w in weightraw.split(',') for w2 in w.split('\n') if w2.isalpha()]
'''
words = [
    'bait','fish','sardine','shark','dolphin','cramp','fin','turtle','tail','jaw',
    'harpoon','knife',
    'sail','hit','jump','swim','big','circle',
    'fisherman','oar','skiff','boat','hook','tiller','coil','stern','bow','mast',
    'slowly','aloud','slant',
    'sun','breeze','shoulder','sea','ocean','club',
    'maybe','dream'
]
'''
words = [
    'bait','fish','shark','dolphin',
    'harpoon','knife',
    'hit','big','circle',
    'oar','skiff'
]
#text.dispersion_plot(words[:20])
text.dispersion_plot(words)
#text.dispersion_plot(['father'])


#print fd.hapaxes()
#print sorted([w for w in set(fd) if len(w) > 7 and fd[w] > 7])

