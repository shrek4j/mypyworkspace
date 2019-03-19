# -*- coding: utf-8 -*
import sys
reload(sys)
sys.setdefaultencoding('utf8')


from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import feature_extraction
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer

filenames = [
          'C:\\Users\\Administrator\\Desktop\\myfolder\\sea-and-adventures\\stats\\the-old-man-and-the-sea-words.txt',
          'C:\\Users\\Administrator\\Desktop\\myfolder\\sea-and-adventures\\stats\\the-life-and-adventures-of-robinson-crusoe-words.txt',
          'C:\\Users\\Administrator\\Desktop\\myfolder\\sea-and-adventures\\stats\\treasure-island-words.txt',
          'C:\\Users\\Administrator\\Desktop\\myfolder\\sea-and-adventures\\stats\\twenty-thousand-leagues-under-the-sea-words.txt'
        ]

corpus = []
for filename in filenames:
    file = open(filename)
    try:
        corpus.append(file.read())
    finally:
        file.close()

vectorizer=CountVectorizer(max_df=0.95, min_df=2,stop_words='english')#该类会将文本中的词语转换为词频矩阵，矩阵元素a[i][j] 表示j词在i类文本下的词频
transformer=TfidfTransformer()#该类会统计每个词语的tf-idf权值
tfidf=transformer.fit_transform(vectorizer.fit_transform(corpus))#第一个fit_transform是计算tf-idf，第二个fit_transform是将文本转为词频矩阵
word=vectorizer.get_feature_names()#获取词袋模型中的所有词语
weight=tfidf.toarray()#将tf-idf矩阵抽取出来，元素a[i][j]表示j词在i类文本中的tf-idf权重

docs = []
for i in range(len(weight)):#打印每类文本的tf-idf词语权重，第一个for遍历所有文本，第二个for便利某一类文本下的词语权重
    doc = []
    docs.append(doc)
    for j in range(len(word)):
        doc.append((word[j],weight[i][j]))

num = 0
for doc in docs:
    doc.sort(key=lambda x:x[1],reverse=True)
    newfilename = filenames[num][:-10] + "-weight-same-compare.txt"
    file = open(newfilename,'w')
    try:
        file.write(str(doc))
    finally:
        file.close()
    num +=1