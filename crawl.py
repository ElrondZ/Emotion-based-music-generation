import tkinter
import re
from urllib.request import urlopen
from bs4 import BeautifulSoup
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *


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


root = tk.Tk()
root.title("Main Page")
root.geometry("400x200")
label = tkinter.Label(root, text="welcome")
label.pack()

b1 = ttk.Button(root, text="Button 1", bootstyle=SUCCESS)
b1.pack(side=LEFT, padx=5, pady=10)

b2 = ttk.Button(root, text="Button 2", bootstyle=(INFO, OUTLINE))
b2.pack(side=LEFT, padx=5, pady=10)

root.mainloop()

