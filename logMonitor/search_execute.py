import time
import user_center_util
import web_search_service

'''
per hour
'''
list = web_search_service.get_events_1()
for item in list:
	path_ = item[0]
	endtime = int(round(time.time() * 1000))
	starttime = endtime - 1000 * 60 * 60
	key_word = item[1]
	response = user_center_util.search_es(starttime,endtime,path_,key_word,10000)
	messages = web_search_service.get_message_1(response, starttime, endtime, key_word, path_)
	if messages:
		user_center_util.send_weixin_message(path_,messages)