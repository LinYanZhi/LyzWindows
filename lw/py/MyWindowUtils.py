import os
import json
import pygetwindow as gw

from LyzWindows.lw.py.MyWindow import MyWindow


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
def get_exclude_item(file_path):
    # 如果文件不存在
    if not os.path.exists(file_path):
        return []
    with open(file_path, 'r', encoding='utf-8') as f:
        exclude_items = json.load(f)
    for item in exclude_items:
        item["size"] = item.get("size", None)
        if item["size"] is not None:
            item["size"] = tuple(item["size"])
        item["position"] = item.get("position", None)
        if item["position"] is not None:
            item["position"] = tuple(item["position"])
    return exclude_items


# 查看是否在exclude_item中
def is_in_exclude_item(exclude_items, my_window: MyWindow):
    """{
        "title": "QQ",
        "exec_path: "",
        "size": null,
        "position": null
    }
    检查窗口是否应该被排除。
    :param exclude_items: 排除项列表，每个项是一个字典，包含窗口的属性。
    :param my_window: 要检查的窗口对象。
    :return: 如果窗口应该被排除，返回True，否则返回False。
    """
    for item in exclude_items:
        match_count = 0
        for key, value in item.items():
            if value is None:
                continue  # 如果排除项中的属性值为None，跳过检查
            if hasattr(my_window, key) and getattr(my_window, key) == value:
                match_count += 1

        # 如果所有非None属性都匹配，则窗口应该被排除
        if match_count == len([item for item in item.values() if item is not None]):
            return True
    return False


# 排除特定的标题
def exclude_by_items(my_windows: list[MyWindow], exclude_path, ):
    result = []
    exclude_item = get_exclude_item(exclude_path)
    for i in my_windows:
        if not is_in_exclude_item(exclude_item, i):
            result.append(i)
    return result


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

if __name__ == '__main__':
    my_windows = get_my_windows()
    for mw in my_windows:
        print(mw.title, "|", mw.exec_path, "|", f"{mw.size[0]}x{mw.size[1]}", "|", mw.position, "|", mw.pid, "|",
              mw.hwnd)
    # kimi_window = get_mw_by_exec(my_windows, "Kimi")[0]
    # print(kimi_window)
    # kimi_window.set_dock_opt(5)
