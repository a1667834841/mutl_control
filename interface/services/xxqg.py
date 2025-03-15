from scripts.qg.xxqg import Xxqg,User
from device.virtual_device_manager import VirtualDeviceManager
from device.virtual_device import VirtualDevice



def login_before(phone:str, password:str):
    """
    登录前置
    :param phone: 手机号
    :param password: 密码
    :return:
    """
    vd = VirtualDeviceManager.get_one_available_device()
    if vd == None:
        return None
    user = User(phone=phone, password=password)
    xxqg = Xxqg(VirtualDevice=vd,User=user)
    xxqg.login()

    pass