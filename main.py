import os
import sys
from device.virtual_device_manager import VirtualDeviceManager


def print_folder_tree(path, parent_is_last=1, depth_limit=-1, tab_width=1):
    """
    以树状打印输出文件夹下的文件, 并返回文件夹内的所有文件
    :param tab_width: 空格宽度
    :param path: 文件夹路径
    :param depth_limit: 要输出文件夹的层数, -1为输出全部文件及文件夹
    :param parent_is_last: 递归调用上级文件夹是否是最后一个文件(夹), 控制输出 │ 树干
    :return: 返回path下的所有文件的数组
    """
    files = []
    if len(str(parent_is_last)) - 1 == depth_limit:
        return files
    items = os.listdir(path)
    for index, i in enumerate(items):
        is_last = index == len(items) - 1
        i_path = path + "/" + i
        for k in str(parent_is_last)[1:]:
            if k == "0":
                print("│" + "\t" * tab_width, end="")
            if k == "1":
                print("\t" * tab_width, end="")
        if is_last:
            print("└── ", end="")
        else:
            print("├── ", end="")
        if os.path.isdir(i_path):
            print(i)
            files.extend(print_folder_tree(
                path=i_path, depth_limit=depth_limit, parent_is_last=(parent_is_last * 10 + 1) if is_last else (parent_is_last * 10)))
        else:
            print(i_path.split("/")[-1])
            files.append(i_path)
    return files

if __name__ == "__main__":
    print(sys.path)
    print(sys.stdout.encoding)
    VirtualDeviceManager()
    