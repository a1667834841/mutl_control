
from json import JSONEncoder


class SimpleClassEncoder(JSONEncoder):

    def default(self, o):
        return o.__dict__
    

# list 转成Json格式数据
def listToJson(lst):
    import json
    import numpy as np
    keys = [str(x) for x in np.arange(len(lst))]
    list_json = dict(zip(keys, lst))
    str_json = json.dumps(list_json, indent=2, ensure_ascii=False)  # json转为string
    return str_json