import re
import time
import traceback
from urllib import urlopen
from bs4 import BeautifulSoup

import MySQLdb
import tushare as ts
#grab all stock history data and store them in separate table by their belongings

db = MySQLdb.connect('localhost', 'root', 'Password123', 'stock', charset="utf8")
cursor = db.cursor()
api = ts.pro_api('318937ff6bf3c29a921d03cf609ac255a4896ed2f03c47ea91a07bc0')

def handleOne(stock, year, sql):
    # data = ts.get_h_data(stock, autype='qfq', start=str(year)+'-01-01', end=str(year)+'-12-13',pause=1)
    #ts.set_token()

    data = ts.pro_bar(pro_api=api, ts_code=stock, adj='hfq', start_date=str(year)+'0101', end_date=str(year)+'1213')

    if not data.empty:  # means we have history data to grab
        for i in data.index:
            row = data.loc[i]
            params = (stock, row['trade_date'], int(float(row['open']) * 100),
                      int(float(row['high']) * 100), int(float(row['close']) * 100),
                      int(float(row['low']) * 100), row['vol'], 0)
            cursor.execute(sql, params)


def grabHistoryDataTask(stock):
    stockBelong = str(stock[0])[0]
    tableName = 'ts_history_data_' + stockBelong
    sql = "INSERT INTO " + tableName + " (stock_code, trade_date, open_price, highest_price,close_price, lowest_price, volume, amount) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"

    #year 1990-2015
    #season 1-4
    try:
        normalFinishFlag = True
        for year in range(int(str(stock[1])[0:4]), 2019):
           # time.sleep(0.5)  # lower visit frequency
            try:
                myPrint("handle year:" + str(year))
                handleOne(stock[0], year, sql)
            except Exception,e:
                print traceback.print_exc()
                normalFinishFlag = False
        if normalFinishFlag == True:
            db.commit()
            updateStatus(str(stock[0]))
        myPrint("handle stock:" + str(stock[0]) + " finished. normalFinishFlag:" + str(normalFinishFlag))
    except:
        pass


def getStockCodes():
    sql = "select ts_code,list_date from ts_stock_list where status = 0"
    cursor.execute(sql)
    rows = cursor.fetchall()
    return rows


def updateStatus(stock):
    try:
        sql = "update ts_stock_list set status = 1 where ts_code = '" + stock+"'"
        cursor.execute(sql)
        db.commit()
    except:
        myPrint("update "+stock+" status=1 failed")


def closeDb(cursor, db):
    if cursor:
        cursor.close()
    if db:
        db.close()

def myPrint(str):
    print str

if __name__ == '__main__':
    try:
        stockList = getStockCodes()
        for stock in stockList:
            myPrint('=======================')
            myPrint('handling ' + str(stockList.index(stock)) + '/' + str(len(stockList)) + ' stock:' + stock[0])
            grabHistoryDataTask(stock)
    finally:
        closeDb(cursor,db)
