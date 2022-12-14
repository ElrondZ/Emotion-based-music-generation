import os

import cv2
import cvzone
from cvzone.SelfiSegmentationModule import SelfiSegmentation
from crawl import get_index

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

segmentor = SelfiSegmentation()
fpsReader = cvzone.FPS()

listImg = os.listdir("weather_img")
imgList = []
for imgPath in listImg:
    img = cv2.imread(f'weather_img/{imgPath}')
    imgList.append(img)

indexImg = get_index()

while True:
    success, img = cap.read()
    imgOut = segmentor.removeBG(img, imgList[indexImg], threshold=0.8)

    imgStack = cvzone.stackImages([img, imgOut], 2, 1)
    _, imgStack = fpsReader.update(imgStack)

    cv2.imshow("image", imgStack)
    key = cv2.waitKey(1)
    if key == ord('a'):
        if indexImg > 0:
            indexImg -= 1
    elif key == ord('d'):
        if indexImg < len(imgList) - 1:
            indexImg += 1
    elif key == ord('q'):
        break
