# coding: utf-8
import threading
import config

lock = threading.Lock()


def find_accounts_from_db():
    str = "SELECT mobile,password FROM accounts"
    rows = config.MY_CURSOR.execute(str)
    return rows


def get_record_from_db(mobile, date, key):
    str = "SELECT id FROM records WHERE date='%s' AND key='%s' AND mobile='%s'" % (
        date, key, mobile)
    rows = config.MY_CURSOR.execute(str)
    for row in rows:
        return row[0]
    return None


def insert_record_to_db(mobile, date, key):
    str = "INSERT INTO records (DATE,KEY,MOBILE) VALUES ('%s','%s','%s')" % (
        date, key, mobile)
    config.MY_CURSOR.execute(str)
    config.MY_CONN.commit()


def insert_article_to_db(mobile, title):
    str = "INSERT INTO read_article (TITLE,MOBILE) VALUES ('%s','%s')" % (
        title, mobile)
    config.MY_CURSOR.execute(str)
    config.MY_CONN.commit()


def find_article_from_db(mobile):
    str = "SELECT TITLE FROM read_article WHERE mobile='%s'" % (mobile)
    rows = config.MY_CURSOR.execute(str)
    result = []
    for row in rows:
        result.append(row[0])
    return result


def get_version_from_db(md5, key):
    str = "SELECT id FROM version WHERE md5='%s' AND key='%s'" % (md5, key)
    rows = config.MY_CURSOR.execute(str)
    for row in rows:
        return row[0]
    return None


def insert_version_to_db(md5, key):
    str = "INSERT INTO version (md5,KEY) VALUES ('%s','%s')" % (md5, key)
    config.MY_CURSOR.execute(str)
    config.MY_CONN.commit()


def get_two_four_question_from_db(question, options):
    str = "SELECT answer FROM two_four_question WHERE question LIKE '%s'" % (
        '%' + question + '%')
    rows = config.MY_CURSOR.execute(str)
    for row in rows:
        if row[0] in options:
            print("数据库查询得答案："+row[0])
            return row[0]
    return None


def get_challenge_answer_from_db(question, options):
    question = question.replace("\xa0", "").replace(" ", "")
    str = "SELECT answer FROM challenge_question WHERE question LIKE '%s'" % (
        '%' + question + '%')
    rows = config.MY_CURSOR.execute(str)
    for row in rows:
        for optionIndex in range(len(options)):
            if row[0] in options[optionIndex]:
                print("数据库查询得答案："+options[optionIndex])
                return optionIndex, options[optionIndex]
    return 0, None


def get_challenge_question_from_db(question):
    str = "SELECT answer FROM challenge_question WHERE question = '%s'" % (
        question)
    rows = config.MY_CURSOR.execute(str)
    for row in rows:
        return row[0]
    return None


def insert_challenge_question_to_db(question, answer):
    str = "INSERT INTO challenge_question (question,answer) VALUES ('%s','%s')" % (
        question, answer)
    config.MY_CURSOR.execute(str)
    config.MY_CONN.commit()


def has_none_step(all_step, mobile):
    try:
        lock.acquire(True)
        str = "SELECT id FROM records WHERE date='%s' and mobile='%s'" % (
            config.TODAY, mobile)
        i = 0
        rows = config.MY_CURSOR.execute(str)
        for row in rows:
            i = i + 1
        if (len(all_step) == i):
            return True
    finally:
        lock.release()
    return False
