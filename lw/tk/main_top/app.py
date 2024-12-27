import os.path
import sys
import tkinter as tk
from tkinter import ttk

from LyzWindows.lw.py.MyWindowUtils import *
from LyzWindows.lw.tk.globe import g_data, g_method, g_object
from LyzWindows.lw.tk.css import css


def init_frame(frame, root):
    # 在frame1中创建一个标题
    temp_frame = tk.Frame(frame)
    title_label = tk.Label(temp_frame, text="所有窗口信息：", font=css['font10'])
    title_label.pack(side='left', padx=(10, 0))  # 设置为左对齐，并在左侧添加内边距
    button = tk.Button(temp_frame, text="刷新(ctrl+r)(右键)", font=css['font10'], relief='flat',
                       command=on_refresh_click)
    button.pack(side='left', padx=(0, 10), pady=1)  # 设置为右对齐，并在右侧添加内边距
    # 创建一个按钮，初始不置于顶层
    top_button = tk.Button(temp_frame, text="↓", width=5)
    top_button.pack(side='right', padx=(0, 10))
    temp_frame.pack(fill='x')  # 使temp_frame填充水平空间
    root.attributes('-topmost', g_data.is_on_top)

    # 按钮点击事件处理函数
    def toggle_top():
        if g_data.is_on_top:
            # 如果按钮已经在顶层，则取消置于顶层
            top_button.lower()
            top_button.config(text="↙")
        else:
            # 如果按钮不在顶层，则置于顶层
            top_button.lift()
            top_button.config(text="↓")
        # 切换标志状态
        g_data.is_on_top = not g_data.is_on_top
        root.attributes('-topmost', g_data.is_on_top)

    # 绑定按钮点击事件
    top_button.config(command=toggle_top)

    # 获取数据
    exclude_path = g_data.get_exclude_items()
    my_windows = get_my_windows()
    my_windows = exclude_by_items(my_windows, exclude_path)
    for item in my_windows:
        g_data.main_top_table_data.append(item.to_list())

    # 增加序号：
    column_names = ['#'] + g_data.main_top_tabel_column_name
    data = [[i + 1] + item for i, item in enumerate(g_data.main_top_table_data)]

    # 创建表格样式并设置字体
    style = ttk.Style()
    style.configure("Treeview.Heading", font=css['font10'])
    style.configure("Treeview", font=('JetBrain Mono', 11))

    # 创建表格
    tree = ttk.Treeview(frame, columns=column_names, show='headings', style="Treeview")

    # 设置列名
    for col in column_names:
        tree.heading(col, text=col)
        tree.column(col, anchor='center')

    # 添加数据
    for item in data:
        tree.insert('', 'end', values=item)

    tree.pack(expand=True, fill='both', padx=10, pady=(0, 10))

    # 更新表格数据的方法
    def update_tree_data(data):
        for item in tree.get_children():
            tree.delete(item)
        for item in data:
            tree.insert('', 'end', values=item)

    g_method.refresh_table_data = update_tree_data

    # 绑定单元格点击事件
    tree.bind('<Button-1>', on_cell_click)

    return


def on_cell_click(event):
    # 获取被点击的单元格的列和行
    tree = event.widget
    item_id = tree.identify_row(event.y)
    # 获取整行的值
    row_values = tree.item(item_id, 'values')

    if row_values is None or len(row_values) < 11:
        g_method.update_main_middle_by_table({})
        g_data.main_top_select_row = {}
        g_object.main_bottom_window_width.delete(0, tk.END)
        g_object.main_bottom_window_height.delete(0, tk.END)
        g_object.main_bottom_window_x.delete(0, tk.END)
        g_object.main_bottom_window_y.delete(0, tk.END)
        return

    # for i, item in enumerate(row_values):
    #     print(i, item)

    obj = {
        'PID': row_values[5],
        'hwnd': row_values[6],
        '焦点': row_values[8],
        '最大': row_values[9],
        '最小': row_values[10],
        '名称': row_values[1],
        '大小': row_values[3],
        '位置': row_values[4],
        '程序': row_values[2],
        '路径': row_values[7]
    }
    # 更新到全局变量中
    g_data.main_top_select_row = obj
    g_method.update_main_middle_by_table(obj)
    # w, h
    width, height = row_values[3].split('x')
    g_object.main_bottom_window_width.delete(0, tk.END)
    g_object.main_bottom_window_width.insert(0, width)
    g_object.main_bottom_window_height.delete(0, tk.END)
    g_object.main_bottom_window_height.insert(0, height)
    # x, y
    x, y = row_values[4].split(',')
    g_object.main_bottom_window_x.delete(0, tk.END)
    g_object.main_bottom_window_x.insert(0, x)
    g_object.main_bottom_window_y.delete(0, tk.END)
    g_object.main_bottom_window_y.insert(0, y)

    return


def on_refresh_click():
    # 清空历史数据
    g_data.main_top_table_data = []
    exclude_path = g_data.get_exclude_items()
    my_windows = get_my_windows()
    my_windows = exclude_by_items(my_windows, exclude_path)
    for i, item in enumerate(my_windows):
        g_data.main_top_table_data.append([i + 1] + item.to_list())
    g_method.refresh_table_data(g_data.main_top_table_data)
    # 清空选择的
    g_data.main_top_select_row = {}
    g_method.update_main_middle_by_table({})
    g_object.main_bottom_window_width.delete(0, tk.END)
    g_object.main_bottom_window_height.delete(0, tk.END)
    g_object.main_bottom_window_x.delete(0, tk.END)
    g_object.main_bottom_window_y.delete(0, tk.END)
    # 颜色恢复
    g_object.main_bottom_button_wh.config(bg='SystemButtonFace')
    g_object.main_bottom_button_xy.config(bg='SystemButtonFace')
    return
