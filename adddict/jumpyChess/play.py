# -*- coding: utf-8 -*
import sys
import cv2
import os
import time
import numpy as np

reload(sys)
sys.setdefaultencoding('utf8')

def get_screenshot(id):
    os.system('adb shell screencap -p /sdcard/%s.png' % str(id))
    os.system('adb pull /sdcard/%s.png .' % str(id))

def jump(distance):
    # 这个参数还需要针对屏幕分辨率进行优化
    press_time = int(distance * 2)
    print press_time
    cmd = 'adb shell input swipe 320 410 320 410 ' + str(press_time)
    os.system(cmd)

def get_center(img_canny, ):
    # 利用边缘检测的结果寻找物块的上沿和下沿
    # 进而计算物块的中心点
    y_top = np.nonzero([max(row) for row in img_canny[400:]])[0][0] + 400
    x_top = int(np.mean(np.nonzero(canny_img[y_top])))

    y_bottom = y_top + 50
    for row in range(y_bottom, H):
        if canny_img[row, x_top] != 0:
            y_bottom = row
            break

    x_center, y_center = x_top, (y_top + y_bottom) // 2
    return img_canny, x_center, y_center



# 匹配小跳棋的模板
chess = cv2.imread('temp_player.jpg', 0)
w1, h1 = chess.shape[::-1]

# 匹配游戏结束画面的模板
temp_end = cv2.imread('temp_end.jpg', 0)

# 循环直到游戏失败结束
for i in range(10000):
    get_screenshot(i)
    gamePic = cv2.imread('%s.png' % 0, 0)
    gamePic1 = cv2.imread('%s.png' % 0)

    # 模板匹配截图中小跳棋的位置
    res = cv2.matchTemplate(gamePic,chess,cv2.TM_CCOEFF_NORMED)
    min_val1,max_val1,min_loc1,max_loc1 = cv2.minMaxLoc(res)
    center1_loc = (max_loc1[0] + 39, max_loc1[1] + 189)

    # 边缘检测
    # 先做高斯模糊能够提高边缘检测的效果
    gausPic = cv2.GaussianBlur(gamePic1,(5,5),0)
    cv2.imwrite('gaus.png', gausPic)
    grayPic = cv2.cvtColor(gausPic,cv2.COLOR_BGR2GRAY)
    cv2.imwrite('gray.png', grayPic)
    canny_img = cv2.Canny(grayPic, 1, 10)
    cv2.imwrite('canny.png', canny_img)
    H, W = canny_img.shape

    # 消去小跳棋轮廓对边缘检测结果的干扰
    #for k in range(max_loc1[1] - 10, max_loc1[1] + 189):
    #    for b in range(max_loc1[0] - 10, max_loc1[0] + 100):
    #        canny_img[k][b] = 0
    img_rgb, x_center, y_center = get_center(canny_img)

    # 将图片输出以供调试
    img_rgb = cv2.circle(img_rgb, (x_center, y_center), 10, 255, -1)
    # cv2.rectangle(canny_img, max_loc1, center1_loc, 255, 2)
    cv2.imwrite('last.png', img_rgb)

    distance = (center1_loc[0] - x_center) ** 2 + (center1_loc[1] - y_center) ** 2
    distance = distance ** 0.5
    jump(distance)
    time.sleep(2)