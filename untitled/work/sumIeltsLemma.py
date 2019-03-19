# -*- coding: utf-8 -*
import sys
reload(sys)
sys.setdefaultencoding('utf8')

import os
import MySQLdb
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from textblob import TextBlob


if __name__ == '__main__':

    db = MySQLdb.connect('localhost', 'root', 'Password123', 'lexi_db', charset="utf8")
    cursor = db.cursor()
    try:
        sql = "SELECT wwr.word_id,SUM(ww.ielts_freq) all_ielts_freq FROM wiki_word_rela wwr LEFT JOIN wiki_word ww ON wwr.similar_word_id=ww.id GROUP BY wwr.word_id"
        cursor.execute(sql)
        rows = cursor.fetchall()

        for row in rows:
            if row[1]:
                sql = "update wiki_word set all_ielts_freq = "+ str(row[1]) +" where id="+str(row[0])
                cursor.execute(sql)

        db.commit()
    except:
        db.rollback()
    finally:
        cursor.close()
        db.close()