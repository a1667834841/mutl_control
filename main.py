import logging
import sys
import threading
import signal
import time
from urllib import request
from interface.app import app
from device.virtual_device_manager import VirtualDeviceManager 
from scripts.qg.crontask import run_jobs, stop_jobs
from util.rec.capche import Capche

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# 创建一个事件对象
stop_event = threading.Event()

def signal_handler(signum, frame):
    logger.info("接收到终止信号，正在停止所有线程...")
    stop_event.set()
    sys.exit(0)


def run_flask():
    app.run()

def init():
    # adb启动
    vdm = VirtualDeviceManager()
    # 图像识别模块启动
    capche = Capche()

def run():
    try:
        signal.signal(signal.SIGINT, signal_handler)
        init()
        # 在单独的线程中运行定时任务
        jobs_thread = threading.Thread(target=run_jobs, args=(stop_event,))
        jobs_thread.start()
        
        # 在主线程中运行Flask
        run_flask()
     
    except Exception as e:
        logger.error(f'发生错误: {str(e)}')
    finally:
        stop_jobs()  # 停止定时任务
        # 等待所有线程结束
        jobs_thread.join()
        logger.info('多控平台v1.0.0已停止')

if __name__ == '__main__':
    print('多控平台v1.0.0启动')
    logger.info('多控平台v1.0.0启动')
    run()




    