import os
import sys
sys.path.append(os.getcwd()) 
import time
import uiautomator2 as u2
import logging
from scripts.qg.answer.AnswerTask import answer
from db.DBMysqlHelper import getVerifyCodeByPhone,clearVerifyCodeByPhone
from device.virtual_device import VirtualDevice
from util.rec.capche import Capche
from util import SimulateHelper
from PIL import Image
from constant import *


class Res:
    """
    返回结果
    """
    code:int  # 状态码
    msg:str  # 消息
    data:dict  # 数据

    def __init__(self,code:int,msg:str,data:dict):
        self.code = code
        self.msg = msg
        self.data = data

    def success(msg:str,data:dict):
        """
        成功
        :param msg:
        :param data:
        :return:
        """
        return Res(200,msg,data)
    
    def fail(msg:str,data:dict):
        """
        失败
        :param msg:
        :param data:
        :return:
        """
        return Res(500,msg,data)

class XxqgUtil:
    """
    学习强国工具
    """
    def back_home(self,d:u2.Device):
        """
        返回首页
        :return:
        """
        while d.app_current()["activity"] != XXQG_HOME_ACTIVITY:
            d.press("back")
            time.sleep(0.5)
        pass

    
    def getTextVeiws(self,d:u2.Device):
        """
        获取TextView
        :return:
        """
        textViews = d(className="android.widget.TextView")
        if (len(textViews) == 0):
            return d(className="android.view.View")
        return textViews
    
    
    def cropAndSave(self,bounds=None,path=None,image:Image=None):
        """
        裁剪图片
        :param bounds:
        :param path:
        :param image:Image
        """
        image.crop((bounds["left"],bounds["top"],bounds["right"],bounds["bottom"])).save(path)

class XxqgUser:
    """
    学习强国用户
    """
    phone:str  # 手机号
    password:str  # 密码
    today_score:int  # 今日积分
    vd : VirtualDevice  # 虚拟设备
    d :u2.Device  # u2设备实例
    xxqgUtil :XxqgUtil  # 学习强国工具

    def __init__(self,phone,password,vd:VirtualDevice):
        self.phone = phone
        self.password = password
        self.vd = vd
        self.d = vd.device
        self.xxqgUtil = XxqgUtil()





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
            editInputs = self.d(className="android.widget.EditText")
            # 删除选中的文字
            # self.d.click(966, 676)
            editInputs[0].set_text(self.phone)
            # time.sleep(3)
            # phone_input.set_text(self.login_user.phone)
            # time.sleep(1)
            while self.d(text="请输入密码").exists(timeout=5):
                passwdBtn = self.d.xpath(
                '//*[@resource-id="cn.xuexi.android:id/et_pwd_login"]')
                passwdBtn.set_text(self.password)
                time.sleep(1)
            
            if self.d(text="登录").wait(timeout=5):
                self.d(text="登录").click()

            # 密码错误
   
            
            # 校验是否登录成功
            wait_login_time = 0
            while self.d.app_current()["activity"] != XXQG_HOME_ACTIVITY or  wait_login_time > 5:
                logger.warning("登录中,当前页面:{}".format(ACTIVITY_MAP.get(self.d.app_current()["activity"])))
                time.sleep(2)
                if self.d(text='短时间内登录次数过多，请在10分钟后重试').exists(timeout=5):
                    logger.error("短时间内登录次数过多，请在10分钟后重试")
                    return Res.fail("短时间内登录次数过多，请在10分钟后重试",{})
                if self.d(text="号码或密码错误，请重新输入").exists(timeout=5):
                    logger.error("号码或密码错误，请重新输入,user:{}".format(self.phone))
                    return Res.fail("号码或密码错误，请重新输入",{})
                if self.d(text="登录").exists(timeout=5):
                    self.d(text="登录").click()
                    time.sleep(1)
                # 如果为首页，则登录成功
                if self.d.app_current()["activity"] == XXQG_HOME_ACTIVITY:
                    break
                
            if self.d.app_current()["activity"] != XXQG_HOME_ACTIVITY:
                logger.error("%s:登录失败",self.phone)
                return Res.fail("登录失败",{})

            logger.info("登录成功,耗时:"+str(time.time()-start))

        return Res.success("登录成功",{})

    def logout(self):
        """
        退出登录
        :return:
        """
        isHome = self.d.app_current()["activity"] == XXQG_HOME_ACTIVITY
        if isHome:
            if self.d(text="新版本抢先体验").exists(timeout=3):
                print("新版本抢先体验")
                self.d(text="取消").click()
            logger.info("已登录其他账号,即将退出登录")
            mine = self.d.xpath('//*[@resource-id="'+XXQG_MINE_RESOURCE_ID+'"]')
            mine.click()
            time.sleep(1)
            self.d.click(0.929, 0.044)
            time.sleep(1)
            self.d.xpath('//*[@text="退出登录"]').click()
            time.sleep(1)
            if self.d(text="您确定要退出登录吗？").exists(timeout=3):
                self.d(text="确认").click()
                time.sleep(1)
        
            logger.info("退出登录成功")
            time.sleep(1)

    def study(self):
        """
        学习
        :return:
        """
        # 获取当天的积分
        # socre,go_on = self.enter_score()
        # if not go_on:
        #     return
        time.sleep(1)
        while self.d.app_current()["activity"] != XXQG_HOME_ACTIVITY:
            self.xxqgUtil.back_home(self.d)
       
        d = self.d
        d.xpath('//*[@resource-id="'+XXQG_MINE_RESOURCE_ID+'"]').click()
        time.sleep(1)
        answer(self,self.vd,self.d)
        self.vd.stop()
    
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

class XxqgScript:
    """
    学习强国api
    """
    vd : VirtualDevice  # 虚拟设备
    d :u2.Device  # u2设备实例
    current_activity :str  # 当前activity
    login_users :list[XxqgUser]  # 登录用户
    capcheUtil :Capche  # 验证码工具
    xxqgUtil :XxqgUtil  # 学习强国工具

    def __init__(self,vd:VirtualDevice,login_users:list[XxqgUser]):
        self.vd = vd
        self.d = vd.device
        self.login_users = login_users
        self.watchExceptionStart()
        self.capcheUtil = Capche()
        self.current_activity = None
        self.xxqgUtil = XxqgUtil()
        pass


    def start_app(self):
        """
        启动app
        :return:
        """
        self.d.app_stop(XXQG_APP_PACKAGE)
        # self.d.app_clear(XXQG_APP_PACKAGE)
        time.sleep(4)
        self.d.app_start(XXQG_APP_PACKAGE)
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
            current_app = self.d.app_current()
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
    
   

    def isExceptionPage(self):
        """
        是否是异常页
        :return:
        """

        d = self.d
        d(text="访问异常").exists(timeout=5)
        textViews = d(className="android.widget.TextView")
        return d(text="请按照说明拖动滑块").exists(timeout=0.5) or d(description="请按照说明拖动滑块").exists(timeout=0.5) or d.app_current()["activity"] 
    

    
    def watchExceptionStart(self):  
        """
        监控异常
        :return:
        """
        self.d.watcher.when("访问异常").call(lambda :self.slideVerification())
        # self.d.watcher.when("确定").click()
        self.d.watcher.when("退出").click()
        self.d.watcher.when("同意").click()
        self.d.watcher.when("好的").click()
        # self.d.watcher.when("仅在使用中允许").click()
        # self.d.watcher.when("下次默认选择此项，不再提示").click()
        self.d.watcher.when("取消").click()
        self.d.watcher.when("始终允许").click()
    
        # enable auto trigger watchers
        self.d.watcher.start()

    def watchExceptionStop(self):
        """
        停止监控异常
        :return:
        """
        self.d.watcher.remove()
        self.d.watcher.stop()



    def handle_login_exception(self):
        """
        Handle login exception
        """
        raise Exception("短时间内登录次数过多")

    def slideVerification(self):
        """
        滑块验证
        :return:
        """
        d = self.d

        # 判断是否有 img/tip、img/capche 文件夹，没有则创建
        import os
        if not os.path.exists("img/tip"):
            os.makedirs("img/tip")
        if not os.path.exists("img/capche"):
            os.makedirs("img/capche")
        x0,y0 = 0,0
        try:
            i = 1
            currentActivity = self.d.app_current()["activity"]
            while (EXCEPTION_ACTIVITY == currentActivity and i <= 3):
                            
                textViews = self.xxqgUtil.getTextVeiws(self.d)
                print("滑块验证,第" + str(i) + "次")
                slideBtn = None
                slideRangeView = None
                for index in range(len(textViews)):
                    textView = textViews[index]
                    if textView.info["text"] == "\ue64e":
                        slideBtn = textView
                    if textView.info["text"] == "请按照说明拖动滑块":
                        slideRangeView = textView

                if slideBtn is not None and slideRangeView is not None:
                    slideBtnHalfWidth = (slideBtn.info["bounds"]["right"] - slideBtn.info["bounds"]["left"])/2
                    x0 = slideBtn.info["bounds"]["left"] + slideBtnHalfWidth
                    y0 = slideBtn.info["bounds"]["top"] + (slideBtn.info["bounds"]["bottom"] - slideBtn.info["bounds"]["top"])/2

                    slideWidth = slideRangeView.info["bounds"]["right"] - slideRangeView.info["bounds"]["left"]

                    print("拖动中心点:"+str(x0)+","+str(y0))
                    print("总滑动宽度:"+str(slideWidth))
                    date = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime())
                    right_end = x0+slideWidth-slideBtnHalfWidth
                    # d.swipe(x0, y0, right_end, y0, 0.2)
                    d.touch.down(x0, y0)
                    d.touch.move(right_end, y0)
                    time.sleep(1)
                    # 截图
                    d.screenshot().save("img/"+date+".png")
                    raw_image = Image.open("img/"+date+".png")
                    tip_img = d(className="android.widget.Image")[2]
                    capche_img =  d(className="android.widget.Image")[3]

                    # 获取项目根目录
                    rootPath = os.path.dirname(os.path.abspath(__file__)).split("scripts")[0]
                    capche_img_name = os.path.join(rootPath,"img/capche",date+"_capche.png")
                    tip_img_name = os.path.join(rootPath,"img/tip",date+"_tip.png")
                    self.xxqgUtil.cropAndSave(capche_img.info["bounds"],capche_img_name,raw_image)
                    self.xxqgUtil.cropAndSave(tip_img.info["bounds"],tip_img_name,raw_image)

                    # 识别tip的坐标
                    x_end = self.capcheUtil.get_right_pos(capche_img_name,tip_img_name)
                    # 误差
                    offset = 13
                    if x_end is not None:
                        move_x = x_end+slideBtnHalfWidth+offset
                        d.touch.move(move_x, y0)
                        d.touch.up(move_x, y0)
                time.sleep(1)
                i = i + 1
                currentActivity = self.d.app_current()["activity"]

        except Exception as e:
            print(e)
            pass
        finally:
            d.touch.up(x0, y0)

        if currentActivity != EXCEPTION_ACTIVITY:
            print("滑块验证成功")


    def slideVerificationForLogin(self):
        """
        登录滑块验证
        :return:
        """
        d = self.d

        while d(text="你在新的设备登录学习强国，为了保障你的账户安全，需要使用短信验证码确认").exists(timeout=3):
            d(text="确定").click()
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
            d(text="退出").click()
            time.sleep(3)
        while d(description="网络不佳，提交失败，请重试").exists(timeout=3):
            print("网络不佳，提交失败，请重试")
            if d(description="重试").exists(timeout=3):
                d(description="重试").click()
        while d(text="新版本抢先体验").exists(timeout=3):
            print("新版本抢先体验")
            d(text="取消").click()

    def enter_verify_code(self):
        """
        进入验证码页
        :return:
        """
        d = self.d
        wait_login_time = 0
        while wait_login_time < 10:
            if d.app_current()['activity'] == XXQG_VERIFY_CODE_ACTIVITY:
                break
            time.sleep(1)
            
        
        # 接收验证码
        verify_code = self.recevie_verify_code()
        # 输入验证码
        logger.info("第一次验证码:"+verify_code)
        verify_code_enter_time = 0
        while self.do_input_verify_code(verify_code,d) is False and verify_code_enter_time < 3:
            verify_code = self.recevie_verify_code()
            logger.info("输入验证码错误，重新获取验证码:"+verify_code)
            verify_code_enter_time += 1

        # 清空验证码
        self.reset_verify_code()
        logger.info("验证码输入成功,清空验证码")

    def recevie_verify_code(self):
        """
        接收验证码
        :return:
        """
        verify_code = ""
        attempt_times = 0
        while attempt_times <= 60:
            verify_code = self.get_verify_code()
            if len(verify_code) == 4:
                break
            attempt_times += 1
            time.sleep(1)
            continue
        return verify_code

    def reset_verify_code(self):
        """
        重置验证码
        :return:
        """
        clearVerifyCodeByPhone(self.login_user.phone)

    
    def get_verify_code(self):
        """
        获取验证码
        :return:
        """
        return getVerifyCodeByPhone(self.login_user.phone)

 

    def do_input_verify_code(self,captcha,d):
        """
        输入验证码
        :param captcha:
        :return:
        """
        d.xpath('//*[@resource-id="cn.xuexi.android:id/piv_verify_code_1"]').click()
        captchaArr = list(captcha)
        print(captchaArr)
        for index in range(len(captchaArr)):
            print(index, captchaArr[index])
            i = index + 1
            d.xpath(
                '//*[@resource-id="cn.xuexi.android:id/piv_verify_code_'+str(i)+'"]').click()
            d.set_fastinput_ime(True)  # 切换成FastInputIME输入法
            d.send_keys(captchaArr[index])  # adb广播输入
            d.set_fastinput_ime(False)  # 切换成正常的输入法
            time.sleep(1)

        if d(text="验证码错误，请重新输入").exists(timeout=5):
            d(text="确定").click()
            # 清空验证码
            self.reset_verify_code()
            return False

        return True

           
    
    def scan_qr_code(self):
        """
        扫码
        :return:
        """
        if self.d.app_current()["activity"] != XXQG_HOME_ACTIVITY:
            print("未在首页，退出")
            return
        d = self.d
        if d(text="强国通").wait(timeout=5) is False:
            print("未进入强国通，退出")
            return
        d(text="强国通").click()
        if d.xpath('//*[@resource-id="cn.xuexi.android:id/home_action_bar_button_icon"]').wait(timeout=5) is False:
            print("未找到+，退出")
            return
        # 点击+
        bar_btns = d.xpath('//*[@resource-id="cn.xuexi.android:id/home_action_bar_button_icon"]').all()
        print(len(bar_btns))
        bar_btns[1].click()

        # 点击扫一扫
        if d(text="扫一扫").wait(timeout=5) is False:
            print("未找到扫一扫，退出")
            return
        d(text="扫一扫").click()

        # 选择图册
        if d(text="相册").wait(timeout=5) is False:
            print("未找到图册，退出")
            return
        d(text="相册").click()

        # 选择从相册选择
        if d(text="相册").wait(timeout=5) is False:
            print("未找到相册，退出")
            return
        d(text="相册").click()

        # 选择第一张照片
        if d(className="android.widget.ImageView").wait(timeout=5) is False:
            print("未找到照片，退出")
            return
        imgs = d(className="android.widget.ImageView")
        print("找到照片,数量："+str(len(imgs)))
        imgs[0].click()

        
    

        d = self.d

    def run(self):
        users = self.login_users
        for user in users:
            print("用户："+user.phone+"开始学习")
            self.start_app()
            res = user.login()
            if res.code != 200:
                print("用户："+user.phone+"登录失败")
                continue
            user.study()
            print("用户："+user.phone+"学习结束")




logger = logging.getLogger(__name__)
