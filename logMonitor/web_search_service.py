import time



def get_events_0():
	events = []
	events.append(["indexfile.log","调用productService.productIdsByChannelCode接口异常"])
	events.append(["indexfile.log","索引ADD自营商品操作失败"])
	events.append(["indexfile.log","构建平台商品Doc失败"])
	events.append(["indexfile.log","索引ADD平台商品操作失败"])
	events.append(["indexfile.log","索引COMMIT操作失败"])
	events.append(["indexfile.log","索引重建发生异常"])
	events.append(["indexfile.log","自营调用productService.productInfo接口异常"])
	events.append(["indexfile.log","自营商品重建索引发生异常"])
	events.append(["indexfile.log","商家调用productService.productInfo接口异常"])
	events.append(["indexfile.log","平台商品重建索引发生异常"])
	events.append(["indexfile.log","创建平台商品索引出错"])
	return events

def get_events_1():
	events = []
	events.append(["search.log","search接口查询时间过长"])
	return events


def get_message_0(response,starttime,endtime,key_word,path_):
	messages = ""
	for (k, v) in response.items():
		if k == "hits":
			for (x, y) in v.items():
				if x == "total":
					if y > 0 :
						starttime1 = time.localtime(starttime/1000)
						starttime2 = time.strftime("%H:%M:%S", starttime1)
						endtime1 = time.localtime(endtime/1000)
						endtime2 = time.strftime("%H:%M:%S", endtime1)
						messages = path_ + "从" + starttime2 + "到" + endtime2 + "出现" + str(y) + "个关键字[" + key_word + "] 请注意查看\r\n"
	return messages


def get_message_1(response,starttime,endtime,key_word,path_):
	messages = ""
	segDict = {}
	for (k, v) in response.items():
		if k == "hits":
			for (x, y) in v.items():

				if x == "total":
					if y > 0 :
						starttime1 = time.localtime(starttime/1000)
						starttime2 = time.strftime("%H:%M:%S", starttime1)
						endtime1 = time.localtime(endtime/1000)
						endtime2 = time.strftime("%H:%M:%S", endtime1)
						messages = path_ + "从" + starttime2 + "到" + endtime2 + "出现" + str(y) + "个关键字[" + key_word + "]，请注意查看。超时详细信息："

				if x == "hits" and key_word =="search接口查询时间过长":
					for p in y:
						for (a, b) in p.items():
							if a == "_source":
								for (j, k) in b.items():
									if j == "message":
										timeCost = int(k.split('|')[2])
										if timeCost <= 4000:
											timeCost = 4000
										elif timeCost <= 5000:
											timeCost = 5000
										elif timeCost <= 6000:
											timeCost = 6000
										elif timeCost <= 7000:
											timeCost = 7000
										elif timeCost <= 8000:
											timeCost = 8000
										elif timeCost <= 9000:
											timeCost = 9000
										elif timeCost <= 10000:
											timeCost = 10000
										elif timeCost <= 20000:
											timeCost = 20000
										elif timeCost <= 30000:
											timeCost = 30000
										else:
											timeCost = 100000

										count1 = segDict.get(timeCost)
										if not count1:
											segDict[timeCost] = 1
										else:
											segDict[timeCost] = count1 + 1

	segDict = [ (v,segDict[v]) for v in sorted(segDict.keys())]
	for tuple in segDict:
		if tuple[0] == 100000:
			messages += "超过30秒:%s个，" % (tuple[1])
		else:
			messages += "%s秒内:%s个，" % (int(tuple[0]/1000), tuple[1])
	return messages