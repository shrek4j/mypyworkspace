# -*- coding: utf-8 -*
import sys
import MySQLdb

reload(sys)
sys.setdefaultencoding('utf8')


db = MySQLdb.connect('localhost', 'root', 'Password123', 'stock', charset="utf8")
cursor = db.cursor()

sql1 = "SELECT ts_code FROM ts_stock_list WHERE symbol LIKE '0%'"
cursor.execute(sql1)
stockCodes = cursor.fetchall()

piviList = []
pivdList = []
pdvdList = []
pdviList = []
piviCount = 0
pivdCount = 0
pdvdCount = 0
pdviCount = 0
total = 0

def showFreq(piviList):
    dictP = {}
    dictV = {}
    for i in range(len(piviList)):
        tup = piviList[i]
        if dictP.get(tup[0]):
            dictP[tup[0]] = dictP.get(tup[0])+1
            dictV[tup[0]] = dictV.get(tup[0])+tup[1]
        else:
            dictP[tup[0]] = 1
            dictV[tup[0]] = tup[1]

    for p in dictP:
        print "       平均震幅："+str(p)+"%,次数："+str(dictP[p])+"，成交量平均震幅："+str(round(dictV[p]*100/dictP[p]))+"%"
    print ""

for code in stockCodes:

    sql = "select trade_date,close_price,volume from ts_history_data_0 where stock_code = '" + code[0] + "' and trade_date > '20000000' order by trade_date asc"
    cursor.execute(sql)
    rows = cursor.fetchall()
    total += len(rows)
    for i in range(1,len(rows),1):
        if float(rows[i][2]) == 0.0 or float(rows[i-1][2]) == 0.0:
            continue
        if rows[i][1] > rows[i-1][1] and float(rows[i][2]) > float(rows[i-1][2]):
            piviPricePercent = round(((float(rows[i][1]) - float(rows[i-1][1]))/float(rows[i-1][1]))*100)
            if piviPricePercent > 10:
                continue
            piviVolumePercent = ((float(rows[i][2]) - float(rows[i-1][2]))/float(rows[i-1][2]))
            piviList.append((piviPricePercent,piviVolumePercent))
            piviCount += 1
        elif rows[i][1] < rows[i-1][1] and float(rows[i][2]) < float(rows[i-1][2]):
            piviPricePercent = round(((float(rows[i-1][1]) - float(rows[i][1]))/float(rows[i][1]))*100)
            if piviPricePercent > 10:
                continue
            piviVolumePercent = ((float(rows[i-1][2]) - float(rows[i][2]))/float(rows[i][2]))
            pdvdList.append((piviPricePercent,piviVolumePercent))
            pdvdCount += 1
        elif rows[i][1] > rows[i-1][1] and float(rows[i][2]) < float(rows[i-1][2]):
            piviPricePercent = round(((float(rows[i][1]) - float(rows[i-1][1]))/float(rows[i-1][1]))*100)
            if piviPricePercent > 10:
                continue
            piviVolumePercent = ((float(rows[i-1][2]) - float(rows[i][2]))/float(rows[i][2]))
            pivdList.append((piviPricePercent,piviVolumePercent))
            pivdCount += 1
        elif rows[i][1] < rows[i-1][1] and float(rows[i][2]) > float(rows[i-1][2]):
            piviPricePercent = round(((float(rows[i-1][1]) - float(rows[i][1]))/float(rows[i][1]))*100)
            if piviPricePercent > 10:
                continue
            piviVolumePercent = ((float(rows[i][2]) - float(rows[i-1][2]))/float(rows[i-1][2]))
            pdviList.append((piviPricePercent,piviVolumePercent))
            pdviCount += 1

print "交易日总数："+str(total)
print "本交易日与上一个交易日相比，价升同时量升："+str(piviCount)
showFreq(piviList)
print "本交易日与上一个交易日相比，价升同时量降："+str(pivdCount)
showFreq(pivdList)
print "本交易日与上一个交易日相比，价降同时量降："+str(pdvdCount)
showFreq(pdvdList)
print "本交易日与上一个交易日相比，价降同时量升："+str(pdviCount)
showFreq(pdviList)


if cursor:
    cursor.close()
if db:
    db.close()
