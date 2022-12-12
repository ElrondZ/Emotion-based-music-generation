#test_html.py
#在url库里，查找request模块，导入urlopen函数

from urllib.request import urlopen
from bs4 import BeautifulSoup


html = urlopen('http://www.weather.com.cn/weather/401110101.shtml')
bs_obj = BeautifulSoup(html.read(), 'html.parser')
weather = bs_obj.find("p", "wea").text
tem = bs_obj.find("p", "tem").text

print(weather)
print(tem)
html.close()
