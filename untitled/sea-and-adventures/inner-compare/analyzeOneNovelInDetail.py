import sys
reload(sys)
sys.setdefaultencoding('utf8')

import nltk
from nltk.text import  Text

file = open("C:\\Users\\Administrator\\Desktop\\myfolder\\sea-and-adventures\\the-old-man-and-the-sea.txt")
raw = file.read()
tokens = [w.lower() for w in nltk.word_tokenize(raw)]
fd = nltk.FreqDist(tokens)
text = Text(tokens)

weightfile = open("C:\\Users\\Administrator\\Desktop\\myfolder\\sea-and-adventures\\stats\\the-old-man-and-the-sea-3-weight.txt")
weightraw = weightfile.read()
words = [w2 for w in weightraw.split(',') for w2 in w.split('\n') if w2.isalpha()]

#text.dispersion_plot(words[:20])
text.dispersion_plot(words[:40])
#text.dispersion_plot(['father'])




#print fd.hapaxes()
#print sorted([w for w in set(fd) if len(w) > 7 and fd[w] > 7])