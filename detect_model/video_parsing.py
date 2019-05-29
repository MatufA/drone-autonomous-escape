# -*- coding: utf-8 -*-

import cv2
import numpy as np

vidcap = cv2.VideoCapture('2.mp4')
success, img = vidcap.read()
count = 29
num = 0

while success:
    vidcap.set(cv2.CAP_PROP_POS_MSEC,(count*500))
    count += 1   
    
    # if count%7 == 0:
    #     brightness = 50
    #     contrast = 30
    #     img = np.int16(img)
    #     img = img * (contrast/127+1) - contrast + brightness
    #     img = np.clip(img, 0, 255)
    #     img = np.uint8(img)
    
    rows, cols, _ = img.shape
    # M = cv2.getRotationMatrix2D((cols/2,rows/2),70,1)
    # img_70 = cv2.warpAffine(img,M,(cols,rows))
    
    # M = cv2.getRotationMatrix2D((cols/2,rows/2),-50,1)
    # img_Minus_50 = cv2.warpAffine(img,M,(cols,rows))
    
    print(count%17)
    num += 1
    cv2.imwrite("data//images//{:4}.jpg".format(count), img)
    # num+=1
    # cv2.imwrite("vid1_imgs//frame%d.jpg" % num, img_70)
    # num+=1
    # cv2.imwrite("vid1_imgs//frame%d.jpg" % num, img_Minus_50)     # save frame as JPEG file      
    success ,img = vidcap.read()
    # print('save a new frame:  ', num, success)
