from window import Windows, WindowTool
from typing import List


import win32gui

# 获取当前顶级窗口句柄
# hwnd = win32gui.GetForegroundWindow()
# print("hwnd: ", hwnd)

# window = Windows(hwnd)
# print(window)


# 获取所有窗口句柄
window_handle_list = WindowTool.get_all_window_handle()
all_windows: List[Windows] = []
for window_handle in window_handle_list:
    try:
        window = Windows(window_handle)
        all_windows.append(window)
    except:
        pass


print("所有窗口有: ", len(all_windows))

is_visible_window_list: List[Windows] = [
    window for window in all_windows if window.is_visible()
]
print("可见窗口有: ", len(is_visible_window_list))

is_size_normal_window_list: List[Windows] = [
    window for window in all_windows if window.is_size_normal()
]
print("正常大小窗口有: ", len(is_size_normal_window_list))

# 打印正常的窗口信息
# for window in is_size_normal_window_list:
#     print(window.print(True))



# 获取屏幕宽高像素
screen_size = WindowTool.get_screen_size()
print(screen_size.print(True))
