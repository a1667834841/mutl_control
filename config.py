# coding: utf-8
import os
import threading
import time
import uiautomator2 as u2
import secrets
import sqlite3
import pymysql
from datetime import date
from requests_html import HTMLSession
from adbutils import adb

# 全局本地变量

GLOBAL_LOCAL_VARIABLES = threading.local()


SESSION = HTMLSession()
MY_CONN = sqlite3.connect('records.db', timeout=10, check_same_thread=False)
MY_CURSOR = MY_CONN.cursor()
MYSQL_DB = pymysql.connect(host='127.0.0.1',
                           port=3306,
                           user='root',
                           password='root',
                           database='xxqg'
                           )
MYSQL_CURSOR = MYSQL_DB.cursor()

PUSHPUSH_TOKEN = 'XXXXXX'  # 在pushpush网站中可以找到
TODAY = date.today()
MAX_TRY = 1  # 所有任务是否都完成,没有完成尝试的次数
MOBILE_TYPE = "default"  # 手机型号
# adb的路径
ADB_PATH = "D:\\install\\platform-tools_r34.0.4-windows\\platform-tools\\adb.exe"
SCHEDULE_TIME = "10:30"

# 百度ocr
API_KEY = 'FrUX84vCV2zfrNCbI1ikxFVs'
SECRET_KEY = 'C33VZj2stHiYI8VU4H49g797iqtR2hCG'
OCR_URL = "https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic"
TOKEN_URL = 'https://aip.baidubce.com/oauth/2.0/token'
# TWO_FOUR_ANSWER = 'https://raw.gh.fakev.cn/Pandaver/XXQG_TiKu_Transform/main/question'
TWO_FOUR_ANSWER = 'https://fastly.jsdelivr.net/gh/mondayfirst/XXQG_TiKu@main/%E9%A2%98%E5%BA%93_%E6%8E%92%E5%BA%8F%E7%89%88.json'
CHALLENGE_ANSWER = 'https://raw.githubusercontent.com/mondayfirst/XXQG_TiKu/main/%E9%A2%98%E5%BA%93_%E6%8E%92%E5%BA%8F%E7%89%88.json'
SCORE_TIMES = 3
# 登录手机号
ACCOUNTS = ['13217913287', 'a13014483325']
# 登录密码
PWD = 'a13014483325'