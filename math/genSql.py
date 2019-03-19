# -*- coding: utf-8 -*
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import csv
import MySQLdb

#db = MySQLdb.connect('localhost', 'root', 'Password123', 'lexi_db', charset="utf8")
db = MySQLdb.connect('101.201.109.96', 'bajiao_dev', '!@34QWerASdf', 'lexi_db', charset="utf8")
cursor = db.cursor()

def checkExits(word_id,word_root_id):
    sql = "select id from wiki_word_root_rela where word_id="+word_id+" and word_root_id="+word_root_id
    cursor.execute(sql)
    row = cursor.fetchone()
    return row

def getWordId(word):
    sql = "SELECT id FROM wiki_word WHERE word = '" + word +"'"
    cursor.execute(sql)
    row = cursor.fetchone()
    return row[0]

with open("F:\odin\learn top100-200.csv") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
       # word_id = row['word_id']
        word_id = str(getWordId(row['word']))
        word_root_ids_str = row['word_root_id']
        learn = row['learn_by_root'].decode('GBK')

        if learn and learn != '':
            print "UPDATE wiki_word SET learn_by_root='"+learn+"' WHERE id="+word_id+";"

        if word_root_ids_str and word_root_ids_str != '':
            word_root_ids = row['word_root_id'].split('|')
            if len(word_root_ids) > 0:
                for word_root_id in word_root_ids:
                    if not checkExits(word_id,word_root_id):
                        print "INSERT INTO wiki_word_root_rela(word_id,word_root_id) VALUES("+word_id+","+word_root_id+");"


