# -*- coding: utf-8 -*
import sys
import cv2
import os
import time
import numpy as np
from PIL import Image
from PIL import ImageChops
from PIL import ImageMorph

reload(sys)
sys.setdefaultencoding('utf8')

def get_screenshot(id):
    os.system('adb shell screencap -p /sdcard/%s.png' % str(id))
    os.system('adb pull /sdcard/%s.png .' % str(id))


im = Image.open("C:\\Users\\Administrator\\Desktop\\3.jpg")
w,h = im.size
pixels = im.load()

#(218, 237, 235)
ren_i = 0
ren_j = 0
flag = False
ren_i2 = 0
ren_j2 = 0
for j in range(0,h,2):
    for i in range(0,w,2):
        if pixels[i,j] == (218, 237, 235) and not flag:
            ren_i = i
            ren_j = j
            flag = True
        if pixels[i,j] == (218, 237, 235) and flag:
            ren_i2 = i
            ren_j2 = j

print ren_i,ren_j
print ren_i2,ren_j2


box1 = (ren_i+15,ren_j,ren_i2+25,(ren_j2-ren_j)/2)
region1 = im.crop(box1)

morphOp = ImageMorph.MorphOp()
morphOp.apply(region1)

box2 = (ren_i+15,ren_j+(ren_j2-ren_j)/2,ren_i2+25,ren_j2)
region2 = im.crop(box2)


#region1.show()
#region2.show()

out = ImageChops.difference(region1, region2)
out.show()

'''
for i in range(w):
    for j in range(ren_j):
        pixels[i,j] = (218, 237, 235)
'''



'''
for i in reversed(range(0,w,10)):
    for j in reversed(range(0,h,10)):
        if pixels[i,j] == (218, 237, 235):
            ren_i = i
            ren_j = j
            break;

print ren_i,ren_j
for i1 in range(w):
    for j1 in reversed(range(ren_j,h)):
        pixels[i1,j1] = (218, 237, 235)
'''


#im.save("C:\\Users\\Administrator\\Desktop\\3-out.jpg")

'''
box = (200,98,1025,922)
region1 = im.crop(box)

box2 = (200,998,1025,1822)
region2 = im.crop(box2)

out = ImageChops.difference(region1, region2)
out.show()
'''