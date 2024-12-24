import tkinter as tk

import pyautogui

from LyzWindows.lw.tk.css import css
from LyzWindows.lw.tk.globe import g_method, g_object

# 创建主窗口
root = tk.Tk()
root.title("LyzWindow 窗口控制")

# 大小
root.geometry(f"{css['width']}x{css['height']}")
# 位置
root.geometry(f"+{css['x']}+{css['y']}")

# 加入全局对象
g_object.root = root

# 上部分frame
frame_top = tk.Frame(root)
# 中部分frame
frame_middle = tk.Frame(root)
# 下部分frame
frame_bottom = tk.Frame(root)

# 初始化
from LyzWindows.lw.tk.main_top.app import init_frame as init_frame1, on_refresh_click
from LyzWindows.lw.tk.main_middle.app import init_frame as init_frame2
from LyzWindows.lw.tk.main_bottom.app import init_frame as init_frame3

init_frame1(frame_top, root)
init_frame2(frame_middle)
init_frame3(frame_bottom)

# 加入
frame_top.pack(fill='both', expand=True)
frame_middle.pack(fill='both', expand=True)
frame_bottom.pack(fill='both', expand=True)

# 绑定键盘事件
root.bind('<Control-r>', lambda x: on_refresh_click())
# 绑定鼠标右键事件
root.bind('<Button-3>', lambda x: on_refresh_click())

# 屏幕大小
print("屏幕wh:", *pyautogui.size())


# 获取root
def get_root():
    return root


# 启动主事件循环
root.mainloop()


r"""
(home) D:\PyCharm_code\home\LyzWindows\lw\package>
pyinstaller ..\tk\main.py -p D:\PyCharm_code\home\LyzWindows\lw
pyinstaller --onefile --windowed ..\tk\main.py -p D:\PyCharm_code\home\LyzWindows
"""

