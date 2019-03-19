import sys
reload(sys)
sys.setdefaultencoding('utf8')

from textblob import TextBlob
#26780 the old man and the sea

file = open("C:\\Users\\Administrator\\Desktop\\myfolder\\sea-and-adventures\\the-old-man-and-the-sea.txt")
raw = file.read()
text = TextBlob(raw)
tokens = text.words
print len(tokens)
