import os
import re
import cv2
import numpy as np
from ultralytics import YOLO
import ddddocr



# 使用 ultralytics 识别图片 返回物体box坐标和类别
# 返回的是一个列表，列表中的每个元素是一个字典，字典中包含了box坐标和类别
# 例如 [{'box': [0.0, 0.0, 0.0, 0.0], 'class': '0'}]
# 0.0 0.0 0.0 0.0 分别代表左上角x坐标，左上角y坐标，右下角x坐标，右下角y坐标
# class 代表类别

class Capche:

    # yolo模型
    model: YOLO = None
    # ocr模型
    ocr: ddddocr.DdddOcr = None
    # tip中英文映射表 花盆,篮子,气球 ,树 ,足球 ,帐篷,枕头,鞋,向日葵 ,花,向且羹,房子,蛋糕 ,革果,杯子,免子,椅子 ,蝴蝶 ,草莓,皇冠 ,瓶子,挂锁,车,闹钟,冰淇淋,宇航员,玫瑰花,苹果,量冠,草,苹栗,字航员,宝航员,林子,冰湛淋,冰滇淋,蛋精,轨头
    # 花盆 pot,篮子 basket,气球 balloon,树 tree,足球 soccer ball,帐篷 tent,枕头 pillow,鞋 shoe,向日葵 sunflower,房子 house,杯子 cup,兔子 rabbit,蝴蝶 butterfly,草莓 strawberry,皇冠 crown,瓶子 bottle,菠萝 pineapple,挂锁 padlock,车 car,闹钟 alarm clock,冰淇淋 ice cream,宇航员 astronaut,玫瑰花 rose,苹果 apple,椅子 chair,蛋糕 cake
    tip_map = {
        "花盆":"pot",
        "篮子":"basket",
        "气球":"balloon",
        "树":"tree",
        "足球":"soccer-ball",
        "帐篷":"tent",
        "枕头":"pillow",
        "鞋":"shoe",
        "向日葵":"sunflower",
        "花":"flower",
        "向且羹":"sunflower",
        "房子":"house",
        "蛋糕":"cake",
        "革果":"apple",
        "杯子":"cup",
        "免子":"rabbit",
        "椅子":"chair",
        "蝴蝶":"butterfly",
        "草莓":"strawberry",
        "皇冠":"crown",
        "瓶子":"bottle",
        "挂锁":"padlock",
        "车":"car",
        "闹钟":"alarm-clock",
        "冰淇淋":"ice-cream",
        "宇航员":"astronaut",
        "玫瑰花":"rose",
        "苹果":"apple",
        "量冠":"crown",
        "草":"grass",
        "苹栗":"apple",
        "字航员":"astronaut",
        "宝航员":"astronaut",
        "林子":"cup",
        "冰湛淋":"ice-cream",
        "冰滇淋":"ice-cream",
        "蛋精":"cake",
        "向白萎":"sunflower",
        "向日羹":"sunflower",
        "蓝子":"basket",
    }

    def __init__(self):
        current_path = os.path.abspath(os.path.dirname(__file__))
        self.model = YOLO(current_path+"/best.pt")
        self.ocr = ddddocr.DdddOcr()

    def get_box_class(self,image):
        """
        识别图片 返回物体box坐标和类别
        """
        model = self.model
        rec_result_list = []
        results = model(image)
        for result in results:
            # 输出类别对应的box坐标
            # print(result.boxes.cls)
            classes = result.boxes.cls.tolist()
            class_names = result.names
            xyxys = result.boxes.xyxy.tolist()
            conf_list = result.boxes.conf.tolist()

            for i in range(len(classes)):
                # 输出box坐标
                rec_result = {}
                rec_result["class"] = classes[i]
                rec_result["className"] = class_names[int(classes[i])]
                rec_result["box"] = xyxys[i]
                rec_result["conf"] = conf_list[i]
                rec_result_list.append(rec_result)

            # 输出类别
            # print(result.names)
        # print(rec_result_list)
        return rec_result_list

    # get_box_class("rec/test_capche.png")


    def get_words(self,path):
        """
        识别图片，返回文字
        """
        file = None
        try:
            file = open(path, 'rb')
            image = file.read()
            result = self.ocr.classification(image)
        except Exception as e:
            print(f"识别图片失败，错误信息：{e}")
            result = None
        finally:
            file.close()
        return result


    def get_tip_by_words(self,path):
        """
        通过识别的文字，返回提示
        """
        result = self.get_words(path)
        if result is None:
            return None
        
        num,tip = result.split("个")
        # 判断num是否为数字
        if not num.isdigit():
            return '1',tip
        return num,tip
    

    def get_right_pos(self,capche_path,tip_path) -> int:
        """
        获取提示物体的左上角坐标
        """
        # 识别tip 返回物体和数量
        num,word = self.get_tip_by_words(tip_path)
        # 获取识别图片的box结果
        rec_results = self.get_box_class(capche_path)

        # 根据word获取tip对应的英文
        tip_class = self.tip_map.get(word)
        if tip_class is None:
            print("tip:"+word+",对应的英文不存在")
            raise Exception("tip:"+word+",对应的英文不存在")
        
        # 将rec_results过滤出 className=tip_class 的集合，按照box[0]从小到大排序
        tip_results = list(filter(lambda x: x["className"]==tip_class,rec_results ))
        tip_results.sort(key=lambda x: x["box"][2])
        
        if len(tip_results) >= int(num):
            return tip_results[int(num)-1]["box"][2]
        return None
  