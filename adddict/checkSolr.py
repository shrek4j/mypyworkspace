# -*- coding: utf-8 -*
import sys
reload(sys)
sys.setdefaultencoding('utf8')

import requests
import json

import time;  # 引入time模块

solrlist = ["10.102.35.119",
            "10.102.35.121",
            "10.102.35.122",
            "10.102.35.123",
            "10.102.35.124",
            "10.102.35.125",
            "10.102.35.127",
            "10.102.38.47",
            "10.102.38.51",
            "10.102.38.52",
            "10.102.38.53",
            "10.102.38.54",
            "10.102.38.58",
            "10.102.38.59",
            "10.102.38.60",
            "10.102.38.61",
            "10.102.38.65",
            "10.102.38.66"]

solrlist = ["10.102.25.233"]

for ip in solrlist:
    count = 0
    while count < 10000:
        #url = 'http://'+ip+':8091/solr/core_goods/select?wt=json&debugQuery=true&q=text:混合&start=0&rows=20&defType=edismax&fl=productId,number,name,id,categoryId,categoryName,brand,adWords,price,countryId,picture,year,isBook,businessModel,clickNum,favoritesNum,commentsNum,parentId,isHave,isPresale,isPresentCard,attribute,merchantName,merchantNumber,isMerchant,saleNum,score&hl=true&hl.simple.pre=<font%20color="red">&hl.fl=name&hl.simple.post=</font>&facet=true&facet.field=brand&facet.field=countryId&facet.field=categoryId&facet.field=price&facet.field=attribute&fq=(isSfv:1%20AND%20isSale:0)%20OR%20(isSfv:0%20AND%20isMerchant:0%20AND%20region_stock:2709_1)%20OR%20(isMerchant:1%20AND%20region_stock:2709_1)&fq=(saleAddress:\-1%20OR%20saleAddress:0%20OR%20saleAddress:3%20OR%20saleAddress:2%20OR%20saleAddress:4%20OR%20saleAddress:5%20OR%20saleAddress:6%20OR%20saleAddress:7%20OR%20saleAddress:10%20OR%20saleAddress:15%20OR%20saleAddress:14%20OR%20saleAddress:16%20OR%20saleAddress:20%20OR%20saleAddress:22%20OR%20saleAddress:26%20OR%20saleAddress:34%20OR%20saleAddress:28%20OR%20saleAddress:17%20OR%20saleAddress:18%20OR%20saleAddress:30%20OR%20saleAddress:38%20OR%20saleAddress:40%20OR%20saleAddress:43%20OR%20saleAddress:45%20OR%20saleAddress:49%20OR%20saleAddress:73%20OR%20saleAddress:61%20OR%20saleAddress:51%20OR%20saleAddress:65%20OR%20saleAddress:59%20OR%20saleAddress:53%20OR%20saleAddress:63%20OR%20saleAddress:75%20OR%20saleAddress:77%20OR%20saleAddress:91%20OR%20saleAddress:121%20OR%20saleAddress:125%20OR%20saleAddress:145%20OR%20saleAddress:147%20OR%20saleAddress:135%20OR%20saleAddress:155%20OR%20saleAddress:153%20OR%20saleAddress:159%20OR%20saleAddress:163%20OR%20saleAddress:165%20OR%20saleAddress:167%20OR%20saleAddress:157%20OR%20saleAddress:173%20OR%20saleAddress:137%20OR%20saleAddress:1%20OR%20saleAddress:36%20OR%20saleAddress:177%20OR%20saleAddress:181%20OR%20saleAddress:183%20OR%20saleAddress:187%20OR%20saleAddress:67%20OR%20saleAddress:175%20OR%20saleAddress:87%20)&fq=(channelCodes:SDKXD)&fq=price:[*%20TO%20*]&fq=-businessModel:7&bf=sum(1,saleNum)^300&sort=score%20desc';
        url = 'http://'+ip+':8091/solr/core_goods/select?wt=json&debugQuery=true&q=text:混合&start=0&rows=20&defType=edismax&fl=productId,number,name,id,categoryId,categoryName,brand,adWords,price,countryId,picture,year,isBook,businessModel,clickNum,favoritesNum,commentsNum,parentId,isHave,isPresale,isPresentCard,attribute,merchantName,merchantNumber,isMerchant,saleNum,score&hl=true&hl.simple.pre=<font%20color="red">&hl.fl=name&hl.simple.post=</font>&facet=true&facet.field=brand&facet.field=countryId&facet.field=categoryId&facet.field=price&facet.field=attribute&fq=(isSfv:1%20AND%20isSale:0)%20OR%20(isSfv:0%20AND%20isMerchant:0%20AND%20region_stock:2709_1)%20OR%20(isMerchant:1%20AND%20region_stock:2709_1)&fq=(channelCodes:SDKXD)&fq=price:[*%20TO%20*]&fq=-businessModel:7&bf=sum(1,saleNum)^300&sort=score%20desc';
   #     url = 'http://'+ip+':8091/solr/core_userorder/select?q=name:橄榄油%20AND%20userId:26865723%20AND%20(channelCodes:HAP001)&fl=number&start=0&rows=3&sort=orderTime%20desc';
        start = int(round(time.time()*1000))
        results = requests.get(url)
        end = int(round(time.time()*1000))

        #if end - start > 50:
            #print "warning:"
        print count
        print end-start
        rst = json.loads(results.content)
        print json.dumps(rst['debug']['timing'])
        print

        count += 1
