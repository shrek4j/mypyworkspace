# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf8')

from textblob import TextBlob,Word
from textblob.sentiments import NaiveBayesAnalyzer
import nltk

 #ADJ, ADJ_SAT, ADV, NOUN, VERB = 'a', 's', 'r', 'n', 'v'
def penn_to_wordnet(tag):
    """Converts a Penn corpus tag into a Wordnet tag."""
    if tag in ("NN", "NNS", "NNP", "NNPS"):
        return 'n'
    if tag in ("JJ", "JJR", "JJS"):
        return 'a' #adj
    if tag in ("VB", "VBD", "VBG", "VBN", "VBP", "VBZ"):
        return 'v'
    if tag in ("RB", "RBR", "RBS"):
        return 'r' #adv
    return None

title = "the old man and the sea"
file = open("C:\\Users\\Administrator\\Desktop\\myfolder\\corpora\\the-old-man-and-the-sea.txt")
text = file.read()

blob = TextBlob(text,analyzer=NaiveBayesAnalyzer())
#print blob.sentiment

adjlist = []
advlist = []
nounlist = []
verblist = []
for sentence in blob.sentences:
    wordtags = sentence.tags
    for wt in wordtags:
        w = Word(string=wt[0])
        pos=penn_to_wordnet(wt[1])
        lemma = w.lemmatize(pos)
        if pos == 'a':
            adjlist.append(lemma)
        if pos == 'r':
            advlist.append(lemma)
        if pos == 'n':
            nounlist.append(lemma)
        if pos == 'v':
            verblist.append(lemma)

adjfq = nltk.FreqDist(adjlist)
print "adj"
print len(adjlist)
print len(adjfq)
print adjfq.most_common()

advfq = nltk.FreqDist(advlist)
print "adv"
print len(advlist)
print len(advfq)
print advfq.most_common()

nounfq = nltk.FreqDist(nounlist)
print "noun"
print len(nounlist)
print len(nounfq)
print nounfq.most_common()

verbfq = nltk.FreqDist(verblist)
print "verb"
print len(verblist)
print len(verbfq)
print verbfq.most_common()
