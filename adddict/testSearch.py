# -*- coding: UTF-8 -*-
# encoding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import urllib
import json
from pyhessian.client import HessianProxy

service = HessianProxy("http://search.sfbest.com/search/remoteSearcher.hessian")
result = service.search("{\"channelCodes\":[\"HAP001\"],\"ltrType\":1,\"threeRegion\":500,\"isreach\":true,\"isstock\":true,\"keyword\":\"牛肉\",\"pageNo\":0,\"pageSize\":36}")
result=urllib.unquote(result)
rstJson = json.loads(result)
print rstJson['result']['productList']