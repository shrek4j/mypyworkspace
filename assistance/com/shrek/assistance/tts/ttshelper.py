# -*- coding: utf-8 -*
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from aip import AipSpeech
from playsound import playsound
import os

APP_ID = '15696556'
API_KEY = '9iLQvBS33Vszc1BUFrpUbp2R'
SECRET_KEY = 'DwLVNv0GMAaKyeXzOOfy0q5A8lpTKygG'
client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

def doTTS(text):
    result  = client.synthesis(text, 'zh', 1, {
        'vol': 5,
    })

    if not isinstance(result, dict):
        file = 'D:/pyworkspace/assistance/com/shrek/assistance/tts/audio.mp3'
        with open(file, 'wb') as f:
            f.write(result)
        playsound(file)
        os.remove(file)