##  app层级调试命令
pip install uiautodev
uiauto.dev


pip install weditor
python -m weditor
## adb命令

### 查看当前设备所处的activity
adb shell dumpsys activity top | grep ACTIVITY

### 查看当前的app的包名
#### windows
```shell
adb shell dumpsys window | findstr mCurrentFocus
```
#### linux/mac
```shell
adb shell dumpsys window | grep mCurrentFocus
```


## 测试命令
pytest scripts/qg/xxqg_test.py::test_app_start
pytest scripts/qg/xxqg_test.py::test_app_login
pytest scripts/qg/xxqg_test.py::test_app_study
pytest scripts/qg/xxqg_test.py::test_xxqg_all

## 查看依赖版本
使用pipdeptree

首先安装pipdeptree库: pip install pipdeptree

然后使用命令pipdeptree -p 库名


https://github.com/openatx/uiautomator2/blob/master/QUICK_REFERENCE.md


## u2 基本操作
https://www.cnblogs.com/dyd168/p/15756529.html


## 问题
### 包问题 ModuleNotFoundError: No module named

调用文件和被调用文件 在不同目录下时适用
sys.path.append(os.getcwd()) 

调用文件和被调用文件 在同一目录下时适用
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)


### most likely due to a circular import
解决掉循环依赖

### 在push项目时遇到问题：Push failed Empty reply from server
执行
git config --global --unset http.proxy