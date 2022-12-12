#test_html.py
#在url库里，查找request模块，导入urlopen函数

import re
from urllib.request import urlopen
from bs4 import BeautifulSoup

def get_weather(weather):
    res = "sunny"

    if(re.search(r'晴', weather)):
        res = "sunny"
    elif(re.search(r'阴', weather)):
        res = "cloudy"
    elif(re.search(r'雨', weather)):
        res = "rainy"
    else:
        res = "snowy"

    return res

html = urlopen('http://www.weather.com.cn/weather/401110101.shtml')
bs_obj = BeautifulSoup(html.read(), 'html.parser')
weather = bs_obj.find("p", "wea").text
tem = bs_obj.find("p", "tem").text

# res = get_weather(weather)
res = get_weather(weather)
print(res)
html.close()

