from virtual_device_manager import VirtualDeviceManager as Vdm

vdm = Vdm()

def test_virtual_device_init():
    # 测试设备管理初始化,得到设备列表
    assert len(vdm.devices) > 0