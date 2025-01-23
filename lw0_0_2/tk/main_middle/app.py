import tkinter as tk

from lw0_0_2.tk.globe import g_data, g_method
from lw0_0_2.tk.css import css


# main-bottom-left
def init_frame(frame):
    title_label = tk.Label(frame, text="窗口具体信息：", font=css['font10'])
    title_label.pack(padx=(5, 0), pady=(0, 5), anchor='nw')

    # 0.1 0.4 0.1 0.5

    # 创建两个子框架，一个用于显示column1，另一个用于显示column2
    frame_column1_title = tk.Frame(frame, width=frame.winfo_width() * 0.1)
    frame_column1_value = tk.Frame(frame, width=frame.winfo_width() * 0.4)
    frame_column2_title = tk.Frame(frame, width=frame.winfo_width() * 0.1)
    frame_column2_value = tk.Frame(frame, width=frame.winfo_width() * 0.4)

    # 将两个子框架放置在frame2_left中
    frame_column1_title.pack(side='left', fill='y', padx=(10, 0))
    frame_column1_value.pack(side='left', fill='y', padx=(10, 0), pady=(0, 10))
    frame_column2_title.pack(side='left', fill='both', padx=(10, 0))
    frame_column2_value.pack(side='left', fill='both', padx=(10, 0), pady=(0, 10), expand=True)

    # 定义column1的内容
    column1 = ['PID', 'hwnd', '焦点', '最大', '最小', ]
    # 定义column2的内容
    column2 = ['名称', '大小', '位置', '程序', '路径']

    # 更新条目的方法
    def update_entries(selected_data):
        for i, item in enumerate(column1):
            entry = frame_column1_value.winfo_children()[i]
            entry.config(textvariable=tk.StringVar(value=f"{selected_data.get(item, '')}"))

        for i, item in enumerate(column2):
            entry = frame_column2_value.winfo_children()[i]
            entry.config(textvariable=tk.StringVar(value=f"{selected_data.get(item, '')}"))

    g_method.update_main_middle_by_table = update_entries

    # 在frame_left_column1中显示column1的内容
    for item in column1:
        tk.Label(frame_column1_title, text=f"{item}", font=css['font10']).pack(fill='x')
        tk.Entry(frame_column1_value,
                 textvariable=tk.StringVar(value=f"{g_data.main_middle_columns_dict.get(item, '')}"),
                 state='readonly',
                 readonlybackground='white',
                 relief='flat',
                 width=8,
                 font=css['font10']).pack(fill='x', pady=1)

    # 在frame_left_column2中显示column2的内容
    for item in column2:
        tk.Label(frame_column2_title, text=f"{item}", font=css['font10']).pack(fill='x')
        tk.Entry(
            frame_column2_value,
            textvariable=tk.StringVar(value=f"{g_data.main_middle_columns_dict.get(item, '')}"),
            state='readonly',
            readonlybackground='white',
            relief='flat',
            font=css['font10']).pack(fill='x', pady=1)
