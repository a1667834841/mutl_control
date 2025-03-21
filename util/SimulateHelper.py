# coding: utf-8
import re
import threading
import config.config as Config
import time
import random
import os
import logging
WIDTH = 0
HEIGHT = 0

local_var = threading.local()


def send_keys(tips, driver):
    # driver = local_var.driver
    time.sleep(5)
    driver.set_fastinput_ime(True)
    time.sleep(5)
    driver.send_keys(tips)


def swipe_down():

    x1 = random.randint(int(WIDTH / 10) * 3, int(WIDTH / 10) * 7)
    y1 = random.randint(int(HEIGHT / 20) * 16, int(HEIGHT / 20) * 17)
    x2 = random.randint(int(WIDTH / 10) * 3, int(WIDTH / 10) * 7)
    y2 = random.randint(int(HEIGHT / 20) * 2, int(HEIGHT / 20) * 3)
    drag_str = Config.ADB_PATH + ' shell input swipe ' + str(x1) + ' ' + str(y1) + ' ' + str(
        x2) + ' ' + str(y2)
    os.system(drag_str)
    time.sleep(5)


def getXY(x, y):
    return (WIDTH / 560 - x, HEIGHT / 1800 - 1 - y)


def goto_score_page(d):
    d(resourceId="cn.xuexi.android:id/comm_head_xuexi_score").click()
    time.sleep(2)
    return getScore(d)


def getScore(d):

    score = 0
    list_views = d(className="android.widget.TextView")
    for scoreView in list_views:
        if scoreView is None:
            continue
        scoreStr = scoreView.info["text"]
        if scoreStr is None or scoreStr == "" or "今日已累积" not in scoreStr:
            continue
        pattern = r'\d+'
        matches = re.findall(pattern, scoreStr)
        if matches:
            logger.info("今日得分："+matches[0])
            score = int(matches[0])
            break
    return score


def swipe_question(serial):
    x1 = WIDTH / 10 * 3
    y1 = HEIGHT / 20 * 12
    x2 = WIDTH / 10 * 3
    y2 = HEIGHT / 20 * 2
    drag_str = Config.ADB_PATH + ' -s ' + serial + ' shell input swipe ' + str(x1) + ' ' + str(y1) + ' ' + str(
        x2) + ' ' + str(y2)
    os.system(drag_str)
    time.sleep(2)

def click_question(d):
    """
    点击 我要答题
    """
    d.click(539, 835)
    time.sleep(1)

def click_challenge_question(d):
    """
    已经进入 我要答题 点击 挑战答题
    """
    click_by_image("challenge",d)
    time.sleep(2)
    click_by_image("total",d)

def click_daily_question(d):
    """
    已经进入 我要答题 点击 每日答题
    """
    d(text="每日答题").click()
    time.sleep(2)

def click_by_image(text,d):
    """
    根据图片点击
    """
    isFind = False
    imges = d(className="android.widget.Image")
    count = 0
    while count < 10:
        imges = d(className="android.widget.Image")
        count += 1
        for img in imges:
            if text in img.info["text"]:
                img.click()
                isFind = True
                break
        if isFind:
            break
        time.sleep(2)
    
    if not isFind:
        raise Exception("没有找到"+text+"对应的的图片")



def swipe_score_top(d):
    x2 = WIDTH / 10 * 3
    y2 = HEIGHT / 20 * 12
    x1 = WIDTH / 10 * 3
    y1 = HEIGHT / 20 * 2
    drag_str = Config.ADB_PATH + ' -s ' + d.serial + ' shell input swipe ' + str(x1) + ' ' + str(y1) + ' ' + str(
        x2) + ' ' + str(y2)
    os.system(drag_str)
    time.sleep(2)


def swipe_down_small():
    x1 = 300
    y1 = 1600
    x2 = 200
    y2 = 1300
    drag_str = Config.ADB_PATH + ' shell input swipe ' + str(x1) + ' ' + str(y1) + ' ' + str(
        x2) + ' ' + str(y2)
    os.system(drag_str)
    time.sleep(5)


def getMobileXY(key):
    MI_11_XY = {
        # 0.851, 0.163
        "daily_question": (2.04, 0.28),
        # 0.858, 0.305
        "special_question": (2.04, 0.13),
        # 0.895, 0.728
        "two_fight_question": (2.0, -0.3),
        # 0.851, 0.588
        "four_fight_question": (2.04, -0.16),
        # 0.888, 0.458
        "challenge_question": (2.0, 0),
        # 0.885, 0.858
        "subscribe": (2.01, -0.42),
        # 0.871, 0.874
        "weekly_question": (2.02, -0.43),
    }
    MI_6_XY = {
        # 0.9, 0.514
        "daily_question": (1.05, -0.428),
        # 0.897, 0.696
        "special_question": (1.02, -0.6),
        # 0.894, 0.934
        "two_fight_question": (1.02, -0.85),
        # 0.867, 0.901
        "four_fight_question": (1.05, -0.82),
        # 0.878, 0.915
        "challenge_question": (1.05, -0.83),

        "subscribe": (2.01, -0.42),
        "weekly_question": (2.02, -0.43),
    }
    default = {
        # 0.9, 0.514
        "daily_question": (1.05, -0.428),
        # 0.897, 0.696
        "special_question": (1.02, -0.6),
        # 0.894, 0.934
        "two_fight_question": (0.874, 0.287),
        # 0.867, 0.901
        "four_fight_question": (0.868, 0.297),
        # 0.878, 0.915
        "challenge_question": (0.868, 0.297),

        "subscribe": (2.01, -0.42),
        "weekly_question": (2.02, -0.43),
    }

    if Config.MOBILE_TYPE == "MI11":
        return MI_11_XY[key]
    elif Config.MOBILE_TYPE == "default":
        return default[key]
    else:
        return MI_6_XY[key]
logger = logging.getLogger(__name__)