# coding: utf8

# @Author: 郭 璞
# @File: MyZhiHuLogin.py                                                                 
# @Time: 2017/4/8                                   
# @Contact: 1064319632@qq.com
# @blog: http://blog.csdn.net/marksinoberg
# @Description: 我的模拟登录知乎

import requests
from bs4 import BeautifulSoup
import os, time
import re

# import http.cookiejar as cookielib

# ------------------------------------------------------------------------------------------------------
# @ creat Request headers
# agent = 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Mobile Safari/537.36'
agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
headers = {
    "Host": "www.zhihu.com",
    "Referer": "https://www.zhihu.com/",
    'User-Agent': agent
}

# ------------------------------------------------------------------------------------------------------
# @ session
session = requests.Session()

# ------------------------------------------------------------------------------------------------------
# @ xsrf_token
homeurl = 'https://www.zhihu.com'

# @ proxy
proxies = {"http": "http://10.144.1.10:8080", "https": "http://10.144.1.10:8080", }

homeresponse = session.get(url=homeurl, headers=headers, proxies=proxies)

homesoup = BeautifulSoup(homeresponse.text, 'html.parser')
xsrfinput = homesoup.find('input', {'name': '_xsrf'})
xsrf_token = xsrfinput['value']
print("got xsrf_token： ", xsrf_token)



# ------------------------------------------------------------------------------------------------------
# @ sign up
headers['X-Xsrftoken'] = xsrf_token
headers['X-Requested-With'] = 'XMLHttpRequest'
loginurl = 'https://www.zhihu.com/login/email'

postdata = {
    '_xsrf': xsrf_token,
    'email': '15858127547@139.com',
    'password': '50948612'
}

# @ get auth code
randomtime = str(int(time.time() * 1000))
captchaurl = 'https://www.zhihu.com/captcha.gif?r=' + \
             randomtime + "&type=login"
captcharesponse = session.get(url=captchaurl, headers=headers, proxies=proxies)
with open('checkcode.gif', 'wb') as f:
    f.write(captcharesponse.content)
    f.close()

captcha = input('请输入验证码：')
print(captcha)
postdata['captcha'] = captcha
loginresponse = session.post(url=loginurl, headers=headers, data=postdata, proxies=proxies)
print('服务器端返回响应码：', loginresponse.status_code)
print(loginresponse.json())

# ------------------------------------------------------------------------------------------------------
# @ print the signed up page
profileurl = 'https://www.zhihu.com/settings/profile'
profileresponse = session.get(url=profileurl, headers=headers, proxies=proxies)
print('profile页面响应码：', profileresponse.status_code)
profilesoup = BeautifulSoup(profileresponse.text, 'html.parser')
div = profilesoup.find('div', {'id': 'rename-section'})
print(div)
