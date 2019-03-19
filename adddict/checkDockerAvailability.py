# -*- coding: utf-8 -*
import sys
reload(sys)
sys.setdefaultencoding('utf8')

from pyhessian.client import HessianProxy

ips = ["10.102.26.145","10.102.26.144","10.102.26.146","10.102.26.143","10.102.26.142","10.102.26.141","10.102.27.137",
       "10.102.27.136","10.102.27.135","10.102.27.134","10.102.8.193","10.102.8.192","10.102.8.191","10.102.8.190",
       "10.102.8.19","10.102.8.189","10.102.8.188","10.102.8.187","10.102.8.186","10.102.8.185"]
path = "http://127.0.0.1:8081/search/remoteSearcher.hessian"
params = '{"channelCodes":["HPC001"],"isreach":true,"isstock":true,"keyword":"beef","pageNo":0,"pageSize":1}'

running = 0
exception = 0
for ip in ips:
    url = path.replace("127.0.0.1",ip)
    print url
    service = HessianProxy(url)

    try:
        result = service.search(params)
        print ip + " 正常运行中..."
        running += 1
    except Exception,e:
        print ip + " 服务异常!!!"
        exception += 1

print "总机器数："+ str(len(ips))
print "运行机器数："+ str(running)
print "异常机器数："+ str(exception)
