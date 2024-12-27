import tkinter as tk
from tkinter import ttk

import pyautogui

from LyzWindows.lw.tk.globe import g_data, g_object
from LyzWindows.lw.tk.css import css


# 窗口控制
def page_controller(frame):
    title_label = tk.Label(frame, text="窗口控制：", font=css['font10'])
    title_label.pack(padx=(5, 0), anchor='nw')

    # 第一行
    row1_frame = tk.Frame(frame, )
    row1_frame.pack(anchor='nw')
    # width
    tk.Label(row1_frame, text="w", font=css['font10'], width=1).pack(side='left', padx=(10, 0))
    g_object.main_bottom_window_width = tk.Entry(row1_frame, width=8, relief='flat')
    g_object.main_bottom_window_width.pack(side='left', padx=(5, 0))
    # height
    tk.Label(row1_frame, text="  h", font=css['font10'], width=2).pack(side='left')
    g_object.main_bottom_window_height = tk.Entry(row1_frame, width=8, relief='flat')
    g_object.main_bottom_window_height.pack(side='left', padx=(5, 0))
    # button
    g_object.main_bottom_button_wh = tk.Button(row1_frame, text="确定", relief='flat', font=css['font10'],
                                               command=set_window_size,
                                               )
    g_object.main_bottom_button_wh.pack(side='left', padx=(5, 0))

    # 第二行
    row2_frame = tk.Frame(frame, )
    row2_frame.pack(anchor='nw')
    # x
    tk.Label(row2_frame, text="x", font=css['font10'], width=1).pack(side='left', padx=(10, 0))
    g_object.main_bottom_window_x = tk.Entry(row2_frame, width=8, relief='flat')
    g_object.main_bottom_window_x.pack(side='left', padx=(5, 0))
    # y
    tk.Label(row2_frame, text="  y", font=css['font10'], width=2).pack(side='left')
    g_object.main_bottom_window_y = tk.Entry(row2_frame, width=8, relief='flat')
    g_object.main_bottom_window_y.pack(side='left', padx=(5, 0))
    # button
    # tk.Button(row2_frame, text="确定", relief='flat', font=css['font10'],
    #           command=set_window_position,
    #           ).pack(side='left', padx=(5, 0))
    g_object.main_bottom_button_xy = tk.Button(row2_frame, text="确定", relief='flat', font=css['font10'],
                                               command=set_window_position,
                                               )
    g_object.main_bottom_button_xy.pack(side='left', padx=(5, 0))

    # 第三行
    row3_frame = tk.Frame(frame, )
    row3_frame.pack(anchor='nw')
    tk.Button(row3_frame, text="restore()", relief='flat', font=css['font10'],
              command=lambda: set_window("restore")
              ).pack(side='left', padx=(5, 0))
    tk.Button(row3_frame, text="max()", relief='flat', font=css['font10'],
              command=lambda: set_window("max")
              ).pack(side='left', padx=(5, 0))
    tk.Button(row3_frame, text="min()", relief='flat', font=css['font10'],
              command=lambda: set_window("min")
              ).pack(side='left', padx=(5, 0))
    tk.Button(row3_frame, text="close()", relief='flat', font=css['font10'],
              command=lambda: set_window("close")
              ).pack(side='left', padx=(5, 0))

    # 第4行
    # row4_frame = tk.Frame(frame, )
    # row4_frame.pack(anchor='nw')
    # tk.Button(row4_frame, text="hide()", relief='flat', font=css['font10'],
    #           command=lambda: set_window("hide")
    #           ).pack(side='left', padx=(5, 0))
    # tk.Button(row4_frame, text="show()", relief='flat', font=css['font10'],
    #           command=lambda: set_window("show")
    #           ).pack(side='left', padx=(5, 0))

    return


# 事件：集合(restore, max, min, close, hide, show)
def set_window(action):
    # 根据 hwnd
    if 'hwnd' not in g_data.main_top_select_row and True:
        return
    hwnd = g_data.main_top_select_row['hwnd']
    exclude_path = g_data.get_exclude_items()
    my_windows = get_my_windows()
    my_windows = exclude_by_items(my_windows, exclude_path)
    window = get_mw_by_hwnd(my_windows, hwnd)
    if len(window) != 1:
        raise Exception(f'根据pid搜索，理应只找到一个，结果len={len(window)}，无法理解，程序退出。')
    window = window[0]
    # 开始
    if action == "restore":
        window.win_obj.restore()
    elif action == "max":
        window.win_obj.maximize()
    elif action == "min":
        window.win_obj.minimize()
    elif action == "close":
        window.win_obj.close()
    elif action == "hide":
        window.win_obj.hide()
    elif action == "show":
        window.win_obj.show()
    else:
        raise Exception("无法理解action={}".format(action))
    return


# 窗口停靠-事件
def set_window_dock(t):
    if g_object.main_bottom_window_width.get() == '' or g_object.main_bottom_window_height.get() == '':
        return
    screen_width, screen_height = pyautogui.size()
    window_width = int(g_object.main_bottom_window_width.get())
    window_height = int(g_object.main_bottom_window_height.get())

    if t == '7':  # 左上角
        new_x = 0
        new_y = 0
    elif t == '8':  # 中上角
        new_x = (screen_width - window_width) // 2
        new_y = 0
    elif t == '9':  # 右上角
        new_x = screen_width - window_width
        new_y = 0
    elif t == '4':  # 左中角
        new_x = 0
        new_y = (screen_height - window_height) // 2
    elif t == '5':  # 中间
        new_x = (screen_width - window_width) // 2
        new_y = (screen_height - window_height) // 2
    elif t == '6':  # 右中角
        new_x = screen_width - window_width
        new_y = (screen_height - window_height) // 2
    elif t == '1':  # 左下角
        new_x = 0
        new_y = screen_height - window_height
    elif t == '2':  # 中下角
        new_x = 0
        new_y = screen_height - window_height
    elif t == '3':  # 右下角
        new_x = screen_width - window_width
        new_y = screen_height - window_height
    else:
        raise Exception("输入应该是1~9才对，无法理解...")
    g_object.main_bottom_window_x.delete(0, tk.END)
    g_object.main_bottom_window_y.delete(0, tk.END)
    g_object.main_bottom_window_x.insert(0, new_x)
    g_object.main_bottom_window_y.insert(0, new_y)
    g_object.main_bottom_button_xy.config(bg='lightblue')
    return

    pass


# 窗口停靠
def page_dock(frame):
    title_label = tk.Label(frame, text="窗口停靠：", font=css['font10'])
    title_label.pack(padx=(0, 0), anchor='nw')
    # 九宫格按钮
    grid_frame = tk.Frame(frame)
    grid_frame.pack(side='top', anchor='ne')  # 放置在右上角
    grid_buttons = [
        '7', '8', '9',
        '4', '5', '6',
        '1', '2', '3'
    ]
    for i, text in enumerate(grid_buttons):
        row = i // 3
        col = i % 3
        tk.Button(grid_frame, text=text, width=3, height=0, relief='flat', font=css['font9'],
                  command=lambda t=text: set_window_dock(t)
                  ).grid(row=row, column=col)
    return


# 窗口大小预设`
def page_size(frame):
    title_label = tk.Label(frame, text="窗口大小预设：", font=css['font10'])
    title_label.pack(pady=(0, 0), anchor='nw')
    # 窗口大小按钮
    size_frame = tk.Frame(frame)
    size_frame.pack(fill='x')  # 放置在底部
    size_buttons = [
        'full(1938,1098)',
        'screen(1920,1080)',
        'jetbrains(1770,1000)',
        '智谱清言(1663,938)',
        '~(1550,980)',
        '夸克,钉钉(1410,809)',
        'music(1321,940)',
        'explorer(1313,750)',
        'cmd(1259,770)',
        '微信(1080,800)',
    ]
    # 初始化网格布局的行和列索引
    row_index = 0
    col_index = 0

    # 创建按钮并放置到网格中，自动换行
    for text in size_buttons:
        button = tk.Button(size_frame, text=text, relief='flat', font=css['font9'],
                           command=lambda t=text: set_window_size(t)
                           )
        button.grid(row=row_index, column=col_index, padx=(0, 5), pady=(0, 0), sticky='w')
        col_index += 1  # 移动到下一列
        if col_index >= 3:  # 如果达到3列，则换行
            col_index = 0
            row_index += 1  # 移动到下一行
    return


# main-bottom-right
def init_frame(frame):
    frame_page_controller = tk.Frame(frame,
                                     # bg='pink'
                                     )
    frame_page_dock = tk.Frame(frame,
                               # bg='blue'
                               )
    frame_page_size = tk.Frame(frame,
                               # bg='green'
                               )

    # init
    page_controller(frame_page_controller)
    page_dock(frame_page_dock)
    page_size(frame_page_size)

    # pack
    frame_page_controller.pack(side='left', fill='y', padx=(0, 20))
    frame_page_dock.pack(side='left', fill='y', padx=(0, 20))
    frame_page_size.pack(side='left', fill='both', expand=True, padx=(0, 0))

    return


from LyzWindows.lw.py.MyWindowUtils import *


# 设置窗口大小
def set_window_size(text=None):
    # 仅设置值
    if text and g_object.main_bottom_window_height.get() != '':
        # 截取 ( 和 ) 中间的字符串
        size = text.split('(')[1].split(')')[0]
        width, height = size.split(',')
        g_object.main_bottom_window_width.delete(0, tk.END)
        g_object.main_bottom_window_width.insert(0, width)
        g_object.main_bottom_window_height.delete(0, tk.END)
        g_object.main_bottom_window_height.insert(0, height)
        g_object.main_bottom_button_wh.config(bg='lightgreen')
        return

    if g_object.main_bottom_window_width.get() == '' or g_object.main_bottom_window_height.get() == '':
        return

    width = int(g_object.main_bottom_window_width.get())
    height = int(g_object.main_bottom_window_height.get())
    # 根据 hwnd
    if 'hwnd' not in g_data.main_top_select_row:
        return
    hwnd = g_data.main_top_select_row['hwnd']
    exclude_path = g_data.get_exclude_items()
    my_windows = get_my_windows()
    my_windows = exclude_by_items(my_windows, exclude_path)
    window = get_mw_by_hwnd(my_windows, hwnd)
    if len(window) != 1:
        raise Exception(f'根据pid搜索，理应只找到一个，结果len={len(window)}，无法理解，程序退出。')
    window = window[0]
    # 设置窗口宽高
    window.set_size((width, height))
    # 恢复颜色
    g_object.main_bottom_button_wh.config(bg='SystemButtonFace')
    return


# 设置窗口位置
def set_window_position():
    if g_object.main_bottom_window_x.get() == '' or g_object.main_bottom_window_y.get() == '':
        return
    x = int(g_object.main_bottom_window_x.get())
    y = int(g_object.main_bottom_window_y.get())
    # 根据 hwnd 和
    hwnd = g_data.main_top_select_row['hwnd']
    exclude_path = g_data.get_exclude_items()
    my_windows = get_my_windows()
    my_windows = exclude_by_items(my_windows, exclude_path)
    window = get_mw_by_hwnd(my_windows, hwnd)
    if len(window) != 1:
        raise Exception(f'根据pid搜索，理应只找到一个，结果len={len(window)}，无法理解，程序退出。')
    window = window[0]
    # 设置窗口位置
    window.set_position((x, y))
    # 恢复颜色
    g_object.main_bottom_button_xy.config(bg='SystemButtonFace')
    return
