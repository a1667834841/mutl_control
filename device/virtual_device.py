from enum import Enum
import logging
"""
设备 核心api
"""

class DeviceStatus(Enum):
    """
    设备状态
    """
    OFF = 0  # 已停止
    STARTING = 1  # 启动中
    RUNNING = 2  # 已启动
    STOPPING = 3  # 停止中

class VirtualDevice:
    """
    设备
    """
    serialNumber = None  # 设备序列号
    status = None  # 设备状态 0:已停止 1:启动中 2:已启动 3:停止中 
    device = None  # 设备实例

    def __init__(self, serialNumber,device,status=DeviceStatus.OFF):
        self.serialNumber = serialNumber
        self.status = status
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
