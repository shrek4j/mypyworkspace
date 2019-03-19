# -*- coding: utf-8 -*
import sys
reload(sys)
sys.setdefaultencoding('utf8')


from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import feature_extraction
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import NMF, LatentDirichletAllocation

n_features = 5000
n_topics = 10
n_top_words = 20

def print_top_words(model, feature_names, n_top_words):
    for topic_idx, topic in enumerate(model.components_):
        print("Topic #%d:" % topic_idx)
        print(" ".join([feature_names[i]
                        for i in topic.argsort()[:-n_top_words - 1:-1]]))
    print()


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

tf_vectorizer=CountVectorizer(max_df=0.95, min_df=2, max_features=n_features, stop_words='english')
tf=tf_vectorizer.fit_transform(corpus)
word=tf_vectorizer.get_feature_names()

tfidf_vectorizer = TfidfVectorizer(max_df=0.95, min_df=2, max_features=n_features, stop_words='english')
tfidf = tfidf_vectorizer.fit_transform(corpus)

nmf = NMF(n_components=n_topics, random_state=1, alpha=.1, l1_ratio=.5).fit(tfidf)
print_top_words(nmf, word, n_topics)
lda = LatentDirichletAllocation(n_topics=20, max_iter=5,
                                learning_method='online',
                                learning_offset=50.,
                                random_state=0)
lda.fit(tf)
print("\nTopics in LDA model:")
tf_feature_names = word
print_top_words(lda, tf_feature_names, n_top_words)




"""
##save in doc
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
"""