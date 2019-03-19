# -*- coding: utf-8 -*
import sys
reload(sys)
sys.setdefaultencoding('utf8')


from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import feature_extraction
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer

filenames = [
          'C:\\Users\\Administrator\\Desktop\\myfolder\\corpora\\stats\\a-tale-of-two-cities-words.txt',
          'C:\\Users\\Administrator\\Desktop\\myfolder\\corpora\\stats\\the-old-man-and-the-sea-words.txt',
          'C:\\Users\\Administrator\\Desktop\\myfolder\\corpora\\stats\\An-Inquiry-into-the-Nature-and-Causes-of-the-Wealth-of-Nations-words.txt',
          'C:\\Users\\Administrator\\Desktop\\myfolder\\corpora\\stats\\a-study-in-scarlet-words.txt',
          'C:\\Users\\Administrator\\Desktop\\myfolder\\corpora\\stats\\beowulf-words.txt',
          'C:\\Users\\Administrator\\Desktop\\myfolder\\corpora\\stats\\dracula-words.txt',
          'C:\\Users\\Administrator\\Desktop\\myfolder\\corpora\\stats\\great-expectations-words.txt',
          'C:\\Users\\Administrator\\Desktop\\myfolder\\corpora\\stats\\meditation-words.txt',
          'C:\\Users\\Administrator\\Desktop\\myfolder\\corpora\\stats\\metamorphosis-words.txt',
          'C:\\Users\\Administrator\\Desktop\\myfolder\\corpora\\stats\\odyssey-words.txt',
          'C:\\Users\\Administrator\\Desktop\\myfolder\\corpora\\stats\\on-the-origin-of-species-words.txt',
          'C:\\Users\\Administrator\\Desktop\\myfolder\\corpora\\stats\\pride-and-prejudice-words.txt',
          'C:\\Users\\Administrator\\Desktop\\myfolder\\corpora\\stats\\the-adventures-of-sherlock-holmes-words.txt',
          'C:\\Users\\Administrator\\Desktop\\myfolder\\corpora\\stats\\The-Canterbury-Tales-words.txt',
          'C:\\Users\\Administrator\\Desktop\\myfolder\\corpora\\stats\\the-complete-works-of-william-shakespeare-words.txt',
          'C:\\Users\\Administrator\\Desktop\\myfolder\\corpora\\stats\\the-hound-of-baskervilles-words.txt',
          'C:\\Users\\Administrator\\Desktop\\myfolder\\corpora\\stats\\the-king-james-bible-words.txt',
          'C:\\Users\\Administrator\\Desktop\\myfolder\\corpora\\stats\\the-life-and-adventures-of-robinson-crusoe-words.txt',
          'C:\\Users\\Administrator\\Desktop\\myfolder\\corpora\\stats\\the-memoirs-of-sherlock-holmes-words.txt',
          'C:\\Users\\Administrator\\Desktop\\myfolder\\corpora\\stats\\the-return-of-sherlock-holmes-words.txt',
          'C:\\Users\\Administrator\\Desktop\\myfolder\\corpora\\stats\\the-sign-of-four-words.txt',
          'C:\\Users\\Administrator\\Desktop\\myfolder\\corpora\\stats\\wuthering-heights-words.txt'
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
    newfilename = filenames[num][:-10] + "-weight.txt"
    file = open(newfilename,'w')
    try:
        file.write(str(doc))
    finally:
        file.close()
    num +=1