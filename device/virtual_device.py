from enum import Enum
import logging
"""
设备 核心api
"""

class DeviceStatus:
    """
    设备状态
    """
    OFF = "off"  # 已停止
    STARTING = "starting"  # 启动中
    FREE = "free"  # 空闲
    RUNNING = "running"  # 运行中
    STOPPING = "stopping"  # 停止中

class VirtualDevice():
    """
    设备
    """
    serialNumber : str  # 设备序列号
    online : int  # 是否在线  -1:离线 1:在线
    status : str   # 设备状态 0:已停止 1:启动中 2:已启动 3:停止中 
    device : object  # 设备实例

    def __init__(self, serialNumber:str,device:object,status:str):
        self.serialNumber = serialNumber
        self.status = DeviceStatus.FREE
        self.device = device

    def start(self):
        """
        启动设备
        :return:
        """
        logger.info("启动设备: %s", self.serialNumber)
        self.status = DeviceStatus.RUNNING

        return self

    def stop(self):
        """
        停止设备
        :return:
        """
        logger.info("停止设备: %s", self.serialNumber)
        self.status = DeviceStatus.OFF

        pass

    def isRunning(self):
        """
        是否正在运行
        :return:
        """
        return self.status == DeviceStatus.RUNNING
    
    def isStopped(self):
        """
        是否已停止
        :return:
        """
        return self.status == DeviceStatus.OFF

    def __str__(self):
        return "Device(serialNumber=%s)" % self.serialNumber

    def __repr__(self):
        return self.__str__()


logger = logging.getLogger(__name__)
