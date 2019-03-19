# -*- coding: utf-8 -*
import sys
reload(sys)
sys.setdefaultencoding('utf8')


from Stemmer import Stemmer
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.stem import PorterStemmer
from nltk.stem import SnowballStemmer
from nltk.stem import ISRIStemmer
from nltk.stem import RSLPStemmer
from nltk.stem.lancaster import LancasterStemmer
from pyparsing import StringEnd, oneOf, FollowedBy, Optional, ZeroOrMore, SkipTo

file = open("C:\\Users\Administrator\\Desktop\\myfolder\\corpora\\stats\\ielts-7to11-some.txt")
raw = file.read()

try:
    wordlist = nltk.word_tokenize(raw)

    lemmatizer = WordNetLemmatizer()
    print lemmatizer.lemmatize("ran")
    lanster = LancasterStemmer()
    porter = PorterStemmer()
    snowball = SnowballStemmer("english")
    isri = ISRIStemmer()
    rslp = RSLPStemmer()
    porter2 = Stemmer('english')


    endOfString = StringEnd()
    prefix = oneOf("uni inter intro de con com anti pre pro per an ab ad af ac at as re in im ex en em un dis over sub syn out thermo philo geo for fore back")
    suffix = oneOf("ish")
    #suffix = oneOf("or er ed ish ian ary ation tion al ing ible able ate ly ment ism ous ness ent ic ive "
    #               "ative tude ence ance ise ant age cide ium ion")

    word = (Optional(prefix)("prefixes") +  SkipTo(suffix | suffix + FollowedBy(endOfString) | endOfString)("root") + ZeroOrMore(suffix | suffix + FollowedBy(endOfString))("suffix"))
    #word = (Optional(prefix)("prefixes") + SkipTo(FollowedBy(endOfString))("root"))


    for wd in wordlist:
        print wd
        stem = lanster.stem(wd)
        print "LansterStemmer:"+stem
        print "PorterStemmer2:"+porter2.stemWord(wd)
        #res = word.parseString(stem)
        #print res.dump()
        #print

finally:
    file.close()