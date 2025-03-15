import os
import sys
from adbutils import adb
import uiautomator2 as u2
import logging

from device.virtual_device import VirtualDevice,DeviceStatus
from db import DBMysqlHelper as mysqlHelper

# 把当前文件所在文件夹的父文件夹路径加入到PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class VirtualDeviceManager:
    """
    设备管理
    """
    devices = []  # 设备列表

    def __init__(self):
        # 初始化设备列表
        self.refresh()
        pass

    def add_device(device:VirtualDevice):
        """
        添加设备
        :param device:
        :return:
        """
        VirtualDeviceManager.devices.append(device)
    
    def all_devices() -> list[VirtualDevice]:
        """
        所有设备
        :return:
        """
        return VirtualDeviceManager.devices

    def get_device(serialNumber) -> VirtualDevice:
        """
        获取设备
        :param serialNumber:
        :return:
        """
        try:
            d =  u2.connect(serialNumber)
        except Exception as e:
            logging.error("连接设备:%s失败", serialNumber)
            raise e
        return VirtualDevice(serialNumber,d,DeviceStatus.FREE)
    
    def get_one_available_device(self):
        """
        获取一个可用设备
        :return:
        """
        for device in VirtualDeviceManager.devices:
            if device != None and device.status == DeviceStatus.FREE:
                return device
        return None
    

    def start_all(self):
        """
        启动所有设备
        :return:
        """
        for device in VirtualDeviceManager.devices:
            device.start()

        return self

    def stop_all(self):
        """
        停止所有设备
        :return:
        """
        for device in VirtualDeviceManager.devices:
            device.stop()

        return self

    def __str__(self):
        return "DeviceManager(devices=%s)" % self.devices

    def __repr__(self):
        return self.__str__()
    
    def refresh(self):
        """
        刷新设备列表
        :return:
        """
        # os.system("adb remount")
        # os.system("adb devices")
        print("在线设备数量:",len(adb.device_list()))
        mysqlHelper.setAllDeviceOffline()
        for device in adb.device_list():
            d = u2.connect(device.serial)
            if d is None:
                logging.error("设备连接失败: %s", device.serial)
                vd = VirtualDevice(device.serial,d)
                VirtualDeviceManager.add_device(vd)
                continue
            vd = VirtualDevice(serialNumber=device.serial,device=d,status=DeviceStatus.FREE)
            VirtualDeviceManager.add_device(vd)
            mysqlHelper.initDeviceToAvaliable(device.serial)
        logging.info("%s台设备连接成功", len(adb.device_list()))
        if len(adb.device_list()) == 0:
            logging.error("没有设备连接成功")
            raise Exception("没有设备连接成功")
        print("%s台设备连接成功" % len(adb.device_list()))
    
logger = logging.getLogger(__name__)