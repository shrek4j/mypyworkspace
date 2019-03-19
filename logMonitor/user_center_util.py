import urllib.request
from urllib.parse import quote
from elasticsearch import Elasticsearch


def send_weixin_message(text, desp):
	req = urllib.request.Request("http://pushbear.ftqq.com/sub?sendkey=2748-604ec2ad00808e9ca4345f2682eef17f&" + "text="+ text +"&desp="+quote(desp))
	data = urllib.request.urlopen(req).read()
	print (desp)


def search_es(start_time,end_time,path_,keyword,size):
	esclient = Elasticsearch(['http://10.102.4.250:9200'])
	response = esclient.search(
	index='java-log-*',
	body={
		"size": size,
		"sort": [{
			"@timestamp": {
				"order": "desc",
				"unmapped_type": "boolean"
			}
		}],
		"query": {
			"bool": {
				"must": [{
					"match_phrase": {
						"message": {
							"query": keyword
						}
					}
				}, {
					"match_phrase": {
						"path": {
							"query": path_
						}
					}
				}, {
					"range": {
						"@timestamp": {
							"gte": start_time,
							"lte": end_time,
							"format": "epoch_millis"
						}
					}
				}]
			}
		},
		"aggs": {
			"2": {
				"date_histogram": {
					"field": "@timestamp",
					"interval": "30m",
					"time_zone": "Asia/Shanghai",
					"min_doc_count": 1
				}
			}
		}
	}
	)
	return response