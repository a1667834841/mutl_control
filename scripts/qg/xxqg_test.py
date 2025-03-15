import os,sys
import threading

sys.path.append(os.getcwd())
from device.virtual_device_manager import VirtualDeviceManager
from scripts.qg.xxqg import XxqgScript , XxqgUser , XXQG_APP_PACKAGE
from answer.AnswerTask import *
from answer.AnswerUpdator import *

# vdm = VirtualDeviceManager()
# vd = vdm.get_one_available_device()
# users = []
# login_user1 = XxqgUser(phone="13217913287",password="a13014483325",vd=vd)
# login_user2 = XxqgUser(phone="17303800136",password="a13014483325",vd=vd)
# users.append(login_user1)
# users.append(login_user2)

# xxqg = XxqgScript(vd,users)


# xxqg 首页
XXQG_HOME_ACTIVITY = "com.alibaba.android.rimet.biz.home.activity.HomeActivity"

def test_app_start(xxqg:XxqgScript):
    """
    测试app启动
    """
    xxqg.start_app()
    assert xxqg.vd.device.app_current().get("package") == XXQG_APP_PACKAGE


def test_app_lout(xxqg:XxqgScript):
    """
    测试app登录
    """
    # xxqg.start_app()
    login_user1.logout()

def test_app_login(xxqg:XxqgScript):
    """
    测试app登录
    """
    xxqg.start_app()
    login_user1.login()

    assert xxqg.vd.device.app_current()["activity"] == XXQG_HOME_ACTIVITY

def test_app_enter_score():
    """
    测试app进入积分
    """
    score,go_on = login_user1.enter_score()
    assert score > 0

def test_app_study(user:XxqgUser):
    """
    测试app 登录
    """
    # xxqg.start_app()
    user.study()

def test_tiku_update():
    """
    测试题库更新
    """
    update()

def test_xxqg_all(xxqg:XxqgScript):
    """
    测试全流程
    """
    # 开始时间
    start_time = time.time()
    xxqg.run()
    # 结束时间
    end_time = time.time()
    print(f"{xxqg.login_user.phone}-总耗时：{end_time-start_time}秒")

# def test_scan_qr_code(xxqg:Xxqg):
#     """
#     测试扫码
#     """
#     # 打开app
#     xxqg.start_app()
#     # 登录
#     xxqg.login()
#     # 读取图片二维码byte

#     xxqg.scan_qr_code()

def test_batch_xxqg():
    """
    测试多用户
    """
    users = [
        XxqgUser("13217913287","a13014483325"),
        XxqgUser("17303800136","a13014483325"),
    ]
    threads = []
    for user in users:
        # 多线程 一个用户一个设备
        vd = vdm.get_one_available_device()
        xxqg = XxqgScript(vd,users)
        thread = threading.Thread(target=test_xxqg_all,args=((xxqg,)))
        thread.start()
        threads.append(thread)
        time.sleep(1)
    for thread in threads:
        thread.join()

# 密码输错，输出错误信息，程序停止
def test_error_password():
    """
    测试密码错误
    """
    users = []
    vdm = VirtualDeviceManager()
    vd = vdm.get_one_available_device()
    user = XxqgUser(phone="13217913287",password="a1301448332",vd=vd)
    users.append(user)
    xxqg = XxqgScript(vd,users)
    xxqg.run()
    

test_error_password()
# test_tiku_update()
# test_xxqg_all(xxqg)
# test_app_login(xxqg)
# test_batch_xxqg()
# test_scan_qr_code(xxqg)
# if __name__ == "__main__":
#     test_app_start()