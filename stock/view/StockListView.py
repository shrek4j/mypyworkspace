# -*- coding: utf-8 -*
import sys

from matplotlib import dates
from matplotlib.dates import WeekdayLocator, MONDAY, DateFormatter

reload(sys)
sys.setdefaultencoding('utf8')

from Tkinter import *
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.ticker import MultipleLocator
from pandas import DataFrame
from datetime import datetime
from controller.LivRule import LivRule
from controller.LivSegList import LivSegList
from util.MultiListbox import MultiListbox
import httplib
import json
import matplotlib.finance as mpl_finance

class Application(Frame):

    def draw(self):
        stock = self.t1.get()
        showType = self.rb1.get()
        showPivot = False
        if self.rb2.get() == 1:
            showPivot = True
        colorType = self.rb3.get()
        startDateStr = self.t2.get()
        endDateStr = self.t3.get()
        queryStartDateStr = self.t4.get()
        queryEndDateStr = self.t5.get()
        self.dolivermore(stock,showType,showPivot,colorType,startDateStr,endDateStr,queryStartDateStr,queryEndDateStr)

    def dictToSeq(self,dicts):
        seqs = []
        for dict in dicts:
            seq = (dates.date2num(datetime.strptime(dict['trade_date'],'%Y%m%d')),float(dict['open_price'])/100,float(dict['highest_price'])/100,float(dict['lowest_price'])/100,float(dict['close_price'])/100)
            seqs.append(seq)
        return seqs

    def dolivermore(self,stock, showType, showPivot,colorType,startDateStr,endDateStr,queryStartDateStr,queryEndDateStr):
        startDate = datetime.strptime(startDateStr,'%Y%m%d')
        endDate = datetime.strptime(endDateStr,'%Y%m%d')
        highest = -1.00
        lowest = -1.00

        #query stock history data
        rows = self.getStockHisRemotely(stock,queryStartDateStr,queryEndDateStr)

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
        elif showType == 3:
            ax = fig.add_subplot(2,1,1)
            axK = fig.add_subplot(2,1,2)
            mpl_finance.candlestick_ohlc(axK,self.dictToSeq(rows),width=0.5,colorup='r',colordown='green')

        note = []
        for myLivSeg in livSegList.list:
            color='green'
            if myLivSeg.type == 'ut':
                color='darkred'
            elif myLivSeg.type == 'nra' or myLivSeg.type == 'nf-nra':
                color='orangered'
                if colorType == 4:
                    color='lightgray'
            elif myLivSeg.type == 'dt':
                color='forestgreen'
            elif myLivSeg.type == 'nre' or myLivSeg.type == 'nf-nre':
                color='lightgreen'
                if colorType == 4:
                    color='lightgray'
            if len(myLivSeg.date) > 1:
                ax.plot(myLivSeg.date,myLivSeg.close,color=color)
            else:
                ax.scatter(myLivSeg.date[0],myLivSeg.close[0],color=color,linewidths=0.1)
            if myLivSeg.line != '':
                note.append((myLivSeg.date[-1],myLivSeg.line))

        if showPivot:
            ts = pd.Series(data['close'].values, index=data['date'])
            for ndate,nlabel in note:
                distance = -margin/10
                if nlabel == 'red':
                    distance = margin/10

                if colorType == 4:
                    color = nlabel
                    if nlabel == 'red':
                        color='darkred'
                if colorType == 3:
                    color='fuchsia'
                    if nlabel == 'red':
                        color='blue'

                ax.annotate('',xy=(ndate,ts.asof(ndate)+distance),
                            xytext=(ndate,ts.asof(ndate)+distance*1.2),
                            arrowprops=dict(arrowstyle="->",color=color))
                if showType == 2:
                    axOrig.annotate('',xy=(ndate,ts.asof(ndate)+distance),
                                    xytext=(ndate,ts.asof(ndate)+distance*1.2),
                                    arrowprops=dict(arrowstyle="->",color=color))
                if showType == 3:
                    axK.annotate('',xy=(ndate,ts.asof(ndate)+distance),
                                 xytext=(ndate,ts.asof(ndate)+distance*1.2),
                                 arrowprops=dict(arrowstyle="->",color=color))

        ax.set_xlim([startDate,endDate])
        ax.set_ylim([lowest, highest])
        ax.grid(True, linestyle='--')
        #mondays = WeekdayLocator(MONDAY)
        #mondaysFormatter = DateFormatter('%Y-%m-%d')
        #ax.xaxis.set_major_locator(mondays)
        #ax.xaxis.set_major_formatter(mondaysFormatter)

        #ax.xaxis.set_major_locator(MultipleLocator(20))
        #ax.xaxis.set_minor_locator(MultipleLocator(24))
        # ax.set_xlabel("Date")
        ax.set_ylabel("HFQ price(Unit:RMB yuan)")
        for label in ax.xaxis.get_ticklabels():
            label.set_color('red')
            label.set_rotation(300)
            label.set_fontsize(8)

        if showType == 2:
            axOrig.set_xlim([startDate,endDate])
            axOrig.set_ylim([lowest, highest])
            axOrig.grid(True, linestyle='-.')
            #axOrig.xaxis.set_major_locator(MultipleLocator(20))
            #  axOrig.xaxis.set_minor_locator(MultipleLocator(24))
            # axOrig.set_xlabel("Date")
            axOrig.set_ylabel("HFQ price(Unit:RMB yuan)")
            for label in axOrig.xaxis.get_ticklabels():
                label.set_color('red')
                label.set_rotation(300)
                label.set_fontsize(8)

        if showType == 3:
            axK.set_xlim([startDate,endDate])
            axK.set_ylim([lowest, highest])
            axK.grid(True, linestyle='-.')
            #axK.xaxis.set_major_locator(MultipleLocator(20))
            #  axK.xaxis.set_minor_locator(MultipleLocator(24))
            # axK.set_xlabel("Date")
            axK.set_ylabel("HFQ price(Unit:RMB yuan)")
            for label in axK.xaxis.get_ticklabels():
                label.set_color('red')
                label.set_rotation(300)
                label.set_fontsize(8)

        '''
        ax.xaxis.set_major_locator(DayLocator(bymonthday=range(1,32), interval=15))
        ax.xaxis.set_major_formatter(DateFormatter("%Y-%m-%d"))
        for label in ax.xaxis.get_ticklabels():
           label.set_rotation(45)
        '''
        ax.set_title(stock)
        plt.show()

    def getStockHisRemotely(self, stock,queryStartDateStr,queryEndDateStr):
        url = "https://odin.bajiaoshan893.com/Stock/getStockHistoryDaily?stock="+stock+"&startDate="+queryStartDateStr+"&endDate="+queryEndDateStr
        conn = httplib.HTTPConnection("odin.bajiaoshan893.com")
        conn.request(method="GET",url=url)
        response = conn.getresponse()
        res= response.read()
        obj = json.loads(res).encode('utf-8')
        obj = json.loads(obj)
        return obj['dailyHis']

    def getAllStocks(self):
        url = "https://odin.bajiaoshan893.com/Stock/getAllStocks"
        conn = httplib.HTTPConnection("odin.bajiaoshan893.com")
        conn.request(method="GET",url=url)
        response = conn.getresponse()
        res= response.read()
        obj = json.loads(res).encode('utf-8')
        obj = json.loads(obj)
        return obj['stockList']

    def loadStockList(self):
        stockList = self.getAllStocks()
        for item in stockList: #插入内容
            industry = item['industry']
            if not industry or industry == None:
                industry = '未知'
            self.mlb.insert(END,(item['ts_code'],item['name'],industry,item['list_date']))
        self.mlb.pack(expand=YES, fill=BOTH)

    def createWidgets(self):
        root.title("让利弗莫尔的智慧带领我们走向辉煌！")
        root.geometry('800x600')                 #是x 不是*
        root.resizable(width=True, height=True)

        frame2 = Frame(root)
        self.rb1 = IntVar()
        self.rb2 = IntVar()
        self.rb2.set(1)
        Radiobutton(frame2,variable = self.rb2,text = '展示关键点',value = 1).pack(side=LEFT)
        Radiobutton(frame2,variable = self.rb2,text = '不展示关键点',value = 2).pack(side=LEFT)
        frame2.pack(side=TOP, padx=10)

        frame3 = Frame(root)
        self.rb3 = IntVar()
        self.rb3.set(3)
        Radiobutton(frame3,variable = self.rb3,text = '彩色着色法',value = 3).pack(side=LEFT)
        Radiobutton(frame3,variable = self.rb3,text = '利弗莫尔着色法',value = 4).pack(side=LEFT)
        frame3.pack(side=TOP, padx=10)

        frame1 = Frame(root)
        self.rb1 = IntVar()
        self.rb1.set(1)
        Radiobutton(frame1,variable = self.rb1,text = '单图',value = 1).pack(side=LEFT)
        Radiobutton(frame1,variable = self.rb1,text = '折线对比图',value = 2).pack(side=LEFT)
        Radiobutton(frame1,variable = self.rb1,text = 'K线对比图',value = 3).pack(side=LEFT)
        frame1.pack(side=TOP, padx=10)

        dt = datetime.now()
        endShowDate = dt.strftime("%Y%m%d")

        frame4 = Frame(root)
        var1 = StringVar()
        var1.set("窗口开始日期")
        textLabel1 = Label(frame4,textvariable=var1,justify=LEFT,padx=10)
        textLabel1.pack(side=LEFT)
        self.t2 = Entry(frame4,width=30, borderwidth=2,textvariable='20171024')
        self.t2.insert(0,'20171024')
        self.t2.pack(side=LEFT)
        frame4.pack(side=TOP, padx=10)

        frame5 = Frame(root)
        var2 = StringVar()
        var2.set("窗口结束日期")
        textLabel2 = Label(frame5,textvariable=var2,justify=LEFT,padx=10)
        textLabel2.pack(side=LEFT)
        self.t3 = Entry(frame5,width=30, borderwidth=2)
        self.t3.insert(0,endShowDate)
        self.t3.pack(side=LEFT)
        frame5.pack(side=TOP, padx=10)

        frame6 = Frame(root)
        var3 = StringVar()
        var3.set("查询开始日期")
        textLabel3 = Label(frame6,textvariable=var3,justify=LEFT,padx=10)
        textLabel3.pack(side=LEFT)
        self.t4 = Entry(frame6,width=30, borderwidth=2,textvariable='20161024')
        self.t4.insert(0,'20161024')
        self.t4.pack(side=LEFT)
        frame6.pack(side=TOP, padx=10)

        frame7 = Frame(root)
        var4 = StringVar()
        var4.set("查询结束日期")
        textLabel4 = Label(frame7,textvariable=var4,justify=LEFT,padx=10)
        textLabel4.pack(side=LEFT)
        self.t5 = Entry(frame7,width=30, borderwidth=2)
        self.t5.insert(0,endShowDate)
        self.t5.pack(side=LEFT)
        frame7.pack(side=TOP, padx=10)

        frame8 = Frame(root)
        var = StringVar()
        var.set("股票码")
        textLabel = Label(frame8,textvariable=var,justify=LEFT,padx=10)
        textLabel.pack(side=LEFT)
        self.t1 = Entry(frame8,width=30, borderwidth=2,textvariable='000001.SZ')
        self.t1.insert(0,'000001.SZ')
        self.t1.pack(side=LEFT)
        frame8.pack(side=TOP, padx=10)

        frame9 = Frame(root)
        self.loadStockBtn = Button(frame9,text='加载股票列表')
        self.loadStockBtn["command"] = self.loadStockList
        self.loadStockBtn.pack(side=LEFT)

        self.queryBtn = Button(frame9,text='查询')
        self.queryBtn["command"] = self.draw
        self.queryBtn.pack(side=LEFT)
        frame9.pack(side=TOP, padx=10)

        self.mlb = MultiListbox(root,self.t1,(('股票', 20),('名称', 20),("行业", 20),("上市日期", 20)))


    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

if __name__ == '__main__':
    root = Tk()
    app = Application(master=root)
    app.mainloop()