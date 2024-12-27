from LyzWindows.lw.py.MyWindow import MyWindow
import pygetwindow as gw


# 获取所有窗口对象
def get_my_windows():
    windows = gw.getAllWindows()
    result = []
    for window in windows:
        result.append(MyWindow(window))
    return result


# 排除标题为空的
def exclude_title_empty(my_windows: list[MyWindow]):
    return filter(lambda x: x.title != "", my_windows)


# 排除项
exclude_item = [
    'Program Manager',
    'Microsoft Text Input Application',
    'com.ayangweb.EcoPaste-siw',
    'InputTip.exe',
    'PixPin',
    'Windows Shell Experience 主机'
]


# 排除特定的标题
def exclude_title(my_windows: list[MyWindow]):
    result = []
    for i in my_windows:
        if i.title not in exclude_item:
            result.append(i)
    return result
    # return filter(lambda x: x.title not in exclude_item, my_windows)


# 可用的
def get_my_windows_use():
    my_windows = get_my_windows()
    my_windows = exclude_title_empty(my_windows)
    my_windows = exclude_title(my_windows)
    return my_windows


###########################################################################


# 获取特定的窗口
def get_mw_by_title(my_windows: list[MyWindow], title: str):
    result = []
    for mw in my_windows:
        if str(mw.title).find(title) != -1:
            result.append(mw)
    return result


# 获取特定的窗口(完全相等)
def get_mw_by_title_full(my_windows: list[MyWindow], title: str):
    result = []
    for mw in my_windows:
        if mw.title == title:
            result.append(mw)
    return result


# 获取特定的窗口 根据线程号
def get_mw_by_pid(my_windows: list[MyWindow], pid: int):
    result = []
    pid = int(pid)
    for mw in my_windows:
        if mw.pid == pid:
            result.append(mw)
    return result


# 获取特定的窗口 根据句柄
def get_mw_by_hwnd(my_windows: list[MyWindow], hwnd: int):
    result = []
    hwnd = int(hwnd)
    for mw in my_windows:
        if mw.hwnd == hwnd:
            result.append(mw)
    return result


# 获取特定的窗口 根据启动程序
def get_mw_by_exec(my_windows: list[MyWindow], exec: str):
    result = []
    for mw in my_windows:
        if mw.exec.find(exec) != -1:
            result.append(mw)
    return result

#
