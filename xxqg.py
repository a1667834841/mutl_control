import time
import uiautomator2 as u2
import logging
from device.virtual_device import VirtualDevice


# xxqg app 包名
XXQG_APP_PACKAGE = "cn.xuexi.android"

# ====== activity ======
# xxqg 登录页
XXQG_LOGIN_ACTIVITY = "com.alibaba.android.user.login.SignUpWithPwdActivity"
# xxqg 首页
XXQG_HOME_ACTIVITY = "com.alibaba.android.rimet.biz.home.activity.HomeActivity"
# xxqg 验证码页
XXQG_VERIFY_ACTIVITY = "com.alibaba.android.user.login.VerifyPhoneActivity"


# ===== resourceId =====
# 弹窗标题
XXQG_ALERT_TITLE = "cn.xuexi.android:id/alertTitle"

class User:
    """
    用户
    """
    phone = None  # 手机号
    password = None  # 密码

    def __init__(self,phone,password):
        self.phone = phone
        self.password = password

class Xxqg:
    """
    学习强国api
    """
    vd = None  # 虚拟设备
    d = None  # u2设备实例
    current_activity = None  # 当前activity
    login_user = None  # 登录用户

    def __init__(self,vd:VirtualDevice,login_user:User):
        self.vd = vd
        self.d = vd.device
        self.login_user = login_user
        pass

    def start_app(self):
        """
        启动app
        :return:
        """
        self.vd.device.app_stop(XXQG_APP_PACKAGE)
        time.sleep(1)
        self.vd.device.app_start(XXQG_APP_PACKAGE)
        isEnter,activity = self.isEnter()
        logger.info("App entered,activity: {}".format(activity))
        if not isEnter:
            logger.error("App not entered,activity: {}".format(activity))
            raise Exception("App not entered,activity: {}".format(activity))
        
        return self
    
    def isEnter(self):
        """
        是否进入app
        :return:
        """
        # 等待出现首页或登录页，说明app已启动
        wait_time = 10
        start_time = time.time()
        isEnter = False
        while(True):
            current_app = self.vd.device.app_current()
            current_activity = current_app['activity']

            if current_activity == XXQG_LOGIN_ACTIVITY or current_activity == XXQG_HOME_ACTIVITY:
                isEnter = True
                break
            end_time = time.time()
            if end_time - start_time > wait_time:
                break

            if self.d(text="欢迎使用学习强国").exists(timeout=5):
                self.d(text="同意").click()
                time.sleep(1)
        return isEnter,current_activity
    
    def login(self):
        """
        登录
        :return:
        """
        #TODO 判断当前设备已登录用户和要登录的用户是否一致
        self.logout()

        loginBtn = self.d(text="新用户注册")
        if loginBtn.exists(timeout=10):
            # 统计登录耗时时间
            start = time.time()
            logger.info("未登录")
            time.sleep(1)
            phone = self.d.xpath(
                '//*[@resource-id="cn.xuexi.android:id/et_phone_input"]')
            # 点击输入框使其获得焦点
            phone.long_click()
            # 全选输入框中的文字
            self.d.send_keys([u2.KeyboardEvent.KEYCODE_CTRL_LEFT, u2.KeyboardEvent.KEYCODE_A])
            # 删除选中的文字
            self.d.send_keys([u2.KeyboardEvent.KEYCODE_DEL])
            time.sleep(1)
            self.d.xpath(
                '//*[@resource-id="cn.xuexi.android:id/et_phone_input"]').set_text(self.login_user.phone)
            time.sleep(1)
            self.d.xpath(
                '//*[@resource-id="cn.xuexi.android:id/et_pwd_login"]').set_text(self.login_user.password)

            self.d.xpath('//*[@resource-id="cn.xuexi.android:id/btn_next"]').click()
            # 滑块验证
            # slideVerificationForLogin(self.d)
            # 密码错误
            if self.d(text="号码或密码错误，请重新输入").exists(timeout=5):
                logger.error("号码或密码错误，请重新输入,user:{}".format(self.login_user.phone))
                raise Exception("号码或密码错误，请重新输入,user:{}".format(self.login_user.phone))


        pass

    def logout(self):
        """
        退出登录
        :return:
        """
        isHome = self.current_activity == XXQG_HOME_ACTIVITY
        if isHome:
            logger.info("已登录其他账号,退出登录")
            mine = self.d.xpath('//*[@resource-id="cn.xuexi.android:id/comm_head_xuexi_mine"]')
            mine.click()
            time.sleep(3)
            self.d.click(0.929, 0.044)
            time.sleep(3)
            self.d.xpath('//*[@text="退出登录"]').click()
            time.sleep(3)
            self.d.xpath('//*[@resource-id="android:id/button1"]').click()
            logger.info("退出登录成功")
            time.sleep(3)

logger = logging.getLogger(__name__)
