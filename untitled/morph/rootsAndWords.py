# -*- coding: utf-8 -*
import sys
reload(sys)
sys.setdefaultencoding('utf8')

import re
import MySQLdb
from urllib import urlopen
from bs4 import BeautifulSoup

db = MySQLdb.connect('localhost', 'root', 'Password123', 'lexi_db', charset="utf8")
cursor = db.cursor()

def grab_data_mission():

    #urls = ["https://en.wikipedia.org/wiki/List_of_Greek_and_Latin_roots_in_English/A-G"]
    #urls = ["https://en.wikipedia.org/wiki/List_of_Greek_and_Latin_roots_in_English/H-O"]
    urls = ["https://en.wikipedia.org/wiki/List_of_Greek_and_Latin_roots_in_English/P-Z"]

    for url in urls:
        grab_data_core(url)
        db.commit()


def grab_data_core(url):
    page = urlopen(url).read()
    soup = BeautifulSoup(page, "html.parser")
    tables = soup.select(".wikitable")
    print len(tables)
    for table in tables:
        trs = table.select("tr")
        for tr in trs:
            tds = tr.select("td")
            if len(tds) > 0:
                #extract prefix and word root
                root = re.sub(r'[^a-z,\-]*','',tds[0].text)
                print root
                if len(tds) < 2:
                    continue
                meaning = re.sub("'","",tds[1].text)
                origin = "0"
                if tds[2].text == "Latin":
                    origin = "1"
                if tds[2].text == "Greek":
                    origin = "2"
                # 3.将root保存到wiki_word_root中，返回主键
                wordRootId = addWordRoot(root, meaning, origin)
                if len(tds) < 5:
                    continue
                words = re.sub(' ','',tds[4].text)
                print words
                for word in words.split(','):
                    #1.判断word是否存在
                    wordId = tryGetWordId(word)
                    #2.不存在，添加到wiki_word表中，返回主键
                    if wordId:
                        wordIdInt = int(wordId[0])
                    #2.存在，返回主键
                    else:
                        wordIdInt = addWord(word)
                    #4.将word主键和word_root主键保存到wiki_word_root_rela中
                    addRela(wordIdInt,wordRootId)


def addRela(wordIdInt,wordRootId):
    sql = "insert into wiki_word_root_rela (word_id,word_root_id) values("+str(wordIdInt)+","+str(wordRootId)+")"
   # params = (wordIdInt,wordRootId)
    cursor.execute(sql)

def addWordRoot(root,meaning,origin):
    sql = "insert into wiki_word_root (word_root,meaning,origin) values('"+root+"','"+meaning+"','"+origin+"')"
    cursor.execute(sql)
    return int(cursor.lastrowid)

def addWord(word):
    sql = "insert into wiki_word (word) values('" + word + "')"
    cursor.execute(sql)
    return int(cursor.lastrowid)

def tryGetWordId(word):
    sql = "select id from wiki_word where word='" + word + "'"
    cursor.execute(sql)
    row = cursor.fetchone()
    return row

def closeDb(cursor, db):
    if cursor:
        cursor.close()
    if db:
        db.close()

#do the mission
if __name__ == '__main__':
    try:
        grab_data_mission()
    finally:
        closeDb(cursor,db)