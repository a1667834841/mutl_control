import json
import os,sys
from flask import  jsonify,Blueprint, request

from interface.routes import SimpleClassEncoder
# pwd = os.getcwd()
# sys.path.append(pwd)
sys.path.append(os.getcwd()+"\\device")
from device.virtual_device_manager import VirtualDeviceManager
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

devices_bp = Blueprint('devices', __name__,url_prefix='/devices')


@devices_bp.route('/list', methods=['GET'])
def list_devices():
    """
    获取设备列表
    """
    deviceArray = []
    for device in VirtualDeviceManager.all_devices():
        # 构建json数据
        deviceArray.append(
            {
                "serialNumber":device.serialNumber,
                "status":device.status.value
            }
        )
    return jsonify("devices",deviceArray)


@devices_bp.route('/login/html', methods=['GET'])
def login():
    """
    返回登录页面
    """
    with open('static/login.html', 'r',encoding="UTF-8") as file:
        login_page = file.read()
    return login_page

@devices_bp.route('/login', methods=['POST'])
def login_post():
    """
    登录
    """
    data = request.get_json()
    print(data)
    return jsonify(data)

@devices_bp.route('/capche', methods=['POST'])
def capche():
    """
    触发获取验证码
    """
    data = request.get_json()
    print(data)
    return jsonify(data)

