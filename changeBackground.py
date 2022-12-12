import os
import cv2
import cvzone
from cvzone.SelfiSegmentationModule import SelfiSegmentation
import re
from urllib.request import urlopen
from bs4 import BeautifulSoup

def get_weather(weather):
    res = "sunny"

    if re.search(r'晴', weather):
        res = "sunny"
    elif re.search(r'阴', weather):
        res = "cloudy"
    elif re.search(r'雨', weather):
        res = "rainy"
    else:
        res = "snowy"

    return res

def get_index():
    html = urlopen('http://www.weather.com.cn/weather/401110101.shtml')
    bs_obj = BeautifulSoup(html.read(), 'html.parser')
    weather = bs_obj.find("p", "wea").text
    tem = bs_obj.find("p", "tem").text
    html.close()

    res = get_weather(weather)
    print(res)

    index = -1
    if res == "sunny":
        index = 2
    elif res == "cloudy":
        index = 1
    elif res == "rainy":
        index = 3
    else:
        index = 0
    return index

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

    imgStack = cvzone.stackImages([img, imgOut], 2,1)
    _, imgStack = fpsReader.update(imgStack)

    cv2.imshow("image", imgStack)
    key = cv2.waitKey(1)
    if key == ord('a'):
        if indexImg>0:
            indexImg -=1
    elif key == ord('d'):
        if indexImg<len(imgList)-1:
            indexImg +=1
    elif key == ord('q'):
        break

