# coding: utf-8
from datetime import date
import os,sys
import re
sys.path.append(os.getcwd())
import traceback
from scripts.qg.answer import AnswerHelper

# from answer import *
import os
import sys
# pwd = os.getcwd()
# sys.path.append(pwd)
# sys.path.append(pwd+"\\answer")
# import AnswerHelper
from db import DBHelper
import time
import random
from PIL import Image
from scripts.qg.constant import XXQG_DAILY_ANSWER_ACTIVITY
from util import SimulateHelper,QuestionUtil
import logging

from util.UiUtil import is_i_want_answer_page


# ===== 虚拟页面 =====

# 挑战答题
XXQG_CHALLENGE_ACTIVITY = "challenge-score"

# 每日答题
XXQG_DAILY_ACTIVITY = "daily"

# 四人赛
XXQG_FOUR_ACTIVITY = "best"

# 双人赛
XXQG_DOUBLE_ACTIVITY = "friend"

# 异常activity
EXCEPTION_ACTIVITY = "com.alibaba.wireless.security.open.middletier.fc.ui.ContainerActivity"



def answer(login_user, vd,d):
    mobile = login_user.phone
    # 去积分页面
    SimulateHelper.click_question(d)
    logging.info("进入答题页面")
    if d(text="去看看").exists(timeout=2):
        views = d(className="android.widget.TextView")
        
        i = 0
        for view in views:
            # print(view.info["text"])
            if "错题集" in view.info["text"]:
                view.click()
                i = i + 1
    # x, y = SimulateHelper.getMobileXY("two_fight_question")
    # d.click(x, y)
    # print(x, y)
    # time.sleep(3)
    # 每日答题
    # has_daily_question = DBHelper.get_record_from_db(
    #     mobile, date.today(), "daily_question")
    # if has_daily_question is None:
    #     if __daily_question__():
    #         DBHelper.insert_record_to_db(
    #             mobile, date.today(), "daily_question")

    # time.sleep(8)
    # 专项答题
    # has_special_question = DBHelper.get_record_from_db(mobile, date.today(), "special_question")
    # if has_special_question is None:
    #     if __special_question__():
    #         DBHelper.insert_record_to_db(mobile, date.today(), "special_question")
    
    # 每日答题
    has_daily_question = DBHelper.get_record_from_db(
        mobile, date.today(), "daily_question")
    if has_daily_question is None:
        if __daily_question__(d):
            DBHelper.insert_record_to_db(
                mobile, date.today(), "daily_question")
    else:
        print("今日"+mobile+"已经完成每日答题")
            

    task_type = task_type_current(d)
    print("当前任务类型:"+task_type)
            
    # 双人对战
    has_two_fight_question = DBHelper.get_record_from_db(
        mobile, date.today(), "two_fight_question")
    # 今日未做双人 且 任务类型是双人对战
    if has_two_fight_question is  None and XXQG_DOUBLE_ACTIVITY == task_type:
        if __two_fight_question__(d):
            DBHelper.insert_record_to_db(
                mobile, date.today(), "two_fight_question")
        else:
            print("今日"+mobile+"双人对战已完成")                
    # 挑战答题
    if XXQG_CHALLENGE_ACTIVITY == task_type:
        has_challenge_question = DBHelper.get_record_from_db(
            mobile, date.today(), "challenge_question")
        if has_challenge_question is None:
            if __challenge_question__(d):
                DBHelper.insert_record_to_db(
                    mobile, date.today(), "challenge_question")
            else:
                d.press("back")
        else:
            print("今日"+mobile+"挑战答题已完成")

    # 四人对战
    if XXQG_FOUR_ACTIVITY == task_type:
        has_four_fight_question = DBHelper.get_record_from_db(
            mobile, date.today(), "four_fight_question")
        if has_four_fight_question is None:
            is_ok = True
            for i in range(2):
                is_ok = __four_fight_question__(d)
            if is_ok:
                DBHelper.insert_record_to_db(
                    mobile, date.today(), "four_fight_question")
        else:
            print("今日"+mobile+"四人对战已完成")
    print("答题结束")
    # time.sleep(1)
    # SimulateHelper.swipe_score_top(d)
    # SimulateHelper.getScore(d)


def __daily_question__(d):
    print("每日答题开始.")
    is_ok = False
    def daily_question_answer():
        views = d(className="android.widget.TextView")
        while len(views) == 0:
            views = d(className="android.widget.TextView")
       

        question_type = QuestionUtil.get_question_type(views)
        # 单选题 多选题 填空题
        question = QuestionUtil.get_question_text(views)
        print(question)
        print(question_type)
        if ("单选题" == question_type):
            list_views = d(className="android.widget.ListView").child(
                className="android.widget.TextView")
            options = QuestionUtil.get_answer_option(list_views)
            index,answer = AnswerHelper.query_answer(question, options)
            if (answer is not None and d(text=answer).exists):
                d(text=answer).click()
            else:
                tips = AnswerHelper.search_answer(question, options)
                d(text=tips).click()
  
            if (d(text="下一题").exists(timeout=5)):
                d(text="下一题").click()
            if (d(text="完成").exists(timeout=5)):
                d(text="完成").click()
        elif ("多选题" == question_type):
            list_views = d(className="android.widget.ListView").child(
                className="android.widget.TextView")
            options = QuestionUtil.get_answer_option(list_views)
            for option in options:
                d(text=option).click()
            if (d(text="下一题").exists(timeout=5)):
                d(text="下一题").click()
            if (d(text="完成").exists(timeout=5)):
                d(text="完成").click()
        elif ("填空题" == question_type):
            answer = AnswerHelper.query_answer(question)
            # print("查询的答案是:%s" % answer)
            if (answer is not None):
                d(text=question_type).click()
                time.sleep(3)
                d(text=question).sibling(text="")[2].click()
                SimulateHelper.send_keys("xx",d)
                # d(text="确定").click()
                # time.sleep(5)
                if (d(text="下一题").exists(timeout=5)):
                    d(text="下一题").click()
                if (d(text="完成").exists(timeout=5)):
                    d(text="完成").click()
            else:
                print(question)
                d(text="查看提示").click()
                time.sleep(3)
                tmp = d(textStartsWith=question)
                if (len(tmp) >= 2):
                    tips = tmp[1].info['text']
                    print(tips)
                    tips = tips.replace(question, "")
                    d(text=question_type).click()
                    time.sleep(3)
                    d(text=question).sibling(text="")[2].click()
                    SimulateHelper.send_keys(tips)
                    d(text="确定").click()
                    time.sleep(5)
                    if (d(text="下一题").exists(timeout=5)):
                        d(text="下一题").click()
                    if (d(text="完成").exists(timeout=5)):
                        d(text="完成").click()
                else:
                    d(text=question_type).click()
                    time.sleep(3)
                    d(text=question).sibling(text="")[2].click()
                    SimulateHelper.send_keys("I Have No Answer")
                    d(text="确定").click()
                    time.sleep(5)
                    if (d(text="下一题").exists(timeout=5)):
                        d(text="下一题").click()
                    if (d(text="完成").exists(timeout=5)):
                        d(text="完成").click()
    SimulateHelper.click_daily_question(d)
    for i in range(5):
        try:
            daily_question_answer()
        except Exception as e:
            error = traceback.format_exc()
            print(error)
            d.press("back")
            is_ok = False
            break
    
    while d.app_current()["activity"] != XXQG_DAILY_ANSWER_ACTIVITY:
        print("答题未结束，当前页面：",d.app_current()["activity"])
    
    print("每日答题结束.")
    is_ok = True
    d.press("back")
    return is_ok


# def __special_question__():
#     print("专项答题开始.")

#     def special_question_answer():
#         time.sleep(5)
#         views = Config.DRIVER(className="android.view.View")
#         question_type = QuestionUtil.get_question_type(views)
#         question = QuestionUtil.get_question_text(views)
#         print(question)
#         SimulateHelper.swipe_down()
#         if question_type is None:
#             return
#         if ("单选题" in question_type):
#             list_views = Config.DRIVER(className="android.widget.ListView").child(
#                 className="android.view.View")
#             options = QuestionUtil.get_answer_option(list_views)
#             answer = AnswerHelper.query_answer(question, options)
#             if (answer is not None and Config.DRIVER(text=answer).exists):
#                 Config.DRIVER(text=answer).click()
#             else:
#                 tips = AnswerHelper.search_answer(question, options)
#                 Config.DRIVER(text=tips).click()
#             time.sleep(5)
#             if (Config.DRIVER(text="下一题").exists(timeout=5)):
#                 Config.DRIVER(text="下一题").click()
#             if (Config.DRIVER(text="完成").exists(timeout=5)):
#                 Config.DRIVER(text="完成").click()
#         elif ("多选题" in question_type):
#             list_views = Config.DRIVER(className="android.widget.ListView").child(
#                 className="android.view.View")
#             options = QuestionUtil.get_answer_option(list_views)
#             for option in options:
#                 Config.DRIVER(text=option).click()
#             time.sleep(5)
#             if (Config.DRIVER(text="下一题").exists(timeout=5)):
#                 Config.DRIVER(text="下一题").click()
#             if (Config.DRIVER(text="完成").exists(timeout=5)):
#                 Config.DRIVER(text="完成").click()
#         elif ("填空题" in question_type):
#             answer = AnswerHelper.query_answer(question)
#             print("查询的答案是:%s" % answer)
#             if (answer is not None):
#                 Config.DRIVER(text=question_type).click()
#                 time.sleep(3)
#                 Config.DRIVER(text=question).sibling(text="")[2].click()
#                 SimulateHelper.send_keys(answer)
#                 if (Config.DRIVER(text="下一题").exists(timeout=5)):
#                     Config.DRIVER(text="下一题").click()
#                 if (Config.DRIVER(text="完成").exists(timeout=5)):
#                     Config.DRIVER(text="完成").click()
#             else:
#                 print(question)
#                 Config.DRIVER(text="查看提示").click()
#                 time.sleep(3)
#                 tmp = Config.DRIVER(textStartsWith=question)
#                 if (len(tmp) >= 2):
#                     tips = tmp[1].info['text']
#                     print(tips)
#                     tips = tips.replace(question, "")
#                     Config.DRIVER(text=question_type).click()
#                     time.sleep(3)
#                     Config.DRIVER(text=question).sibling(text="")[2].click()
#                     SimulateHelper.send_keys(tips)
#                     if (Config.DRIVER(text="下一题").exists(timeout=5)):
#                         Config.DRIVER(text="下一题").click()
#                     if (Config.DRIVER(text="完成").exists(timeout=5)):
#                         Config.DRIVER(text="完成").click()
#                 else:
#                     Config.DRIVER(text=question_type).click()
#                     time.sleep(3)
#                     Config.DRIVER(text=question).sibling(text="")[2].click()
#                     SimulateHelper.send_keys("I Have No Answer")
#                     if (Config.DRIVER(text="下一题").exists(timeout=5)):
#                         Config.DRIVER(text="下一题").click()
#                     if (Config.DRIVER(text="完成").exists(timeout=5)):
#                         Config.DRIVER(text="完成").click()

#     Config.DRIVER.click(0.864, 0.702)
#     time.sleep(5)
#     is_ok = True

#     def search_start_question(i):
#         if (Config.DRIVER(text="开始答题").exists(timeout=2)):
#             Config.DRIVER(text="开始答题").click()
#             for i in range(10):
#                 try:
#                     special_question_answer()
#                 except:
#                     Config.DRIVER.press("back")
#                     break
#             time.sleep(5)
#             Config.DRIVER.press("back")
#         else:
#             if i > Config.SCORE_TIMES:
#                 Config.DRIVER.press("back")
#             else:
#                 SimulateHelper.swipe_down()
#                 search_start_question(i + 1)
#     search_start_question(0)
#     Config.DRIVER.press("back")
#     print("专项答题结束.")
#     return is_ok


# def weekly_question():
#     print("每周答题开始.")

#     def weekly_question_answer():
#         time.sleep(5)
#         views = driver(className="android.view.View")
#         question_type = __get_question_type__(views)
#         question = __get_question__(views)
#         print(question)
#         if question_type is None:
#             return
#         if ("单选题" in question_type):
#             list_views = driver(className="android.widget.ListView").child(className="android.view.View")
#             options = __get_answer__(list_views)
#             answer = _query_api_(question, options)
#             if (answer is not None and driver(text=answer).exists):
#                 driver(text=answer).click()
#             else:
#                 tips = _search_(question, options)
#                 driver(text=tips).click()
#             time.sleep(5)
#             if (driver(text="确定").exists(timeout=5)): driver(text="确定").click()
#             if (driver(text="下一题").exists(timeout=5)): driver(text="下一题").click()
#             if (driver(text="完成").exists(timeout=5)): driver(text="完成").click()
#         elif ("多选题" in question_type):
#             list_views = driver(className="android.widget.ListView").child(className="android.view.View")
#             options = __get_answer__(list_views)
#             for option in options:
#                 driver(text=option).click()
#             time.sleep(5)
#             if (driver(text="确定").exists(timeout=5)): driver(text="确定").click()
#             if (driver(text="下一题").exists(timeout=5)): driver(text="下一题").click()
#             if (driver(text="完成").exists(timeout=5)): driver(text="完成").click()
#         elif ("填空题" in question_type):
#             answer = _query_api_(question)
#             print("查询的答案是:%s" % answer)
#             if (answer is not None):
#                 driver(text=question_type).click()
#                 time.sleep(3)
#                 driver(text=question).sibling(text="")[2].click()
#                 send_keys(answer)
#                 if (driver(text="确定").exists(timeout=5)): driver(text="确定").click()
#                 if (driver(text="下一题").exists(timeout=5)): driver(text="下一题").click()
#                 if (driver(text="完成").exists(timeout=5)): driver(text="完成").click()
#             else:
#                 print(question)
#                 driver(text="查看提示").click()
#                 time.sleep(3)
#                 tmp = driver(textStartsWith=question)
#                 if (len(tmp) >= 2):
#                     tips = tmp[1].info['text']
#                     print(tips)
#                     tips = tips.replace(question, "")
#                     driver(text=question_type).click()
#                     time.sleep(3)
#                     driver(text=question).sibling(text="")[2].click()
#                     send_keys(tips)
#                     if (driver(text="确定").exists(timeout=5)): driver(text="确定").click()
#                     if (driver(text="下一题").exists(timeout=5)): driver(text="下一题").click()
#                     if (driver(text="完成").exists(timeout=5)): driver(text="完成").click()
#                 else:
#                     driver(text=question_type).click()
#                     time.sleep(3)
#                     driver(text=question).sibling(text="")[2].click()
#                     send_keys("我不知道这个答案")
#                     if (driver(text="确定").exists(timeout=5)): driver(text="确定").click()
#                     if (driver(text="下一题").exists(timeout=5)): driver(text="下一题").click()
#                     if (driver(text="完成").exists(timeout=5)): driver(text="完成").click()

#     x,y = getMobileXY("weekly_question")
#     x, y = getXY(x,y)
#     driver.click(x, y)
#     time.sleep(5)
#     if (driver(text="未作答").exists(timeout=5)):
#         driver(text="未作答").click()
#         for i in range(5):
#             weekly_question_answer()
#         time.sleep(5)
#         driver(text="返回").click()
#     driver.press("back")
#     print("每周答题结束.")


def __two_fight_question__(d):

    # 准备进入双人对战
    imgViews = d(className="android.widget.Image")
    for imgView in imgViews:
        if "friend" in imgView.info["text"]:
            imgView.click()
            break
    
    while (not d(text="随机匹配").exists(timeout=1)):
        print("等待进入双人对战页面")

    print("进入双人对战对战页面")
    time.sleep(1)
    textViews = d(className="android.widget.TextView")
    for i in range(0,len(textViews)):
        if "随机匹配" in textViews[i].info["text"]:
            textViews[i-1].click()
            print("点击随机匹配")
            break

    # 您已超过今日对战次数，请明日再来 
    if d(text="知道了").exists(timeout=5):
        d(text="知道了").click()
        return True
    
    # 等待页面出现文字包含00:字符
    time.sleep(1)
    current = d.app_current()
    # print(current)
    while (current["activity"] == EXCEPTION_ACTIVITY):
        time.sleep(1)
        print("等待进入答题页面")
        current = d.app_current()
    time.sleep(1)

    # 等待进入答题页面
    textViews = d(className="android.widget.TextView")
    while (textViews.count > 0):
        enterAnswer = False
        for i in range(0,len(textViews)):
            if i == 3 and textViews[i].info["text"] == "0":
                enterAnswer = True
                break
        if enterAnswer:
            break
        textViews = d(className="android.widget.TextView")

    def two_fight_answer(d):
        success = False
        # time.sleep(9)
        score = "0"
        try:
            while score != "100":
                
                if textViews.count == 0:
                    time.sleep(1)
                    continue
                nameView = textViews[2]
                scoreView = textViews[3]
                name = nameView.info["text"]
                score = scoreView.info["text"]
                print(name+"当前得分:" + score)
                optionsExisits = d(
                    className="android.widget.RadioButton").exists(timeout=10)
                if not optionsExisits:
                    raise Exception("答题页面找不到对应选项")
                optionsEL = d(
                    className="android.widget.RadioButton")
                try:
                    time.sleep(0.1)
                    d().screenshot().save(d.serial+"ocr.png")
                    (question, options) = AnswerHelper.ocr(d.serial+"ocr.png")
                    if question is not None and len(question) > 0 and len(options) > 0:
                        print("题目:" + question)
                        answer = DBHelper.get_two_four_question_from_db(
                            question, options)
                        print("答案是" + answer)
                        if (answer is not None):
                            i = 0
                            for option in options:
                                if answer in option:
                                    i = options.index(option)
                                    break
                            optionsEL[i].click()
                        else:
                            optionsEL[random.randint(
                                0, len(optionsEL) - 1)].click()
                    else:
                        return True
                except:
                    optionsEL[0].click()
            success = int(score) > 100
        except:
            traceback.print_exc()
            print("出错")
            return success
        finally:
            d.press("back")
        return success

    is_ok = two_fight_answer(d)
    
    while (is_i_want_answer_page(d)):
        d.press("back")
        if (d(description="退出").exists(timeout=5)):
            d(description="退出").click()
    print("双人对战结束.")
    return is_ok


def __four_fight_question__(d):
    # 准备进入双人对战
    imgViews = d(className="android.widget.Image")
    for imgView in imgViews:
        if "best" in imgView.info["text"]:
            imgView.click()
            time.sleep(1)
            break
    
    while (not d(text="开始比赛").exists(timeout=1)):
        print("等待进入四人对战页面")
    d(text="开始比赛").click()
    
    print("四人对战开始.")
    time.sleep(18)
    textViews = d(className="android.widget.TextView")
    while (textViews.count > 0):
        enterAnswer = False
        for i in range(0,len(textViews)):
            if i == 3 and textViews[i].info["text"] == "0":
                enterAnswer = True
                break
        if enterAnswer:
            break
        textViews = d(className="android.widget.TextView")

    def four_fight_answer(d):
        score = "0"
        try:
            while score != "100":
                textViews = d(className="android.widget.TextView")
                score = textViews[3].info['text']
                print("当前得分:" + score)
                optionsEL = d(
                    className="android.widget.RadioButton")
                if len(optionsEL) == 0:
                    d.press("back")
                try:
                    time.sleep(0.5)
                    d().screenshot().save("ocr.png")
                    (question, options) = AnswerHelper.ocr("ocr.png")
                    if question is not None and len(question) > 0 and len(options) > 0:
                        print("题目:" + question)
                        answer = DBHelper.get_two_four_question_from_db(
                            question, options)
                        if (answer is not None):
                            print("答案是" + answer)
                            i = 0
                            for option in options:
                                if answer in option:
                                    i = options.index(option)
                                    break
                            optionsEL[i].click()
                        else:
                            optionsEL[random.randint(
                                0, len(optionsEL) - 1)].click()
                    else:
                        optionsEL[random.randint(
                            0, len(optionsEL) - 1)].click()
                except:
                    optionsEL[random.randint(0, len(optionsEL) - 1)].click()

        except:
            traceback.print_exc()
            print("出错")

    four_fight_answer(d)

    print("四人对战结束.")
    while (is_i_want_answer_page(d)):
        d.press("back")
    is_ok = True
    return is_ok


def find_chanlleng_question(d):
    """
    找到挑战答题的题目view
    """
    isFindQuersion = False
    # 1. 虚拟机通过ocr识别题目
    views = d(className="android.view.View")
    questionView = views[3]
    question = questionView.info['contentDescription']
    if question is not None and len(question) > 0:
        options = find_chanlleng_options_by_ocr(d)
        return question,options
    
    # 2. 小米手机 通过文本查找题目
    def find_options(d,quesionView):
        options = []
        optionViews = quesionView.down(className="android.widget.ListView").child(className="android.view.View")
        logger.info("optionViews size:"+str(len(optionViews)))
        for viewsub in optionViews:
            if viewsub is not None and viewsub.info['text'] is not None and len(viewsub.info['text']) > 0:
                options.append(viewsub.info['text'])
            elif viewsub.child(className="android.widget.TextView")[0] is not None and viewsub.child(className="android.widget.TextView")[0].info['text'] is not None and len(viewsub.child(className="android.widget.TextView")[0].info['text']) > 0:
                options.append(viewsub.child(className="android.widget.TextView")[0].info['text'])
            
        return options

    question = ""
    for view in views:
        if view.info['text'] is not None and len(view.info['text']) > 0 and (view.info['text'].find("来源：") > 0 or view.info['text'].find(" ") > 0):
            question = view.info['text']
            questionView = view
            isFindQuersion = True
            break
    if isFindQuersion:
        options = find_options(d,questionView)
        return question,options
            
    
    # 未找到题目,抛出异常
    raise Exception("未找到挑战答题的题目")

def find_chanlleng_options_by_ocr(d):
        list_views = d(className="android.widget.ListView").child(
        className="android.view.View")
        options = []
        d.screenshot().save(d.serial+"raw.png")

        x1 = list_views[0].info["bounds"]["left"]
        y1 = list_views[0].info["bounds"]["top"]

        x2 = list_views[len(list_views)-1].info["bounds"]["right"]
        y2 = list_views[len(list_views)-1].info["bounds"]["bottom"]

        image = Image.open(d.serial+"raw.png")
        # 截取指定区域的图像
        region_image = image.crop((x1, y1, x2, y2))
        # 保存图像
        region_image.save(d.serial+'option.png')
        return AnswerHelper.ocrOptions(d.serial+"option.png")



def __challenge_question__(d):
    logger.info("挑战答题开始.")
    time.sleep(1)
    def challenge_question_answer(d, creactNum):

        if creactNum >=3:
            return True

        isQuit = False
        question,options = find_chanlleng_question(d)
        logger.info("挑战题目："+question)
        list_views = d(className="android.widget.ListView").child(
        className="android.view.View")

        if creactNum == 3:
            # 快速失敗
            d(text=options[0]).click()
            return



        answerIndex, answer = AnswerHelper.query_answer(question, options)
        if (answer is not None and answerIndex is not None):
            print("答案是" + answer + " 选项是:" + str(answerIndex) +
                  str(list_views[answerIndex].info["bounds"]))
            # d.click(list_views[answerIndex].info["bounds"]
            #         ["left"], list_views[answerIndex].info["bounds"]["bottom"] + answerIndex * 70)
            # list_views[answerIndex].click()
            d(text=answer).click()
        else:
            tips = AnswerHelper.search_answer(question, options)
            d(text=tips).click()
        if (d(text="结束本局").exists(timeout=5)) or (d(description="结束本局").exists(timeout=5)):
            # 查询答对题数
            num = d(text="结束本局").down().info['text']
            # num = views[7].info['contentDescription']
            # 正则表达式  本次答对 0 题 匹配出 0
            pattern = r'\d+'
            matches = re.findall(pattern, num)
            if matches:
                print("本次答对" + matches[0] + "题")
                if int(matches[0]) > 2:
                    return True
                else:
                    # 重新答题
                    if d(description="结束本局").exists(timeout=500):
                        d(description="结束本局").click()
                        if d(description="再来一局").exists(timeout=500):
                            d(description="再来一局").click()
                            # 重置
                            creactNum = 0
                            return False
            isQuit = True
        return isQuit
    SimulateHelper.click_challenge_question(d)
    time.sleep(3)

    # 选择题目类型
    # d(description="时事政治").click()
    # time.sleep(10)
    is_ok = True
    creactNum = 0
    while (creactNum < 3):
        try:
            if challenge_question_answer(d, creactNum) is True:
                break
            creactNum = creactNum + 1
        except:
            is_ok = False
            traceback.print_exc()
            print("出错")
            continue
    while (True):
        if d(text="结束本局").exists(timeout=0.5):
            print("结束本局")
            d(text="结束本局").click()
            break
        if d(text="再来一局").exists(timeout=0.5):
            break
         # 尝试快速失败 随机数 500~850
        d.click(300,random.randint(800,1250))
    while (True):
        if d(text="再来一局").exists(timeout=5):
            print("出现 再来一局")
            d.press("back")
            if d(text="退出后作答历史将不会保存").exists(timeout=5):
                d(text="退出").click()
            break
        time.sleep(1)

    d.press("back")
    print("挑战答题结束.")
    return is_ok


def task_type_current(d):
    """
    当前任务类型
    """
    # 检查当前页面是否属于答题总页面
    if not is_i_want_answer_page(d):
        return None
    
    # 遍历
    answer_types = ["challenge-score","best","friend"]
    imgViews = d(className="android.widget.Image")

    for imgView in imgViews:
        for answer_type in answer_types:
            if answer_type in imgView.info["text"]:
                return answer_type
    return None

logger = logging.getLogger(__name__)