import os
from adbutils import adb
import uiautomator2 as u2
import logging

from device.virtual_device import VirtualDevice,DeviceStatus

class VirtualDeviceManager:
    """
    设备管理
    """
    devices = []  # 设备列表

    def __init__(self):
        # 初始化设备列表
        self.refresh()
        pass

    def add_device(self, device:VirtualDevice):
        """
        添加设备
        :param device:
        :return:
        """
        self.devices.append(device)

        return self

    def get_device(self, serialNumber):
        """
        获取设备
        :param serialNumber:
        :return:
        """
        for device in self.devices:
            if device.serialNumber == serialNumber:
                return device

        return None

    def start_all(self):
        """
        启动所有设备
        :return:
        """
        for device in self.devices:
            device.start()

        return self

    def stop_all(self):
        """
        停止所有设备
        :return:
        """
        for device in self.devices:
            device.stop()

        return self
    
    def all_devices(self):
        """
        所有设备
        :return:
        """
        return self.devices

    def __str__(self):
        return "DeviceManager(devices=%s)" % self.devices

    def __repr__(self):
        return self.__str__()
    
    def refresh(self):
        """
        刷新设备列表
        :return:
        """
        os.system("adb remount")
        os.system("adb devices")
        for device in adb.device_list():
            d = u2.connect(device.serial)
            if d is None:
                logging.error("设备连接失败: %s", device.serial)
                vd = VirtualDevice(device.serial,d)
                self.add_device(vd)
                continue
            vd = VirtualDevice(device.serial,d,DeviceStatus.RUNNING)
            self.add_device(vd)
        return self
    
logger = logging.getLogger(__name__)