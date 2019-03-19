# encoding: utf-8
# -*- coding: utf-8 -*
import sys
reload(sys)
sys.setdefaultencoding('utf8')

from readability import Readability

#file = open("C:\\Users\\Administrator\\Desktop\\myfolder\\sea-and-adventures\\the-old-man-and-the-sea.txt")
file = open("C:\\Users\\Administrator\\Desktop\\myfolder\\corpora\\An-Inquiry-into-the-Nature-and-Causes-of-the-Wealth-of-Nations.txt")
text = file.read()
rd = Readability(text)
print 'ARI: ', rd.ARI()
print 'FleschReadingEase: ', rd.FleschReadingEase()
print 'FleschKincaidGradeLevel: ', rd.FleschKincaidGradeLevel()
print 'GunningFogIndex: ', rd.GunningFogIndex()
print 'SMOGIndex: ', rd.SMOGIndex()
print 'ColemanLiauIndex: ', rd.ColemanLiauIndex()
print 'LIX: ', rd.LIX()
print 'RIX: ', rd.RIX()

