# -*- coding: utf-8 -*
import matplotlib.pyplot as plt
import pandas as pd
from pandas import DataFrame
from datetime import datetime
from LivRule import LivRule
from LivSegList import LivSegList
import httplib
import json

def getStockHisRemotely(stock,queryStartDateStr,queryEndDateStr):
        url = "https://odin.bajiaoshan893.com/Stock/getStockHistoryDaily?stock="+stock+"&startDate="+queryStartDateStr+"&endDate="+queryEndDateStr
        conn = httplib.HTTPConnection("odin.bajiaoshan893.com")
        conn.request(method="GET",url=url)
        response = conn.getresponse()
        res= response.read()
        obj = json.loads(res).encode('utf-8')
        obj = json.loads(obj)
        return obj['dailyHis']

def getAllStocks():
    url = "https://odin.bajiaoshan893.com/Stock/getAllStocks"
    conn = httplib.HTTPConnection("odin.bajiaoshan893.com")
    conn.request(method="GET",url=url)
    response = conn.getresponse()
    res= response.read()
    obj = json.loads(res).encode('utf-8')
    obj = json.loads(obj)
    return obj['stockList']

def livermore(stock, showType, showPivot,startDateStr,endDateStr,queryStartDateStr,queryEndDateStr):
    startDate = datetime.strptime(startDateStr,'%Y%m%d')
    endDate = datetime.strptime(endDateStr,'%Y%m%d')
    highest = -1.00
    lowest = -1.00

    #query stock history data
    rows = getStockHisRemotely(stock,queryStartDateStr,queryEndDateStr)

    #generate
    livSegList = LivSegList()
    lastDate = datetime.strptime('19900101','%Y%m%d')
    for i in range(0, len(rows),1):
        close = float(rows[i]['close_price'])/100
        date = datetime.strptime(rows[i]['trade_date'],'%Y%m%d')
        if date >= startDate and date <= endDate:
            if highest == -1 and lowest == -1:
                highest = close
                lowest = close
            else:
                if close > highest:
                    highest = close
                if close < lowest:
                    lowest = close
        LivRule.doLivLogic(livSegList,close,date,lastDate)
        lastDate = date

    margin = (highest - lowest)*0.1
    highest += margin
    if lowest <= margin:
        lowest = 0
    else:
        lowest -= margin

    #draw
    fig = plt.figure()
    data = DataFrame({'date':livSegList.livSegAll.date, 'close':livSegList.livSegAll.close})
    if showType == 1:
        ax = fig.add_subplot(1,1,1)
    elif showType == 2:
        ax = fig.add_subplot(2,1,1)
        axOrig = fig.add_subplot(2,1,2)
        axOrig.plot(livSegList.livSegAll.date,livSegList.livSegAll.close,color='dimgrey')

    expl = []
    note = []
    for myLivSeg in livSegList.list:
        expl.append((myLivSeg.date[0],myLivSeg.type))
        color='green'
        if myLivSeg.type == 'ut':
            color='darkred'
        elif myLivSeg.type == 'nra' or myLivSeg.type == 'nf-nra':
            #color='orangered'
            color = 'dimgrey'
        elif myLivSeg.type == 'dt':
            color='green'
        elif myLivSeg.type == 'nre' or myLivSeg.type == 'nf-nre':
            #color='lightgreen'
            color = 'dimgrey'
        if len(myLivSeg.date) > 1:
            ax.plot(myLivSeg.date,myLivSeg.close,color=color)
        else:
            ax.scatter(myLivSeg.date[0],myLivSeg.close[0],color=color,linewidths=0.1)
        if myLivSeg.line != '':
            note.append((myLivSeg.date[-1],myLivSeg.line))

    if showPivot:
        ts = pd.Series(data['close'].values, index=data['date'])
        for ndate,nlabel in note:
            color='fuchsia'
            distance = -10
            if nlabel == 'red':
                color='blue'
                distance = 10
            ax.annotate('',xy=(ndate,ts.asof(ndate)+distance),
                        xytext=(ndate,ts.asof(ndate)+distance*1.2),
                        arrowprops=dict(arrowstyle="->",color=color))

    '''
    ts = pd.Series(data['close'].values, index=data['date'])
    for ndate,nlabel in expl:
        color='fuchsia'
        distance = -20
        if nlabel == 'red':
            color='blue'
            distance = 20
        ax.annotate(nlabel,xy=(ndate,ts.asof(ndate)+distance),
                    xytext=(ndate,ts.asof(ndate)+distance*1.2),
                    arrowprops=dict(arrowstyle="->",color=color))
    '''

    ax.set_xlim([startDate,endDate])
    ax.set_ylim([lowest, highest])
    if showType == 2:
        axOrig.set_xlim([startDate,endDate])
        axOrig.set_ylim([lowest, highest])

    '''
    ax.xaxis.set_major_locator(DayLocator(bymonthday=range(1,32), interval=15))
    ax.xaxis.set_major_formatter(DateFormatter("%Y-%m-%d"))
    for label in ax.xaxis.get_ticklabels():
       label.set_rotation(45)
    '''
    plt.show()

if __name__ == '__main__':
    livermore('000001.SZ',2,True,'20180424','20181024','20161024','20181024')