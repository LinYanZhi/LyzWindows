import pygetwindow as gw
import pyautogui as pg


# 获取当前活动窗口
def get_active_window():
    try:
        # 获取当前活动窗口
        active_window = gw.getActiveWindow()
        if active_window:
            return active_window
        else:
            print("无法获取当前活动窗口。")
            return None
    except Exception as e:
        print(f"发生错误: {e}")
        return None
    pass


# 根据窗口标题查找
def find_window_by_title(title):
    try:
        # 根据窗口标题查找窗口
        windows = gw.getWindowsWithTitle(title)

        # 如果 title 中不包含 cmd
        # 则去除 windows 中前缀为 'C:\Windows\system32\cmd.exe'
        if 'cmd' not in title:
            windows = [w for w in windows if not w.title.startswith('C:\\Windows\\system32\\cmd.exe')]

        # 无
        if len(windows) == 0:
            return None

        # 只有一个则直接返回
        if len(windows) == 1:
            return windows[0]

        # 多个则返回 完全相等 的，若无完全相等的，则也返回无
        elif len(windows) > 1:
            for w in windows:
                if w.title == title:
                    return w
            else:
                print(f"找到 {len(windows)} 个标题为“{title}”的窗口。无法确定要获取哪一个。")
                for w in windows:
                    print(f"窗口标题: {w.title}")
            return None

    except Exception as e:
        print(f"发生错误: {e}")

    return


# 输出长度
print_len = max(len(str(pg.size().width)), len(str(pg.size().height)))


# 根据窗口标题获取窗口具体信息
def get_window_info_by_title(title):
    window = find_window_by_title(title)
    if window:
        # 完整名称
        print(f"窗口标题: {window.title}")
        # 窗口大小
        print(f"窗口大小: {window.size[0]} x {window.size[1]}")
        # 窗口位置
        print(f"窗口位置: {window.left} , {window.top}")
        # 窗口是否有焦点
        print(f"窗口是否有焦点: {window.isActive}")
        # 窗口是否最小化
        print(f"窗口是否最小化: {window.isMinimized}")
        # 窗口是否最大化
        print(f"窗口是否最大化: {window.isMaximized}")
    return
