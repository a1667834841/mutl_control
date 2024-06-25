# coding: utf-8
import io
import re
import traceback
from answer.AnswerHelper import *
from db import DBHelper
import config
import time
import random
from PIL import Image
from util import SimulateHelper,QuestionUtil
import logging



def answer(login_user, vd,d):
    mobile = login_user.phone
    # 去积分页面
    serial = d.serial
    SimulateHelper.click_question(d)
    logging.info("进入答题页面")
    # x, y = SimulateHelper.getMobileXY("two_fight_question")
    # d.click(x, y)
    # print(x, y)
    # time.sleep(3)
    # 每日答题
    # has_daily_question = DBHelper.get_record_from_db(
    #     mobile, Config.TODAY, "daily_question")
    # if has_daily_question is None:
    #     if __daily_question__():
    #         DBHelper.insert_record_to_db(
    #             mobile, Config.TODAY, "daily_question")

    # time.sleep(8)
    # 专项答题
    # has_special_question = DBHelper.get_record_from_db(mobile, Config.TODAY, "special_question")
    # if has_special_question is None:
    #     if __special_question__():
    #         DBHelper.insert_record_to_db(mobile, Config.TODAY, "special_question")
    # 挑战答题
    has_challenge_question = DBHelper.get_record_from_db(
        mobile, config.TODAY, "challenge_question")
    if has_challenge_question is None:
        if __challenge_question__(d):
            DBHelper.insert_record_to_db(
                mobile, config.TODAY, "challenge_question")
        else:
            d.press("back")
    
    # 每日答题
    has_daily_question = DBHelper.get_record_from_db(
        mobile, config.TODAY, "daily_question")
    if has_daily_question is None:
        if __daily_question__(d):
            DBHelper.insert_record_to_db(
                mobile, config.TODAY, "daily_question")


    # if Config.MOBILE_TYPE == "MI6":
    #     SimulateHelper.swipe_down_small()

    # if Config.MOBILE_TYPE == "MI6":
    #     SimulateHelper.swipe_down_small()

    # 双人对战
    # startBtn = d(description="随机匹配")
    # if startBtn.exists(timeout=5):
    #     time.sleep(5)
    #     print("进入 双人对战 随机匹配")
    #     d.click(0.739, 0.482)
    #     has_two_fight_question = DBHelper.get_record_from_db(
    #         mobile, config.TODAY, "two_fight_question")
    #     if has_two_fight_question is None:
    #         if __two_fight_question__(d):
    #             DBHelper.insert_record_to_db(
    #                 mobile, config.TODAY, "two_fight_question")

    # # 四人对战
    # startBtn = d(description="开始比赛")
    # if startBtn.exists(timeout=5):
    #     has_four_fight_question = DBHelper.get_record_from_db(
    #         mobile, config.TODAY, "four_fight_question")
    #     time.sleep(5)
    #     if has_four_fight_question is None:
    #         print("进入 四人赛 随机匹配")
    #         startBtn.click()
    #         is_ok = True
    #         for i in range(2):
    #             is_ok = __four_fight_question__(d)
    #         if is_ok:
    #             DBHelper.insert_record_to_db(
    #                 mobile, config.TODAY, "four_fight_question")
    # print("答题结束")
    # time.sleep(1)
    # SimulateHelper.swipe_score_top(d)
    # SimulateHelper.getScore(d)


def __daily_question__(d):
    print("每日答题开始.")

    def daily_question_answer():
        views = d(className="android.view.View")

        question_type = QuestionUtil.get_question_type(views)
        # 单选题 多选题 填空题
        question = QuestionUtil.get_question_text(views)
        print(question)
        print(question_type)
        if ("单选题" == question_type):
            list_views = d(className="android.widget.ListView").child(
                className="android.view.View")
            options = QuestionUtil.get_answer_option(list_views)
            index,answer = AnswerHelper.query_answer(question, options)
            if (answer is not None and d(text=answer).exists):
                d(text=answer).click()
            else:
                tips = AnswerHelper.search_answer(question, options)
                d(text=tips).click()
            time.sleep(5)
            d(text="确定").click()
            time.sleep(5)
            if (d(text="下一题").exists(timeout=5)):
                d(text="下一题").click()
            if (d(text="完成").exists(timeout=5)):
                d(text="完成").click()
        elif ("多选题" == question_type):
            list_views = d(className="android.widget.ListView").child(
                className="android.view.View")
            options = QuestionUtil.get_answer_option(list_views)
            for option in options:
                d(text=option).click()
            time.sleep(5)
            d(text="确定").click()
            time.sleep(5)
            if (d(text="下一题").exists(timeout=5)):
                d(text="下一题").click()
            if (d(text="完成").exists(timeout=5)):
                d(text="完成").click()
        elif ("填空题" == question_type):
            answer = AnswerHelper.query_answer(question)
            print("查询的答案是:%s" % answer)
            if (answer is not None):
                d(text=question_type).click()
                time.sleep(3)
                d(text=question).sibling(text="")[2].click()
                SimulateHelper.send_keys(answer)
                d(text="确定").click()
                time.sleep(5)
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
    time.sleep(5)
    if d(text="返回"):
        d(text="返回").click()
    print("每日答题结束.")
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
    print("双人对战开始.")
    if d(description="您已超过今日对战次数，请明日再来").exists(timeout=5):
        return True

    def two_fight_answer(d):
        success = False
        time.sleep(5)
        score = "0"
        try:
            while d(description="继续挑战").exists(timeout=3) is False:
                views = d(
                    className="android.view.View")

                if views.count == 0 or views[4] is None:
                    time.sleep(1)
                    continue
                nameView = views[3]
                scoreView = views[4]
                name = nameView.info["contentDescription"]
                score = scoreView.info["contentDescription"]
                print("当前得分:" + score)
                optionsEL = d(
                    className="android.widget.RadioButton")
                if len(optionsEL) == 0:
                    d.press("back")
                try:
                    time.sleep(2)
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
            success = True
        except:
            traceback.print_exc()
            print("出错")
        finally:
            d.press("back")
        return score > "0"

    is_ok = True
    is_ok = two_fight_answer(d)
    time.sleep(1)
    d.press("back")
    time.sleep(1)
    if (d(description="退出").exists(timeout=5)):
        d(description="退出").click()
    print("双人对战结束.")
    return is_ok


def __four_fight_question__(d):
    print("四人对战开始.")

    def four_fight_answer(d):
        # d(text="开始比赛").click()
        # if d(description="开始比赛").click():
        #     print("点击 开始比赛 成功")
        score = "0"
        try:
            while score != "100":
                views = d(className="android.view.View")
                time.sleep(4)
                score = views[10].info['text']
                print("当前得分:" + score)
                optionsEL = d(
                    className="android.widget.RadioButton")
                if len(optionsEL) == 0:
                    d.press("back")
                try:
                    time.sleep(2)
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

    time.sleep(3)
    x, y = SimulateHelper.getMobileXY("four_fight_question")
    # x1, y1 = SimulateHelper.getXY(x, y)
    d.click(x, y)
    time.sleep(3)
    is_ok = True
    four_fight_answer(d)
    d.press("back")
    print("四人对战结束.")
    return is_ok


def __challenge_question__(d):
    print("挑战答题开始.")

    def challenge_question_answer(d, creactNum):
        isQuit = False
        views = d(className="android.view.View")
        questionView = views[3]
        question = questionView.info['contentDescription']
        question = question[:15]
        print(question)
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
        options = AnswerHelper.ocrOptions(d.serial+"option.png")

        answerIndex, answer = AnswerHelper.query_answer(question, options)
        if (answer is not None and answerIndex is not None):
            print("答案是" + answer + " 选项是:" + str(answerIndex) +
                  str(list_views[answerIndex].info["bounds"]))
            d.click(list_views[answerIndex].info["bounds"]
                    ["left"], list_views[answerIndex].info["bounds"]["bottom"] + answerIndex * 70)
            # list_views[answerIndex].click()
            # d(text=answer).click()
        else:
            tips = AnswerHelper.search_answer(question, options)
            d(text=tips).click()
        if (d(description="结束本局").exists(timeout=15)):
            # 查询答对题数
            num = views[7].info['contentDescription']
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
    time.sleep(2)

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
        if d(text="结束本局").exists(timeout=5):
            print("结束本局")
            d(text="结束本局").click()
            break
        time.sleep(1)
        if d(text="再来一局").exists(timeout=5):
            break
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

logger = logging.getLogger(__name__)