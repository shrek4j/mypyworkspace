# -*- coding: utf-8 -*
from LivSeg import LivSeg
from datetime import datetime

class LivRule(object):

    def __init__(self):
        pass

    @staticmethod
    def doLivLogic(livSegList,close,date,lastDate):
        livSegList.livSegAll.date.append(date)
        livSegList.livSegAll.close.append(close)

        if len(livSegList.list) == 0:#the open day
            livSeg = LivSeg('ambi')
            livSeg.date.append(date)
            livSeg.close.append(close)
            livSegList.list.append(livSeg)
        elif len(livSegList.list) == 1 and livSegList.list[-1].type == 'ambi':#right after the open day, to make clear of the trend
            if livSegList.list[-1].close[-1] == close:
                livSegList.list[-1].date.append(date)
                livSegList.list[-1].close.append(close)
            else:
                if livSegList.list[-1].close[-1] > close:
                    livSegList.list[-1].type = 'dt'
                    livSegList.lastDTClose = close
                elif livSegList.list[-1].close[-1] < close:
                    livSegList.list[-1].type = 'ut'
                    livSegList.lastUTClose = close
                if lastDate == livSegList.list[-1].date[-1]:
                    livSegList.list[-1].date.append(date)
                    livSegList.list[-1].close.append(close)
                else:
                    livSeg = LivSeg(livSegList.list[-1].type)
                    livSeg.date.append(date)
                    livSeg.close.append(close)
                    livSegList.list.append(livSeg)
        elif livSegList.list[-1].type == 'ut' and close >= livSegList.list[-1].close[-1]:#1、6. (d) if an upward trend should continue
            if lastDate == livSegList.list[-1].date[-1]:
                livSegList.list[-1].date.append(date)
                livSegList.list[-1].close.append(close)
            else:
                livSeg = LivSeg(livSegList.list[-1].type)
                livSeg.date.append(date)
                livSeg.close.append(close)
                livSegList.list.append(livSeg)
            livSegList.lastUTClose = close
        elif livSegList.list[-1].type == 'dt' and close <= livSegList.list[-1].close[-1]:#2、6. (b) if a downward trend should continue
            if lastDate == livSegList.list[-1].date[-1]:
                livSegList.list[-1].date.append(date)
                livSegList.list[-1].close.append(close)
            else:
                livSeg = LivSeg(livSegList.list[-1].type)
                livSeg.date.append(date)
                livSeg.close.append(close)
                livSegList.list.append(livSeg)
            livSegList.lastDTClose = close
        elif livSegList.list[-1].type == 'ut' and close < livSegList.list[-1].close[-1] and ((livSegList.list[-1].close[-1] - close)/livSegList.list[-1].close[-1] >= 0.06):#4. (a) if a natural reaction occurs
            livSegList.list[-1].line = 'red'
            livSeg = LivSeg('nre')
            livSeg.date.append(date)
            livSeg.close.append(close)
            livSegList.list.append(livSeg)
        elif livSegList.list[-1].type == 'dt' and close > livSegList.list[-1].close[-1] and ((close - livSegList.list[-1].close[-1])/livSegList.list[-1].close[-1] >= 0.06):#4. (c)if a natural rally occurs
            livSegList.list[-1].line = 'black'
            livSeg = LivSeg('nra')
            livSeg.date.append(date)
            livSeg.close.append(close)
            livSegList.list.append(livSeg)
        elif livSegList.list[-1].type == 'nre' and close < livSegList.list[-1].close[-1] and livSegList.lastDTClose != -1.00 and close < livSegList.lastDTClose:#6. (e)
            livSeg = LivSeg('dt')
            livSeg.date.append(date)
            livSeg.close.append(close)
            livSegList.list.append(livSeg)
            livSegList.lastDTClose = close
        elif livSegList.list[-1].type == 'nra' and close > livSegList.list[-1].close[-1] and livSegList.lastUTClose != -1.00 and close > livSegList.lastUTClose:#6. (f)
            livSeg = LivSeg('ut')
            livSeg.date.append(date)
            livSeg.close.append(close)
            livSegList.list.append(livSeg)
            livSegList.lastUTClose = close
        elif ((livSegList.list[-1].type == 'nra' and livSegList.list[-2].type == 'nre' and livSegList.list[-3].type == 'ut') or livSegList.list[-1].type == 'nf-nra') and close < livSegList.list[-1].close[-1] and ((livSegList.list[-1].close[-1] - close)/livSegList.list[-1].close[-1] >= 0.06):#4. (d)if a natural reaction occurs
            livSegList.list[-1].line = 'black'
            livSegList.lastBlackClose = livSegList.list[-1].close[-1]
            livSeg = LivSeg('nf-nre')
            livSeg.date.append(date)
            livSeg.close.append(close)
            livSegList.list.append(livSeg)
        elif ((livSegList.list[-1].type == 'nre' and livSegList.list[-2].type == 'nra' and livSegList.list[-3].type == 'dt') or livSegList.list[-1].type == 'nf-nre') and close > livSegList.list[-1].close[-1] and ((close - livSegList.list[-1].close[-1])/livSegList.list[-1].close[-1] >= 0.06):#4. (b)if a natural rally occurs
            livSegList.list[-1].line = 'red'
            livSegList.lastRedClose = livSegList.list[-1].close[-1]
            livSeg = LivSeg('nf-nra')
            livSeg.date.append(date)
            livSeg.close.append(close)
            livSegList.list.append(livSeg)
        elif livSegList.list[-1].type == 'nra' and close < livSegList.list[-1].close[-1] and ((livSegList.list[-1].close[-1] - close)/livSegList.list[-1].close[-1] >= 0.06):#4. (d)if a natural reaction occurs
            livSegList.list[-1].line = 'black'
            livSegList.lastBlackClose = livSegList.list[-1].close[-1]
            livSeg = LivSeg('nre')
            livSeg.date.append(date)
            livSeg.close.append(close)
            livSegList.list.append(livSeg)
        elif livSegList.list[-1].type == 'nre' and close > livSegList.list[-1].close[-1] and ((close - livSegList.list[-1].close[-1])/livSegList.list[-1].close[-1] >= 0.06):#4. (b)if a natural rally occurs
            livSegList.list[-1].line = 'red'
            livSegList.lastRedClose = livSegList.list[-1].close[-1]
            livSeg = LivSeg('nra')
            livSeg.date.append(date)
            livSeg.close.append(close)
            livSegList.list.append(livSeg)
        elif livSegList.list[-1].type == 'nf-nra' and close > livSegList.list[-1].close[-1] and livSegList.lastBlackClose != -1.00 and close > livSegList.lastBlackClose and (close - livSegList.lastBlackClose)/livSegList.lastBlackClose >= 0.03:#5. (a)
            livSeg = LivSeg('ut')
            livSeg.date.append(date)
            livSeg.close.append(close)
            livSegList.list.append(livSeg)
            livSegList.lastUTClose = close
        elif livSegList.list[-1].type == 'nf-nre' and close < livSegList.list[-1].close[-1] and livSegList.lastRedClose != -1.00 and close < livSegList.lastRedClose and (livSegList.lastRedClose - close)/livSegList.lastRedClose >= 0.03:#5. (b)
            livSeg = LivSeg('dt')
            livSeg.date.append(date)
            livSeg.close.append(close)
            livSegList.list.append(livSeg)
            livSegList.lastDTClose = close
        elif livSegList.list[-1].type == 'nra' and close > livSegList.list[-1].close[-1] and livSegList.lastBlackClose != -1.00 and close > livSegList.lastBlackClose and (close - livSegList.lastBlackClose)/livSegList.lastBlackClose >= 0.03:#5. (a)
            livSeg = LivSeg('ut')
            livSeg.date.append(date)
            livSeg.close.append(close)
            livSegList.list.append(livSeg)
            livSegList.lastUTClose = close
        elif livSegList.list[-1].type == 'nre' and close < livSegList.list[-1].close[-1] and livSegList.lastRedClose != -1.00 and close < livSegList.lastRedClose and (livSegList.lastRedClose - close)/livSegList.lastRedClose >= 0.03:#5. (b)
            livSeg = LivSeg('dt')
            livSeg.date.append(date)
            livSeg.close.append(close)
            livSegList.list.append(livSeg)
            livSegList.lastDTClose = close
        #TODO 6. (g)

        #TODO 6. (h)
        elif (livSegList.list[-1].type == 'nra' or livSegList.list[-1].type == 'nf-nra') and livSegList.list[-1].close[-1] <= close:#6. (c)、6. (d) if a natrual rally should continue
            if lastDate == livSegList.list[-1].date[-1]:
                livSegList.list[-1].date.append(date)
                livSegList.list[-1].close.append(close)
            else:
                livSeg = LivSeg(livSegList.list[-1].type)
                livSeg.date.append(date)
                livSeg.close.append(close)
                livSegList.list.append(livSeg)
        elif (livSegList.list[-1].type == 'nre' or livSegList.list[-1].type == 'nf-nre') and livSegList.list[-1].close[-1] >= close:#6. (a)、6. (b) if a natrual reaction should continue
            if lastDate == livSegList.list[-1].date[-1]:
                livSegList.list[-1].date.append(date)
                livSegList.list[-1].close.append(close)
            else:
                livSeg = LivSeg(livSegList.list[-1].type)
                livSeg.date.append(date)
                livSeg.close.append(close)
                livSegList.list.append(livSeg)




