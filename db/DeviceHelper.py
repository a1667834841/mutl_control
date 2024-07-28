import os
import DBMysqlHelper as db
import config.config as config


# 初始化设备
def initDevice():
    # 声明一个list 存储设备名称
    devices = []
    for serial in config.DRIVER_MAP.keys():
        devices.append(serial)
    db.initDevices(devices)

# 找一个可用的设备


def findAvailableDevice(phone):
    # 先查询是否有绑定的设备
    availableDevice = db.getDeviceByPhone(phone)
    return availableDevice


def findAvailableDeviceByDeviceId(deviceId):
    if deviceId is not None:
        # 先判断设备是否可用
        availableDevice = db.checkFreeDevice(deviceId)
        # 如果设备可用
        if availableDevice:
            # 则返回设备
            return availableDevice
    # 如果设备不可用
    else:
        # 则查询可用的一个设备
        availableDevice = db.getFreeDevice()
    return availableDevice
