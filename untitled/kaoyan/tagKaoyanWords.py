# -*- coding: utf-8 -*
import sys
reload(sys)
sys.setdefaultencoding('utf8')

import MySQLdb

db = MySQLdb.connect('localhost', 'root', 'Password123', 'lexi_db', charset="utf8")
cursor = db.cursor()

total = 0
file = open("C:\\Users\\Administrator\\Desktop\\kaoyan.txt")
lines = file.read()
all = lines.splitlines()
for line in all:
    sql = "select id from wiki_word where word='" + line + "'"
    cursor.execute(sql)
    rows = cursor.fetchone()
    if rows:
        print "update wiki_word set kaoyan_tag = 1 where word='" + line + "';"

if cursor:
    cursor.close()
if db:
    db.close()
