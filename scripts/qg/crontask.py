import json
import logging
import os,sys
import threading
import time
import schedule

sys.path.append(os.getcwd())
from db import DBMysqlHelper as mysqlHelper
from scripts.qg.xxqg import XxqgScript, XxqgUser
from device.virtual_device_manager import VirtualDeviceManager

logger = logging.getLogger(__name__)
# 使用一个简单的锁来防止任务重叠
login_device_lock = threading.Lock()

class EventRes:
    """
    事件结果
    """
    def __init__(self):
        self.code = 0
        self.msg = ""
        self.data = {}

    def __str__(self):
        return "code:%s,msg:%s,data:%s" % (self.code, self.msg, self.data)
    def to_dict(self):
        return {
            "code": self.code,
            "msg": self.msg,
            "data": self.data
        }

def login_device():
    """
    账号登录设备
    :return:
    """
   
    
    # 查询 event_business 表 event_code=login 的记录 且 status=-2
    eventBusiness = mysqlHelper.getLoginDevice()
    print("登录设备事件数量:",len(eventBusiness))
    for eventBusiness in eventBusiness:
        try:
            if not login_device_lock.acquire(False):
                logger.warning("登录设备任务正在执行中,请稍后再试")
                continue
            eventReq = json.loads(eventBusiness.eventReq)
            phone = eventReq["phoneNumber"]
            password = eventReq["password"]
            # 找到合适的设备
            freeDeviceId = mysqlHelper.getFreeDevice(phone)
            # 如果没有空闲设备，则返回，EventRes{code: 1001, msg: "没有空闲设备,请稍后再试", data: {}}
            if freeDeviceId is None:
                eventRes = EventRes()
                eventRes.code = 1001
                eventRes.msg = "没有空闲设备,请稍后再试"
                eventRes.data = {} 
                # eventRes转json
                eventResJosn = json.dumps(eventRes.to_dict())
                eventBusiness.eventRes = eventResJosn
                eventBusiness.updateByEventUid()
                continue
            # 执行登录操作
            vd = VirtualDeviceManager.get_device(freeDeviceId)
            users = list[XxqgUser]()
            # 解析eventBusiness.eventReq
            user = XxqgUser(phone=phone,password=password,vd=vd)
            users.append(user)
            xxqg = XxqgScript(vd,users)
            xxqg.start_app()
            # 异步执行登录
            for user in users:
                user.login()

            # 登录成功
            eventRes = EventRes()
            eventRes.code = 200
            eventRes.msg = "登录成功"
            eventRes.data = {}
            # 执行成功
            eventBusiness.status = 1
        except Exception as e:
            logger.error("登录设备失败:%s",e)
            # 登录失败
            eventRes = EventRes()
            eventRes.code = 1002
            eventRes.msg = "登录失败"
            eventRes.data = {}
            # status = 2 执行失败
            eventBusiness.status = 2
        finally:
            login_device_lock.release()

        eventResJosn = json.dumps(eventRes.to_dict())
        eventBusiness.eventRes = eventResJosn
        eventBusiness.updateByEventUid()

def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)

#  每五秒执行一次
def run_jobs(stop_event):
    # 设置任务每5秒运行一次
    schedule.every(5).seconds.do(login_device)

    while not stop_event.is_set():
        schedule.run_pending()
        time.sleep(1)

def stop_jobs():
    schedule.clear()

if __name__ == "__main__":
    login_device()






