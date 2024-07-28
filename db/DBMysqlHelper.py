import random
import threading
import config.config as config


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


def getFreeDevice():
    selectSql = "SELECT device.device_id FROM device left join user_device on device.device_id = user_device.device_id WHERE free= -1 and status=1 GROUP BY device.device_id ORDER BY count(device.device_id) limit 1"
    config.MYSQL_CURSOR.execute(selectSql)
    devices = config.MYSQL_CURSOR.fetchmany()
    # 随机获取一个设备
    if len(devices) > 0:
        return devices[0][0]
    return None


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


def setDeviceFree(deviceId, free):
    lock = threading.Lock()
    lock.acquire()
    updateSql = "UPDATE device SET free=%s WHERE device_id='%s'" % (
        free, deviceId)
    config.MYSQL_CURSOR.execute(updateSql)
    lock.release()
    config.MYSQL_DB.commit()


# 设置设备在线/离线状态


def setDeviceStatus(deviceId, status):
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
        insertSql = "INSERT INTO device (device_id,status,free) VALUES ('%s',1,-1)" % (
            deviceId)
        config.MYSQL_CURSOR.execute(insertSql)
    else:
        # 更新设备状态
        updateSql = "UPDATE device SET status=1,free=-1 WHERE device_id='%s'" % (
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
