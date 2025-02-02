import psutil
import win32con
import win32gui
import win32process
import pyautogui

from lw0_0_3._rust.R import R
from lw0_0_3.config.Exclude import g_exclude
from lw0_0_3.entity.WindowObj import WindowObj


class Windows:
    all_window_objs: list[WindowObj] = []

    # 获取所有进程
    @staticmethod
    def __enum_windows() -> list:
        # 调用函数
        def callback(hwnd, hwnd_s):
            # IsWindowVisible: 判断窗口是否可见
            # IsWindowEnabled: 判断窗口是否可用
            if win32gui.IsWindowVisible(hwnd) and win32gui.IsWindowEnabled(hwnd):
                hwnd_s.append(hwnd)
            return True

        hwnd_s = []
        win32gui.EnumWindows(callback, hwnd_s)
        return hwnd_s

    # 获取所有窗口对象
    @staticmethod
    def get_window_objs() -> list[WindowObj]:
        Windows.all_window_objs = []
        hwnd_s = Windows.__enum_windows()
        for hwnd in hwnd_s:
            window_obj = WindowObj(hwnd)
            Windows.all_window_objs.append(window_obj)
        return Windows.all_window_objs

    # 排除项
    @staticmethod
    def exclude() -> list[WindowObj]:
        Windows.get_window_objs()

        # 排除项
        def is_exclude(cls, exclude_dict):
            for k, v in exclude_dict.items():
                # 排除空
                if v is None:
                    continue
                # title process_path size xy
                flag = 0
                count = 0
                for key, value in v.items():
                    # 检查类是否有这个属性
                    if hasattr(cls, key):
                        count += 1
                        # 获取属性的值
                        attr_value = getattr(cls, key)
                        # 有相同
                        if attr_value == value:
                            flag += 1
                if flag == count:
                    return True
            # 所有条件都不满足，才返回False
            return False

        exclude_dict = g_exclude.data
        result = []
        for item in Windows.all_window_objs:
            if not is_exclude(item, exclude_dict):
                result.append(item)
        return result

    pass
