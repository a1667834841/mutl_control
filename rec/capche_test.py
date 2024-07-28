import os,sys
# sys.path.append(os.getcwd()) 调用文件和被调用文件 在不同目录下时适用
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
import unittest
from rec.capche import Capche


capche = Capche()
class TestCapche(unittest.TestCase):

    @unittest.skip("跳过")
    def test_get_box_class(self):
        """
        测试识别图片 返回物体box坐标和类别
        """
        image = curPath+"/test_capche.png"
        results = capche.get_box_class(image)
        # 输出每个目标信息 换行输出
        for result in results:
            print(result["className"], result["box"],result["conf"])
        self.assertTrue(len(results) > 0)
    
    @unittest.skip("跳过")
    def test_get_words(self):
        """
        测试识别图片，返回文字
        """
        path = curPath+"/test_tip.png"
        result = capche.get_words(path)
        print(result)
        self.assertEqual(result,"2个篮子",msg="识别文字错误")
    
    @unittest.skip("跳过")
    def test_get_tip_by_words1(self):
        """
        测试通过识别的文字，返回提示
        """
        path = curPath+"/test_tip.png"
        num,result = capche.get_tip_by_words(path)
        self.assertEqual(result,"篮子",msg="返回提示错误")
        self.assertEqual(num,'2',msg="返回数量错误")

    @unittest.skip("跳过")
    def test_get_tip_by_words2(self):
        """
        测试通过识别的文字，返回提示
        """
        path = curPath+"/test_tip2.png"
        num,result = capche.get_tip_by_words(path)
        self.assertEqual(result,"椅子",msg="返回提示错误")
        self.assertEqual(num,'1',msg="返回数量错误")

    # @unittest.skip("跳过")
    def test_get_right_pos(self):
        """
        测试获取提示物体的左上角坐标
        """
        capche_dir_path = rootPath+"/img/capche"
        tip_dir_path = rootPath+"/img/tip"
        # 读取capche_path下的所有文件
        capche_files = os.listdir(capche_dir_path)
        for capche_file in capche_files:
            try:
                # capeche文件绝对路径
                capche_path = os.path.join(capche_dir_path,capche_file)
                # tip文件绝对路径
                tip_path = capche_path.replace("capche","tip")
                

                result = capche.get_right_pos(capche_path,tip_path)
                # print(result)
                self.assertTrue(result > 0,msg="获取坐标错误")

                # 使用cv 在capche_path 图片上的x坐标上画一条竖线，x= result
                # 读取图片
                import cv2
                img = cv2.imread(capche_path)
                # 画一条和图片高度一样的竖线
                start_point = (int(result),0)
                end_point = (int(result),img.shape[0])
                cv2.line(img, start_point, end_point, (0, 0, 255), 2)
                # 下载图片到 img/line文件夹下
                cv2.imwrite(rootPath+"/img/line/"+capche_file,img)
            except Exception as e:
                print("文件："+capche_file+"，识别错误")


if __name__ == '__main__':
    unittest.main()