# -*- coding: utf-8 -*
import sys
reload(sys)
sys.setdefaultencoding('utf8')

from com.shrek.assistance.tts.ttshelper import *
import requests
import json

def reportWeather():
    session = requests.session()
    resp = session.get('https://free-api.heweather.net/s6/weather/forecast?location=CN101010100&key=eb7a186421d54c0bb82996143999fab7')
    weather = json.loads(resp.content)['HeWeather6'][0]
    if weather['status'] == 'ok':
        tmw = weather['daily_forecast'][1]
        today = weather['daily_forecast'][0]
        txt = "明天白天" + tmw['cond_txt_d'] + ","+ tmw['wind_dir'] + tmw['wind_sc'] + "级，明天最低温度" + tmw['tmp_min'] + "度，明天最高温度" + tmw['tmp_max'] + "度，今天最低温度" + today['tmp_min'] + "度，今天最高温度" + today['tmp_max'] + "度"
        print txt
        doTTS(txt)