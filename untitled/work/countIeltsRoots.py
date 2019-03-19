# -*- coding: utf-8 -*
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import MySQLdb

db = MySQLdb.connect('localhost', 'root', 'Password123', 'lexi_db', charset="utf8")
cursor = db.cursor()

def doCount():
    file = open("C:\\Users\\Administrator\\Desktop\myfolder\\corpora\\stats\\ielts-7to11-words.txt")
    raw = file.read()

    words = raw.split(" ")

    count = 0
    for word in words:
        rows = tryGetWordRootFromDB(word)
        print word
        if rows:
            count += 1
            print rows
        print

    print len(words)
    print count

def tryGetWordRootFromDB(word):
    sql = "select www.id,www.word_root from wiki_word ww left join wiki_word_root_rela wrr on ww.id = wrr.word_id left join wiki_word_root www on wrr.word_root_id=www.id where word='" + word + "'"
    cursor.execute(sql)
    rows = cursor.fetchmany()
    return rows

def closeDb(cursor, db):
    if cursor:
        cursor.close()
    if db:
        db.close()

#do the mission
if __name__ == '__main__':
    try:
        doCount()
    finally:
        closeDb(cursor,db)