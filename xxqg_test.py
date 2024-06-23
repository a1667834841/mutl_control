import logging
from device.virtual_device_manager import VirtualDeviceManager as Vdm
from xxqg import User, Xxqg,XXQG_APP_PACKAGE
from answer import AnswerUpdator


vdm = Vdm()
vd = vdm.get_device("emulator-5554")
login_user = User("13217913287","a13014483325")
xxqg = Xxqg(vd,login_user)

def test_app_start():
    """
    测试app启动
    """
    xxqg.start_app()
    assert xxqg.vd.device.app_current().get("package") == XXQG_APP_PACKAGE

def test_app_login():
    """
    测试app登录
    """
    xxqg.start_app()
    xxqg.login()

def test_app_enter_score():
    """
    测试app进入积分
    """
    score,go_on = xxqg.enter_score()
    assert score > 0

def test_app_study():
    """
    测试app登出
    """
    xxqg.study()

def test_tiku_update():
    """
    测试题库更新
    """
    AnswerUpdator.update()

test_app_study()