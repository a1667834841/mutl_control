from virtual_device import VirtualDevice

device = VirtualDevice("123456",None)
def test_device_start():
    """
    测试设备启动
    """
   
    device.start()
    assert device.isRunning()

def test_device_stop():
    """
    测试设备停止
    """
    device.stop()
    assert device.isStopped()


