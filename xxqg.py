import time
import uiautomator2 as u2
import logging
from answer.AnswerTask import answer
from device.virtual_device import VirtualDevice
from util import SimulateHelper


# xxqg app 包名
XXQG_APP_PACKAGE = "cn.xuexi.android"

# ====== activity ======
# xxqg 登录页
XXQG_LOGIN_ACTIVITY = "com.alibaba.android.user.login.SignUpWithPwdActivity"
# xxqg 首页
XXQG_HOME_ACTIVITY = "com.alibaba.android.rimet.biz.home.activity.HomeActivity"
# xxqg 验证码页
XXQG_VERIFY_ACTIVITY = "com.alibaba.android.user.login.VerifyPhoneActivity"
# 异常activity
EXCEPTION_ACTIVITY = "com.alibaba.wireless.security.open.middletier.fc.ui.ContainerActivity"



# ===== resourceId =====
# 弹窗标题
XXQG_ALERT_TITLE_RESOURCE_ID = "cn.xuexi.android:id/alertTitle"
# 我的
XXQG_MINE_RESOURCE_ID = "cn.xuexi.android:id/comm_head_xuexi_mine"

class User:
    """
    用户
    """
    phone = None  # 手机号
    password = None  # 密码
    today_score = 0  # 今日积分

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
        self.current_activity = activity
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
        # 退出登录
        self.logout()

        loginBtn = self.d(text="新用户注册")
        if loginBtn.exists(timeout=10):
            # 统计登录耗时时间
            start = time.time()
            logger.info("未登录")
            time.sleep(1)
            phone_input = self.d.xpath(
                '//*[@resource-id="cn.xuexi.android:id/et_phone_input"]')
            # 删除选中的文字
            self.d.click(966, 676)
            time.sleep(1)
            self.d.xpath(
                '//*[@resource-id="cn.xuexi.android:id/et_phone_input"]').set_text(self.login_user.phone)
            time.sleep(1)
            self.d.xpath(
                '//*[@resource-id="cn.xuexi.android:id/et_pwd_login"]').set_text(self.login_user.password)

            self.d.xpath('//*[@resource-id="cn.xuexi.android:id/btn_next"]').click()
            # 监控滑块验证
            self.watchException()

            # 密码错误
            if self.d(text="号码或密码错误，请重新输入").exists(timeout=5):
                logger.error("号码或密码错误，请重新输入,user:{}".format(self.login_user.phone))
                raise Exception("号码或密码错误，请重新输入,user:{}".format(self.login_user.phone))


        return self

    def logout(self):
        """
        退出登录
        :return:
        """
        isHome = self.current_activity == XXQG_HOME_ACTIVITY
        if isHome:
            logger.info("已登录其他账号,即将退出登录")
            mine = self.d.xpath('//*[@resource-id="cn.xuexi.android:id/comm_head_xuexi_mine"]')
            mine.click()
            time.sleep(3)
            self.d.click(0.929, 0.044)
            time.sleep(3)
            self.d.xpath('//*[@text="退出登录"]').click()
            time.sleep(3)
            self.d.xpath('//*[@resource-id="android:id/button1"]').click()
            logger.info("退出登录成功")
            time.sleep(1)

    
    def watchException(self):  
        """
        监控异常
        :return:
        """
        self.d.watcher.when("登录").call(self.slideVerificationForLogin())
        self.d.watcher.start()

    def slideVerificationForLogin(self):
        """
        登录滑块验证
        :return:
        """
        d = self.d
        # 第一次进来滑块验证
        i = 1
        # print(d.app_current()["activity"])
        while d(text="请按照说明拖动滑块").exists(timeout=3) or d(description="请按照说明拖动滑块").exists(timeout=3) or d.app_current()["activity"] == EXCEPTION_ACTIVITY:
            print("滑块验证,第" + str(i) + "次")
            d.swipe_points([(0.163, 0.544), (0.491, 0.547)], 0.2)
            time.sleep(3)
            i = i + 1
        # 多次滑动重试
        while d(text="当前功能使用人数过多，请稍后重试").exists(timeout=3):
            d.xpath('//*[@resource-id="android:id/button1"]').click()
            print("重试登录")
            d.xpath('//*[@resource-id="cn.xuexi.android:id/btn_next"]').click()
            i = 1
            while d(text="请按照说明拖动滑块").exists(timeout=5) or d(description="请按照说明拖动滑块").exists(timeout=5):
                print("滑块验证,第" + str(i) + "次")
                d.swipe_points([(0.163, 0.544), (0.491, 0.547)], 0.2)
                time.sleep(3)
                i = i + 1
        while d(text="网络开小差，请稍后再试").exists(timeout=3):
            print("网络开小差，请稍后再试")
            d(text="确定").click()
            time.sleep(3)
        while d(description="网络不佳，提交失败，请重试").exists(timeout=3):
            print("网络不佳，提交失败，请重试")
            if d(description="重试").exists(timeout=3):
                d(description="重试").click()

    def study(self):
        """
        学习
        :return:
        """
        # 获取当天的积分
        # socre,go_on = self.enter_score()
        # if not go_on:
        #     return
       
        d = self.d
        d.xpath('//*[@resource-id="'+XXQG_MINE_RESOURCE_ID+'"]').click()
        time.sleep(3)
        answer(self.login_user,self.vd,self.d)
    
    def enter_score(self):
        """
        进入积分页
        :return:
        """
        d = self.d
         # 点击我的
        d.xpath('//*[@resource-id="'+XXQG_MINE_RESOURCE_ID+'"]').click()
        time.sleep(2)
        # 点击学习积分
        d.click(214, 810)
        time.sleep(2)
        # 获取积分
        score = SimulateHelper.getScore(d)
        # score 转int
        go_on = True
        if score > 37:
            logger.info("积分"+str(score)+"大于37,不需要答题")
            go_on = False
        d.press("back")
        d.press("back")
        return score,go_on
logger = logging.getLogger(__name__)
