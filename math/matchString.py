# -*- coding: utf-8 -*
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import csv
import re

def cleanseString(name):
    return name.replace(" ","")


dict = {}
with open("C:\Users\Administrator\Desktop\product_name.csv") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        gbkrow = row['name'].decode('GBK')
        gbkrow = gbkrow.replace("["," ")
        gbkrow = gbkrow.replace("]"," ")
        gbkrow = gbkrow.replace("【"," ")
        gbkrow = gbkrow.replace("】"," ")
        gbkrow = gbkrow.replace("("," ")
        gbkrow = gbkrow.replace(")"," ")
        gbkrow = gbkrow.replace("（"," ")
        gbkrow = gbkrow.replace("）"," ")
        gbkrow = gbkrow.replace("*"," ")
        gbkrow = gbkrow.replace("“"," ")
        gbkrow = gbkrow.replace("”"," ")
        gbkrow = gbkrow.replace("-"," ")
        gbkrow = gbkrow.replace("+"," ")
        gbkrow = gbkrow.replace("."," ")
        gbkrow = gbkrow.replace("~"," ")
        strinfo = re.compile('[a-zA-Z0-9]+')
        gbkrow = strinfo.sub(" ",gbkrow)
        words = gbkrow.split(" ")
        for w in words:
            if len(w) < 2:
                continue
            if dict.get(w):
                num = dict.get(w)
                dict[w] = num + 1
            else:
                dict[w] = 1

prodNames = dict.keys()

dict2 = {}
count = 0
for name in prodNames:
    n = count
    count+=1
    while True:
        n += 1
        if n >= len(prodNames):
            break
        name1 = prodNames[n]
        if name == name1:
            continue

        outeri = -1
        while True:
            outeri += 1
            i = outeri
            for j in range(len(name1)):
                if (i < len(name)-1) and (j < len(name1)-1) and name[i] == name1[j]:
                    if (i < len(name)-1) and (j < len(name1)-1) and (name[i+1] == name1[j+1]):
                        if (i+1 < len(name)-1) and (j+1 < len(name1)-1) and (name[i+2] == name1[j+2]):
                            if (i+2 < len(name)-1) and (j+2 < len(name1)-1) and (name[i+3] == name1[j+3]):
                                if (i+3 < len(name)-1) and (j+3 < len(name1)-1) and (name[i+4] == name1[j+4]):
                                    if (i+4 < len(name)-1) and (j+4 < len(name1)-1) and (name[i+5] == name1[j+5]):
                                        if (i+5 < len(name)-1) and (j+5 < len(name1)-1) and (name[i+6] == name1[j+6]):
                                            if (i+6 < len(name)-1) and (j+6 < len(name1)-1) and (name[i+7] == name1[j+7]):
                                                if (i+7 < len(name)-1) and (j+7 < len(name1)-1) and (name[i+8] == name1[j+8]):
                                                    if (i+8 < len(name)-1) and (j+8 < len(name1)-1) and (name[i+9] == name1[j+9]):
                                                        if (i+9 < len(name)-1) and (j+9 < len(name1)-1) and (name[i+10] == name1[j+10]):
                                                            wd = name[i:i+10]
                                                            if dict2.get(wd):
                                                                num = dict2.get(wd)
                                                                dict2[wd] = num + 1
                                                            else:
                                                                dict2[wd] = 1
                                                            outeri += 9
                                                            break
                                                    else:
                                                        wd = name[i:i+9]
                                                        if dict2.get(wd):
                                                            num = dict2.get(wd)
                                                            dict2[wd] = num + 1
                                                        else:
                                                            dict2[wd] = 1
                                                        outeri += 8
                                                        break
                                                else:
                                                    wd = name[i:i+8]
                                                    if dict2.get(wd):
                                                        num = dict2.get(wd)
                                                        dict2[wd] = num + 1
                                                    else:
                                                        dict2[wd] = 1
                                                    outeri += 7
                                                    break
                                            else:
                                                wd = name[i:i+7]
                                                if dict2.get(wd):
                                                    num = dict2.get(wd)
                                                    dict2[wd] = num + 1
                                                else:
                                                    dict2[wd] = 1
                                                outeri += 6
                                                break
                                        else:
                                            wd = name[i:i+6]
                                            if dict2.get(wd):
                                                num = dict2.get(wd)
                                                dict2[wd] = num + 1
                                            else:
                                                dict2[wd] = 1
                                            outeri += 5
                                            break
                                    else:
                                        wd = name[i:i+5]
                                        if dict2.get(wd):
                                            num = dict2.get(wd)
                                            dict2[wd] = num + 1
                                        else:
                                            dict2[wd] = 1
                                        outeri += 4
                                        break
                                else:
                                    wd = name[i:i+4]
                                    if dict2.get(wd):
                                        num = dict2.get(wd)
                                        dict2[wd] = num + 1
                                    else:
                                        dict2[wd] = 1
                                    outeri += 3
                                    break
                            else:
                                wd = name[i:i+3]
                                if dict2.get(wd):
                                    num = dict2.get(wd)
                                    dict2[wd] = num + 1
                                else:
                                    dict2[wd] = 1
                                outeri += 2
                                break
                        else:
                            wd = name[i:i+2]
                            if dict2.get(wd):
                                num = dict2.get(wd)
                                dict2[wd] = num + 1
                            else:
                                dict2[wd] = 1
                            outeri += 1
                            break
                    else:
                        pass
                else:
                    pass
            if outeri == len(name) - 1:
                break

print "------dict------"
for w in dict2:
    print w,dict2[w]