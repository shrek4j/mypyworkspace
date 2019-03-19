# -*- coding: utf-8 -*
import sys
reload(sys)
sys.setdefaultencoding('utf8')

import MySQLdb
import csv

#db = MySQLdb.connect('101.201.109.96', 'bajiao_dev', '!@34QWerASdf', 'lexi_db', charset="utf8")
db = MySQLdb.connect('localhost', 'root', 'Password123', 'lexi_db', charset="utf8")
cursor = db.cursor()

def getAll():
    sql = "select id,`translation` from wiki_word"
    cursor.execute(sql)
    rows = cursor.fetchall()
    return rows

def addOne(id,trans_wx):
    sql = "insert into wiki_word_translations (word_id,`translation`) values("+str(id)+",'"+trans_wx+"')"
    cursor.execute(sql)

def closeDb(cursor, db):
    if cursor:
        cursor.close()
    if db:
        db.close()



#do the mission
if __name__ == '__main__':
    try:
        all = getAll()
        for one in all:
            trans = one[1]
            tranArr = trans.split('<br/>')
            if not tranArr:
                continue
            else:
                tranArr = tranArr[:-1]
                for tran in tranArr:
                    print str(one[0]),tran
                    addOne(one[0],tran)
        #commit all
        db.commit()
    finally:
        closeDb(cursor,db)