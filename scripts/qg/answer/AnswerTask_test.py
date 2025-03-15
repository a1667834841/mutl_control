import os,sys
import os,sys
pwd = os.getcwd()
sys.path.append(pwd)
sys.path.append(pwd+"\\scripts\\qg")
from device.virtual_device_manager import VirtualDeviceManager
from scripts.qg.xxqg import User , Xxqg , XXQG_APP_PACKAGE
from answer.AnswerTask import *
from answer.AnswerUpdator import *
from AnswerTask import __four_fight_question__, task_type_current,__two_fight_question__
# 调用文件和被调用文件 在不同目录下时适用
# curPath = os.path.abspath(os.path.dirname(__file__))
# rootPath = os.path.split(curPath)[0]
# sys.path.append(rootPath)
import unittest


vdm = VirtualDeviceManager()
vd = vdm.get_one_available_device()
login_user = User("13217913287","a13014483325")
xxqg = Xxqg(vd,login_user)

class AnswerTaskTest(unittest.TestCase):

    def test_task_type(self):
        """
        测试任务类型
        """
        task_type = task_type_current(xxqg.d)
        print(task_type)
        self.assertEqual(task_type,"challenge-score",msg="任务类型错误")

    @unittest.skip("跳过")
    def test_two_fight(self):
        """
        测试两人对战
        """
        __two_fight_question__(xxqg.d)

    def test_four_fight(self):
        """
        测试四人对战
        """
        __four_fight_question__(xxqg.d)
        pass


if __name__ == '__main__':
    unittest.main()