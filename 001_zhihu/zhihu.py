# ------------------------------------------------------------------------------------------------------
# !/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Required
- requests (必须)
- pillow (可选)
Info
- author : "xchaoinfo"
- email  : "xchaoinfo@qq.com"
- date   : "2016.2.4"
Update
- name   : "wangmengcn"
- email  : "eclipse_sv@163.com"
- date   : "2016.4.21"
'''
# ------------------------------------------------------------------------------------------------------
import requests

try:
    import cookielib
except:
    import http.cookiejar as cookielib
import re
import time
import os.path

try:
    from PIL import Image
except:
    pass
# ------------------------------------------------------------------------------------------------------
# creat Request headers
agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
headers = {
    "Host": "www.zhihu.com",
    'User-Agent': agent
}

# ------------------------------------------------------------------------------------------------------
# @ proxy
proxies = {"http": "http://10.144.1.10:8080", "https": "http://10.144.1.10:8080", }

# ------------------------------------------------------------------------------------------------------
# cookies
session = requests.session()
session.cookies = cookielib.LWPCookieJar(filename='cookies')
try:
    # @ get the saved cookies
    session.cookies.load(ignore_discard=True)
except:
    print("Cookie 未能加载")


# ------------------------------------------------------------------------------------------------------
# @ get xsrf
def get_xsrf():
    '''get _xsrf from html'''
    index_url = 'https://www.zhihu.com'
    # @ _xsrf
    index_page = session.get(index_url, headers=headers, proxies=proxies)
    html = index_page.text
    pattern = r'name="_xsrf" value="(.*?)"'
    _xsrf = re.findall(pattern, html)
    return _xsrf[0]


# ------------------------------------------------------------------------------------------------------
# @ get
def get_captcha():
    # @ get captcha
    t = str(int(time.time() * 1000))
    captcha_url = 'https://www.zhihu.com/captcha.gif?r=' + t + "&type=login"
    r = session.get(captcha_url, headers=headers, proxies=proxies)

    # @ save to img
    with open('captcha.jpg', 'wb') as f:
        f.write(r.content)
        f.close()
    # @ show the auth code
    try:
        im = Image.open('captcha.jpg')
        im.show()
        im.close()
    except:
        print(u'请到 %s 目录找到captcha.jpg 手动输入' % os.path.abspath('captcha.jpg'))
    captcha = input("please input the captcha\n>")
    return captcha


def isLogin():
    # is login
    url = "https://www.zhihu.com/settings/profile"
    login_code = session.get(url, headers=headers, allow_redirects=False, proxies=proxies).status_code
    if login_code == 200:
        return True
    else:
        return False


# ------------------------------------------------------------------------------------------------------
# @ login
def login(secret, account):
    # @ xsrf
    _xsrf = get_xsrf()
    headers["X-Xsrftoken"] = _xsrf
    headers["X-Requested-With"] = "XMLHttpRequest"
    # @ phone num
    if re.match(r"^1\d{10}$", account):
        print("手机号登录 \n")
        post_url = 'https://www.zhihu.com/login/phone_num'
        postdata = {
            '_xsrf': _xsrf,
            'password': secret,
            'phone_num': account
        }
    else:
        # @ email
        if "@" in account:
            print("邮箱登录 \n")
        else:
            print("你的账号输入有问题，请重新登录")
            return 0
        post_url = 'https://www.zhihu.com/login/email'
        postdata = {
            '_xsrf': _xsrf,
            'password': secret,
            'email': account
        }
    # ------------------------------------------------------------------------------------------------------
    # @ no auth code
    login_page = session.post(post_url, data=postdata, headers=headers, proxies=proxies)
    login_code = login_page.json()
    if login_code['r'] == 1:
        # @ need auth code
        postdata["captcha"] = get_captcha()
        login_page = session.post(post_url, data=postdata, headers=headers, proxies=proxies)
        login_code = login_page.json()
        print(login_code['msg'])
    # @ save cookies
    session.cookies.save()


try:
    input = raw_input
except:
    pass

# ------------------------------------------------------------------------------------------------------
# @ main
if __name__ == '__main__':
    session.cookies.clear()
    if isLogin():
        print('您已经登录')
    else:
        # account = input('请输入你的用户名\n>  ')
        # secret = input("请输入你的密码\n>  ")
        account = "15858127547@139.com"
        secret = "50948612"
        login(secret, account)
