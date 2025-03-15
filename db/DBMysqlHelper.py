import logging
import random
import threading
import config.config as config


# CREATE TABLE `event_business` (
#   `id` bigint(20) NOT NULL AUTO_INCREMENT,
#   `event_code` varchar(256) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '事件编码',
#   `event_uid` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '事件唯一值',
#   `event_req` varchar(256) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '事件入参',
#   `event_res` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '事件出参',
#   `status` bigint(20) DEFAULT NULL COMMENT '执行状态 -2=未执行 -1=执行中 1=执行成功 2=执行失败',
#   `create_time` bigint(20) DEFAULT NULL,
#   `update_time` bigint(20) DEFAULT NULL,
#   PRIMARY KEY (`id`) USING BTREE
# ) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin ROW_FORMAT=DYNAMIC;
class EventBusiness:
    """
    事件业务表
    """
    def __init__(self, eventCode, eventUid, eventReq, eventRes, status, createTime, updateTime):
        self.eventCode = eventCode
        self.eventUid = eventUid
        self.eventReq = eventReq
        self.eventRes = eventRes
        self.status = status
        self.createTime = createTime
        self.updateTime = updateTime

    def __str__(self):
        return "eventCode:%s,eventUid:%s,eventReq:%s,eventRes:%s,status:%s,createTime:%s,updateTime:%s" % (self.eventCode, self.eventUid, self.eventReq, self.eventRes, self.status, self.createTime, self.updateTime)
    
    def updateByEventUid(self):
        updateSql = "UPDATE event_business SET event_res='%s',status='%s' WHERE event_uid='%s'" % (
            self.eventRes, self.status, self.eventUid)
        config.MYSQL_CURSOR.execute(updateSql)
        config.MYSQL_DB.commit()



def initDevices(devices):

    updateSql = "UPDATE device SET status=0,free=1"
    config.MYSQL_CURSOR.execute(updateSql)
    if len(devices) > 0:
        for device in devices:
            # 查询是否有该设备
            selectSql = "SELECT id FROM device WHERE device_id='%s'" % (device)
            config.MYSQL_CURSOR.execute(selectSql)
            old = config.MYSQL_CURSOR.fetchone()
            if old is None:
                # 插入设备
                insertSql = "INSERT INTO device (device_id,status,free) VALUES ('%s',1,-1)" % (
                    device)
                config.MYSQL_CURSOR.execute(insertSql)
            else:
                # 更新设备状态
                updateSql = "UPDATE device SET status=1,free=-1 WHERE device_id='%s'" % (
                    device)
                config.MYSQL_CURSOR.execute(updateSql)
    config.MYSQL_DB.commit()

# 绑定手机号和设备关系


def bindPhoneAndDevice(phone, deviceId):
    # 查询是否有该手机号和设备绑定关系
    selectSql = "SELECT device_id FROM user_device WHERE phone='%s'" % (phone)
    config.MYSQL_CURSOR.execute(selectSql)
    userDevice = config.MYSQL_CURSOR.fetchone()
    if userDevice is None:
        # 插入手机号和设备绑定关系
        insertSql = "INSERT INTO user_device (phone,device_id) VALUES ('%s','%s')" % (
            phone, deviceId)
        config.MYSQL_CURSOR.execute(insertSql)
    config.MYSQL_DB.commit()

# 根据电话号码查询对应的验证码


def getVerifyCodeByPhone(phone):
    selectSql = "SELECT app_captcha FROM user WHERE phone_number='%s'  LIMIT 1" % (
        phone)
    config.MYSQL_CURSOR.execute(selectSql)
    code = config.MYSQL_CURSOR.fetchone()
    print(code)
    config.MYSQL_DB.commit()
    if code is not None:
        return code[0]
    return None

# 清空验证码


def clearVerifyCodeByPhone(phone):
    updateSql = "UPDATE user SET app_captcha='' WHERE phone_number='%s'" % (
        phone)
    config.MYSQL_CURSOR.execute(updateSql)
    config.MYSQL_DB.commit()

# 查询空闲的设备


def getFreeDevice(phone):
    selectSql = "SELECT device.device_id FROM device left join user_device on device.device_id = user_device.device_id WHERE status= 'free' and online=1 and user_device.phone = %s" % (
        phone)
    config.MYSQL_CURSOR.execute(selectSql)
    device = config.MYSQL_CURSOR.fetchone()
    # 如果之前有匹配过的设备 则返回之前的设备
    if device is not None:
        return device[0]
    
    # 随机获取一个可用设备
    selectSql = "SELECT device.device_id FROM device WHERE status= 'free' and online=1 limit 1"
    config.MYSQL_CURSOR.execute(selectSql)
    device = config.MYSQL_CURSOR.fetchone()
    if device is not None:
        return device[0]


def checkFreeDevice(deviceId):
    selectSql = "SELECT device.device_id FROM device WHERE free= -1 and status=1 and device.device_id='%s' GROUP BY device.device_id ORDER BY count(device.device_id) limit 1" % (
        deviceId)
    config.MYSQL_CURSOR.execute(selectSql)
    devices = config.MYSQL_CURSOR.fetchmany()
    # 获取一个设备
    if len(devices) > 0:
        return devices[0][0]
    return None

# 插入用户


def insertUser(userName, password, expireTime, pushId, nick, uid):
    selectSql = "SELECT uid FROM user WHERE phone_number='%s'" % (userName)
    config.MYSQL_CURSOR.execute(selectSql)
    user = config.MYSQL_CURSOR.fetchone()
    if user is None:
        # 插入手机号和设备绑定关系
        insertSql = "INSERT INTO user (phone_number,password,expiry_time,push_id,status,nick,uid) VALUES ('%s','%s','%s','%s','%s','%s','%s')" % (
            userName, password, expireTime, pushId, -1, nick, uid)
        config.MYSQL_CURSOR.execute(insertSql)
        config.MYSQL_DB.commit()
        return True
    return False

# 根据手机号查询设备


def getDeviceByPhone(phone):
    selectSql = "SELECT device_id FROM user_device WHERE phone='%s'" % (phone)
    config.MYSQL_CURSOR.execute(selectSql)
    devices = config.MYSQL_CURSOR.fetchone()
    # 随机获取一个设备
    if len(devices) > 0:
        return devices[0]
    return None

# 查询有账号密码的用户


def getAccount():
    selectSql = "SELECT phone_number as phoneNumber,password FROM user WHERE phone_number is not null and password is not null"
    config.MYSQL_CURSOR.execute(selectSql)
    accounts = config.MYSQL_CURSOR.fetchall()
    # 随机获取一个设备
    if len(accounts) > 0:
        return accounts
    return None


# 获取设备下的账户信息
def getSerialAccountMap():
    selectSql = "SELECT user.phone_number as phoneNumber,user.password,user_device.device_id FROM user left join user_device on user.phone_number = user_device.phone where user.phone_number is not null and user.password is not null and user_device.device_id is not null"
    config.MYSQL_CURSOR.execute(selectSql)
    accounts = config.MYSQL_CURSOR.fetchall()
    if len(accounts) > 0:
        # 返回map
        serialAccountMap = {}
        for account in accounts:
            # 字典为空 则初始化
            print(account)
            if serialAccountMap.get(account[2]) is None:
                serialAccountMap[account[2]] = []
            serialAccountMap[account[2]].append(account)
        return serialAccountMap
    return None

# 设置设备可用状态


def setDeviceOnline(deviceId, online):
    lock = threading.Lock()
    lock.acquire()
    updateSql = "UPDATE device SET online=%s WHERE device_id='%s'" % (
        online, deviceId)
    config.MYSQL_CURSOR.execute(updateSql)
    lock.release()
    config.MYSQL_DB.commit()

# 设置所有的设备为离线状态
def setAllDeviceOffline():
    updateSql = "UPDATE device SET online=0"
    config.MYSQL_CURSOR.execute(updateSql)
    config.MYSQL_DB.commit()



# 设置设备在线/离线状态


def setDeviceOnline(deviceId, status):
    updateSql = "UPDATE device SET status=%s WHERE device_id='%s'" % (
        status, deviceId)
    config.MYSQL_CURSOR.execute(updateSql)
    config.MYSQL_DB.commit()

# 初始化设备状态


def initDeviceToAvaliable(deviceId):
    slectSql = "SELECT id FROM device WHERE device_id='%s'" % (deviceId)
    config.MYSQL_CURSOR.execute(slectSql)
    device = config.MYSQL_CURSOR.fetchone()
    if device is None:
        # 插入设备
        insertSql = "INSERT INTO device (device_id,online,status) VALUES ('%s',1,'free')" % (
            deviceId)
        result = config.MYSQL_CURSOR.execute(insertSql)
        logger.info("插入设备结果:%s", result)
    else:
        # 更新设备状态
        updateSql = "UPDATE device SET status='free',online=1 WHERE device_id='%s'" % (
            deviceId)
        config.MYSQL_CURSOR.execute(updateSql)
    config.MYSQL_DB.commit()

# 设置验证码


def updateUserCaptcha(uid, captcha):
    updateSql = "UPDATE user SET app_captcha='%s' WHERE uid='%s'" % (
        captcha, uid)
    config.MYSQL_CURSOR.execute(updateSql)
    config.MYSQL_DB.commit()


def getUserByUid(uid):
    selectSql = "SELECT phone_number as phoneNumber,password,expiry_time as expiryTime,push_id as pushId,nick,uid FROM user WHERE uid='%s'" % (
        uid)
    config.MYSQL_CURSOR.execute(selectSql)
    user = config.MYSQL_CURSOR.fetchone()
    if user is not None:
        return user
    return None

# 查询 event_business 表 event_code=LOGIN_EVENT 的记录 且 status=-2
def getLoginDevice() -> list[EventBusiness]:
    eventBusiness = []
    selectSql = "SELECT * FROM event_business WHERE event_code='LOGIN_EVENT' and status=-2"
    config.MYSQL_CURSOR.execute(selectSql)
    config.MYSQL_DB.commit()
    loginDevices = config.MYSQL_CURSOR.fetchall()
    for loginDevice in loginDevices:
        eventBusiness.append(EventBusiness(loginDevice[1], loginDevice[2], loginDevice[3], loginDevice[4], loginDevice[5], loginDevice[6], loginDevice[7]))
    
    return eventBusiness


logger = logging.getLogger(__name__)