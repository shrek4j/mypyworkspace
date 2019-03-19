# -*- coding: utf-8 -*
#coding=utf8
import sys
reload(sys)
sys.setdefaultencoding('utf8')

from wxpy import *

bot = Bot(cache_path=True)
#u'宝宝,小nun nun,小推子,白揪兔'
my_friend = bot.friends().search(u'史莱克')[0]
#my_friend.send('发错了，哈哈')

@bot.register(my_friend)
def reply_my_friend(msg):
    print msg
    return 'received: {} ({})'.format(msg.text, msg.type)

bot.join()