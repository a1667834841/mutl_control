import os,sys
sys.path.append(os.getcwd())
from device.virtual_device_manager import VirtualDeviceManager
from scripts.qg.xxqg import User , Xxqg , XXQG_APP_PACKAGE
from answer.AnswerTask import *
from answer.AnswerUpdator import *

vdm = VirtualDeviceManager()
vd = vdm.get_one_available_device()
# login_user = User("13217913287","a13014483325")
# login_user = User("17303800136","a13014483325")
# xxqg = Xxqg(vd,login_user)


# xxqg 首页
XXQG_HOME_ACTIVITY = "com.alibaba.android.rimet.biz.home.activity.HomeActivity"

def test_app_start(xxqg):
    """
    测试app启动
    """
    xxqg.start_app()
    assert xxqg.vd.device.app_current().get("package") == XXQG_APP_PACKAGE


def test_app_lout(xxqg):
    """
    测试app登录
    """
    xxqg.start_app()
    xxqg.logout()

def test_app_login(xxqg):
    """
    测试app登录
    """
    xxqg.start_app()
    xxqg.login()

    assert xxqg.vd.device.app_current()["activity"] == XXQG_HOME_ACTIVITY

def test_app_enter_score(xxqg):
    """
    测试app进入积分
    """
    score,go_on = xxqg.enter_score()
    assert score > 0

def test_app_study(xxqg):
    """
    测试app 登录
    """
    # xxqg.start_app()
    xxqg.study()

def test_tiku_update():
    """
    测试题库更新
    """
    update()

def test_xxqg_all(xxqg):
    """
    测试全流程
    """
    # 开始时间
    start_time = time.time()
    xxqg.start_app()
    xxqg.login()
    xxqg.enter_score()
    xxqg.study()
    # 结束时间
    end_time = time.time()
    print(f"{xxqg.phone}-总耗时：{end_time-start_time}秒")

def test_batch_xxqg():
    """
    测试多用户
    """
    users = [
        User("13217913287","a13014483325"),
        User("17303800136","a13014483325"),
    ]
    for user in users:
        xxqg = Xxqg(vd,user)
        test_xxqg_all(xxqg)

# test_tiku_update()
# test_xxqg_all()
test_batch_xxqg()
# if __name__ == "__main__":
#     test_app_start()