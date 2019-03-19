# -*- coding: utf-8 -*
import sys
reload(sys)
sys.setdefaultencoding('utf8')

import MySQLdb
import csv

db = MySQLdb.connect('localhost', 'root', 'Password123', 'gsearch_db', charset="utf8")
cursor = db.cursor()

def checkExists(word):
    sql = "select * from dic where name='"+word+"'"
    cursor.execute(sql)
    rows = cursor.fetchmany()
    return rows

def addword(word,type):
    sql = "insert into dic (name,type,remark) values('"+word+"',"+type+",'20170524')"
    cursor.execute(sql)

def closeDb(cursor, db):
    if cursor:
        cursor.close()
    if db:
        db.close()



#do the mission
if __name__ == '__main__':
    try:
        # prepare data
        csv_reader = csv.reader(open('C:\\Users\\Administrator\\Desktop\\words_utf8.csv'))

        for row in csv_reader:
            word = row[0]
            type = row[1]
            print word,type
            if not checkExists(word):
                addword(word,type)

        #commit all
        db.commit()
    finally:
        closeDb(cursor,db)