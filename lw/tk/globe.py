import tkinter as tk

from LyzWindows.lw.py.MyWindowUtils import *


# 全局数据交互
class Data:
    # main_top
    main_top_tabel_column_name = ['窗口名称', '启动程序', '窗口大小', '窗口位置', 'PID', 'hwnd', '路径', '焦点',
                                  '最大化', '最小化']
    main_top_table_data = []
    main_top_select_row = tuple()
    is_on_top = True  # 是否置于顶层
    # main_middle
    main_middle_columns_name = ['名称', '大小', '位置', 'PID', 'hwnd', '程序', '路径', '焦点', '最大', '最小', ]
    main_middle_columns_dict = {_: '' for _ in main_middle_columns_name}
    # main_bottom

    pass


# 全局事件交互
class Method:
    # main
    refresh = None
    # main_top
    refresh_table_data = None  # 需要参数（新的table）
    # main_top -> main_middle
    update_main_middle_by_table = None  # 需要参数（新的select item）


    pass


# 全局对象交互
class Object:
    # main_bottom
    main_bottom_window_width: tk.Entry = None
    main_bottom_window_height: tk.Entry = None
    main_bottom_window_x: tk.Entry = None
    main_bottom_window_y: tk.Entry = None
    main_bottom_button_wh: tk.Button = None
    main_bottom_button_xy: tk.Button = None
    pass


g_data = Data()
g_method = Method()
g_object = Object()