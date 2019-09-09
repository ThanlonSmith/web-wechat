# coding:utf-8
from flask import Flask, render_template
import time
import requests
import re

app = Flask(__name__)


@app.route('/login')
def login():
    '''
    python的时间戳：
     In [1]: import time
     In [2]: time.time()
     Out[2]: 1566619808.3663833
     微信的时间戳：1566619911202
    '''
    ctime = int(time.time() * 1000)
    qcode_url = 'https://login.wx.qq.com/jslogin?appid=wx782c26e4c19acffb&redirect_uri=https%3A%2F%2Fwx.qq.com%2Fcgi-bin%2Fmmwebwx-bin%2Fwebwxnewloginpage&fun=new&lang=zh_CN&_={0}'.format(
        ctime)
    rep = requests.get(
        url=qcode_url,
    )
    # print(rep.text)
    qcode = re.findall('uuid = "(.*)";', rep.text)[0]
    # print(qcode)
    return render_template('login.html', qcode=qcode)


if __name__ == '__main__':
    app.run()
