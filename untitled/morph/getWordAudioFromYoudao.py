import time
import re
import MySQLdb
from urllib import urlopen
import urllib
import urllib2
from bs4 import BeautifulSoup

db = MySQLdb.connect('localhost', 'root', 'Password123', 'lexi_db', charset="utf8")
cursor = db.cursor()

url = "https://dict.youdao.com/dictvoice?"
localDir = "F:\\odin\\audio\\"

def grab_word_mission():
    rows = getWords()
    for row in rows:
        grab_audio_and_save(row)
        db.commit()


def grab_audio_and_save(row):
    print row[0],row[1]
    if row[1].isalpha():
        try:
            urllib.urlretrieve(url+"audio="+row[1]+"&type=2", localDir+row[1]+".mp3")
        except:
            pass



def getWords():
    sql = "SELECT id,word FROM wiki_word WHERE word != '' and id>24683 ORDER BY id limit 0,999999"
    cursor.execute(sql)
    rows = cursor.fetchall()
    return rows


def closeDb(cursor, db):
    if cursor:
        cursor.close()
    if db:
        db.close()

#do the mission
if __name__ == '__main__':
    try:
        grab_word_mission()
    finally:
        closeDb(cursor,db)