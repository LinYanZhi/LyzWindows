from tkinter import Tk
import tkinter as tk
from typing import Dict

from lw0_0_4.Config import Config
from lw0_0_4.Windows import Windows


# 负责所有悬浮卡片的操作：
class FloatingCard:
    # 基本属性
    root: Tk
    config: Config

    def __init__(self, root, is_detail=False):
        """
        :param root: 主窗口对象
        :param is_detail: 是否是窗口详情页
        """
        self.root = root
        self.root.overrideredirect(True)  # 去除默认标题栏
        self.config = Config('config.json')
        self.is_detail = is_detail
        # 设置窗口大小和位置
        self.root.geometry(
            f"{self.config['width']}x{self.config['height']}+{self.config['x']}+{self.config['y']}")
        # 设置背景色
        self.root.configure(bg=self.config['bg_color'])
        # 设置置顶状态
        self.root.attributes('-topmost', self.config['is_topmost'])
        # 边框动态色
        self.current_border_color = self.config['topmost_border_color'] \
            if self.config['is_topmost'] else self.config['border_color']

        # 可调整大小的边框宽度
        self.resize_border = 5
        self.resize_direction = None
        # 创建边框组件
        self.borders = []
        self.create_borders()
        self.content_frame = tk.Frame(self.root, bg=self.config['bg_color'])
        self.content_frame.pack(fill="both", expand=True, padx=10, pady=10)
        self.window_listbox = tk.Listbox(self.content_frame, bg=self.root.cget('bg'), fg='white',
                                         selectbackground=self.current_border_color,
                                         selectforeground='white',
                                         font=('宋体', 10),
                                         activestyle='none')
        self.window_listbox.pack(fill='both', expand=True)
        # 将鼠标滚轮事件绑定到 content_frame 上
        self.content_frame.bind("<MouseWheel>", self.on_mousewheel)

        # 绑定事件
        self.root.bind("<ButtonPress-1>", self.on_press)
        self.root.bind("<B1-Motion>", self.on_drag)
        self.root.bind("<ButtonRelease-1>", self.save_position)
        # 绑定右键事件
        self.root.bind("<Button-3>", self.show_context_menu)

        # 创建右键菜单
        # 设置背景色和文字颜色
        self.context_menu = tk.Menu(self.root, tearoff=0, bg=self.config['menu_bg_color'],
                                    fg=self.config['menu_fg_color'])
        self.context_menu.add_command(label="关闭", command=self.close_window)
        # 添加置顶按钮
        self.context_menu.add_command(label="置顶"
        if not self.config['is_topmost'] else "取消置顶", command=self.toggle_topmost)
        # 添加刷新选项
        self.context_menu.add_command(label="刷新", command=self.update_window_list)

        # 调用 update_window_list 方法
        self.update_window_list()

        return

    def on_press(self, event):
        """
        处理鼠标按下事件，判断是否需要调整窗口大小
        :param event: 鼠标按下事件对象
        """
        # 强制更新窗口信息，确保获取到正确的窗口大小
        self.root.update_idletasks()

        # 获取窗口相对于屏幕的位置
        win_x = self.root.winfo_x()
        win_y = self.root.winfo_y()

        # 获取鼠标相对于屏幕的坐标
        mouse_x = event.x_root
        mouse_y = event.y_root

        # 计算鼠标相对于窗口的实际位置
        x = mouse_x - win_x
        y = mouse_y - win_y

        # 获取窗口的宽度和高度
        width, height = self.root.winfo_width(), self.root.winfo_height()

        # 判断鼠标点击位置是否在窗口的左上角
        if x < self.resize_border:
            # 判断鼠标点击位置是否在窗口的左上角
            if y < self.resize_border:
                self.resize_direction = 'nw'
            # 判断鼠标点击位置是否在窗口的左下角
            elif y > height - self.resize_border:
                self.resize_direction = 'sw'
            # 否则，鼠标点击位置在窗口的左边
            else:
                self.resize_direction = 'w'
        # 判断鼠标点击位置是否在窗口的右上角
        elif x > width - self.resize_border:
            # 判断鼠标点击位置是否在窗口的右上角
            if y < self.resize_border:
                self.resize_direction = 'ne'
            # 判断鼠标点击位置是否在窗口的右下角
            elif y > height - self.resize_border:
                self.resize_direction = 'se'
            # 否则，鼠标点击位置在窗口的右边
            else:
                self.resize_direction = 'e'
        # 判断鼠标点击位置是否在窗口的顶部
        elif y < self.resize_border:
            self.resize_direction = 'n'
        # 判断鼠标点击位置是否在窗口的底部
        elif y > height - self.resize_border:
            self.resize_direction = 's'
        # 否则，鼠标点击位置在窗口内部
        else:
            self.resize_direction = None
            # 记录鼠标按下时相对于窗口的位置
            self.offset_x = event.x
            self.offset_y = event.y
        return

    def on_drag(self, event):
        """
        处理鼠标拖拽事件，根据情况调整窗口位置或大小

        :param event: 鼠标拖拽事件对象
        """
        if self.resize_direction:
            self.perform_resize(event)
        else:
            # 强制更新窗口信息，确保获取到正确的窗口位置
            self.root.update_idletasks()
            # 计算窗口的新位置
            x = event.x_root - self.offset_x
            y = event.y_root - self.offset_y
            # 设置窗口的新位置
            self.root.geometry(f"+{x}+{y}")
        return

    def perform_resize(self, event):
        resize(self.root, self.resize_direction, event)
        return

    def on_mousewheel(self, event):
        # 获取当前窗口的位置和大小
        current_x = self.root.winfo_x()
        current_y = self.root.winfo_y()
        current_width = self.root.winfo_width()
        current_height = self.root.winfo_height()

        # 缩放比例
        scale_factor = 1.1 if event.delta > 0 else 0.9

        # 等比例缩放
        new_width = int(current_width * scale_factor)
        new_height = int(current_height * scale_factor)

        # 确保大小不小于最小值
        min_width = 50
        min_height = 50
        if new_width < min_width:
            new_width = min_width
        if new_height < min_height:
            new_height = min_height

        # 设置窗口的新大小和位置
        self.root.geometry(f"{new_width}x{new_height}+{current_x}+{current_y}")

        # 保存位置
        self.save_position(None)
        return

    def save_position(self, event):
        # 只有是非详情页时才保存
        if self.is_detail:
            return
        self.config['x'] = self.root.winfo_x()
        self.config['y'] = self.root.winfo_y()
        self.config.save_config()
        return

    def show_context_menu(self, event):
        """
        显示右键菜单

        :param event: 鼠标右键点击事件对象
        """
        try:
            # 直接使用已创建的菜单
            self.context_menu.tk_popup(event.x_root, event.y_root)
        except tk.TclError:
            pass
        return

    def close_window(self):
        self.config.save_config()
        self.root.destroy()
        return

    def toggle_topmost(self):
        self.config['is_topmost'] = not self.config['is_topmost']
        self.root.attributes('-topmost', self.config['is_topmost'])
        # 更新右键菜单标签
        self.context_menu.entryconfig(1, label="置顶" if not self.config['is_topmost'] else "取消置顶")
        # 更新边框颜色
        current_border_color = self.config['topmost_border_color'] \
            if self.config['is_topmost'] else self.config['border_color']
        for border in self.borders[:4]:  # 只更新边框，不更新角
            border.config(bg=current_border_color)
        self.save_position(None)
        return

    def create_borders(self):
        current_border_color = self.config['topmost_border_color'] \
            if self.config['is_topmost'] else self.config['border_color']
        # 顶部边框
        top_border = tk.Frame(self.root, bg=current_border_color)
        top_border.place(x=0, y=0, relwidth=1, height=self.resize_border)
        self.borders.append(top_border)

        # 底部边框
        bottom_border = tk.Frame(self.root, bg=current_border_color)
        bottom_border.place(x=0, rely=1, y=-self.resize_border, relwidth=1, height=self.resize_border)
        self.borders.append(bottom_border)

        # 左侧边框
        left_border = tk.Frame(self.root, bg=current_border_color)
        left_border.place(x=0, y=0, width=self.resize_border, relheight=1)
        self.borders.append(left_border)

        # 右侧边框
        right_border = tk.Frame(self.root, bg=current_border_color)
        right_border.place(rely=0, x=-self.resize_border, relx=1, width=self.resize_border, relheight=1)
        self.borders.append(right_border)

        # 左上角
        top_left_corner = tk.Frame(self.root, bg=self.config['corner_color'])
        top_left_corner.place(x=0, y=0, width=self.resize_border, height=self.resize_border)
        self.borders.append(top_left_corner)

        # 右上角
        top_right_corner = tk.Frame(self.root, bg=self.config['corner_color'])
        top_right_corner.place(relx=1, x=-self.resize_border, y=0, width=self.resize_border, height=self.resize_border)
        self.borders.append(top_right_corner)

        # 左下角
        bottom_left_corner = tk.Frame(self.root, bg=self.config['corner_color'])
        bottom_left_corner.place(x=0, rely=1, y=-self.resize_border, width=self.resize_border,
                                 height=self.resize_border)
        self.borders.append(bottom_left_corner)

        # 右下角
        bottom_right_corner = tk.Frame(self.root, bg=self.config['corner_color'])
        bottom_right_corner.place(relx=1, x=-self.resize_border, rely=1, y=-self.resize_border,
                                  width=self.resize_border, height=self.resize_border)
        self.borders.append(bottom_right_corner)
        return

    def update_window_list(self):
        windows = Windows()
        all_windows_info = windows.get_all_windows_info()
        self.window_listbox.delete(0, 'end')

        # 绑定双击事件到 Listbox 上
        self.window_listbox.bind("<Double-Button-1>", self.show_window_details)

        # 存储每个窗口句柄和对应的标题
        self.handle_to_title = {}

        # 分开存储有标题和无标题的窗口信息
        titled_windows = []
        untitled_windows = []

        for info in all_windows_info:
            title = info["标题"]
            handle = info.get("句柄")
            if title:
                titled_windows.append((handle, title))
            else:
                untitled_windows.append((handle, info))

        # 先显示有标题的窗口
        for handle, title in titled_windows:
            self.window_listbox.insert('end', title)
            self.handle_to_title[title] = handle

        # 再显示无标题的窗口
        for index, (handle, info) in enumerate(untitled_windows):
            title = f"无标题{index + 1}"
            self.window_listbox.insert('end', title)
            self.handle_to_title[title] = handle

        return

    def show_window_details(self, event):
        # 获取选中的索引
        selected_index = self.window_listbox.curselection()
        if selected_index:
            index = selected_index[0]
            selected_title = self.window_listbox.get(index)
            target_handle = self.handle_to_title.get(selected_title)

            if target_handle:
                windows = Windows()
                all_windows_info = windows.get_all_windows_info()

                # 通过句柄查找对应的窗口信息
                selected_info = next((info for info in all_windows_info if info.get("句柄") == target_handle), None)

                if selected_info:
                    # 打印选中的窗口信息
                    # print("选中的窗口信息：")
                    # for key, value in selected_info.items():
                    #     print(f"{key}: {value}")

                    # 创建新的弹窗展示详情
                    detail_window = tk.Toplevel(self.root)
                    # 设置新弹窗置顶
                    detail_window.attributes('-topmost', True)
                    detail_window.overrideredirect(True)  # 去除默认标题栏
                    detail_window.selected_info = selected_info  # 保存选中信息以便刷新
                    detail_window.target_handle = target_handle  # 保存窗口句柄以便刷新

                    # 创建右键菜单
                    detail_menu = tk.Menu(detail_window, tearoff=0, bg=self.config['menu_bg_color'],
                                          fg=self.config['menu_fg_color'])
                    detail_menu.add_command(label="关闭", command=detail_window.destroy)
                    detail_menu.add_command(label="刷新", command=lambda: self.refresh_detail_window(detail_window))

                    # 绑定右键事件
                    detail_window.bind("<Button-3>", lambda e: detail_menu.tk_popup(e.x_root, e.y_root))

                    # 自定义暗色标题栏
                    title_bar = tk.Frame(detail_window, bg='#333333', relief='raised', bd=2)
                    title_bar.pack(side='top', fill='x')

                    # 添加标题标签
                    title_label = tk.Label(title_bar, text="窗口详情", bg='#333333', fg='white')
                    title_label.pack(side='left', padx=10)

                    # 添加关闭按钮
                    close_button = tk.Button(title_bar, text="×", bg='#333333', fg='white', bd=0,
                                             command=detail_window.destroy)
                    close_button.pack(side='right')

                    # 绑定标题栏拖动事件
                    title_bar.bind("<ButtonPress-1>", lambda e: self.on_detail_title_bar_press(e, detail_window))
                    title_bar.bind("<B1-Motion>", lambda e: self.on_detail_title_bar_drag(e, detail_window))

                    # 设置窗口背景色
                    detail_window.configure(bg=self.config['bg_color'])

                    # 显示窗口详情信息
                    detail_window.labels = []
                    for key, value in selected_info.items():
                        label = tk.Label(detail_window, text=f"{key}: {value}", bg=self.config['bg_color'], fg='white')
                        label.pack(pady=5, padx=10, anchor='w')
                        detail_window.labels.append(label)

                    # 创建按钮容器
                    button_frame = tk.Frame(detail_window, bg=self.config['bg_color'])
                    button_frame.pack(side='top', fill='x', padx=10, pady=10)

                    # 容器 1: 3 行 3 列的操作按钮
                    container1 = tk.Frame(button_frame, bg=self.config['bg_color'])
                    container1.pack(side='left')

                    screen_width = detail_window.winfo_screenwidth()
                    screen_height = detail_window.winfo_screenheight()
                    window_width = selected_info.get('宽度', self.config['width'])
                    window_height = selected_info.get('高度', self.config['height'])

                    positions = [
                        "左上角",  # 左上角
                        "正上方",  # 正上方
                        "右上角",  # 右上角
                        "左侧",  # 左侧
                        "居中",  # 正中间
                        "右侧",  # 右侧
                        "左下角",  # 左下角
                        "正下方",  # 正下方
                        "右下角"  # 右下角
                    ]

                    buttons_text = ['↖', '↑', '↗', '←', '+', '→', '↙', '↓', '↘']

                    windows = Windows()  # 提前实例化 Windows 类

                    for i in range(3):
                        for j in range(3):
                            index = i * 3 + j
                            position = positions[index]
                            button = tk.Button(container1, text=buttons_text[index], bg=self.config['bg_color'],
                                               fg='white',
                                               command=lambda h=target_handle, p=position: windows.set_window_position(h, p))
                            button.grid(row=i, column=j, padx=5, pady=5)

                    # 容器 2: 3 行 3 列，只有上下左右 4 个实际按钮
                    container2 = tk.Frame(button_frame, bg=self.config['bg_color'])
                    container2.pack(side='left', padx=10)

                    # 上按钮
                    up_button = tk.Button(container2, text="上", bg=self.config['bg_color'], fg='white',
                                          command=lambda h=target_handle: windows.set_window_position(h, "靠上"))
                    up_button.grid(row=0, column=1, padx=5, pady=5)

                    # 左按钮
                    left_button = tk.Button(container2, text="左", bg=self.config['bg_color'], fg='white',
                                            command=lambda h=target_handle: windows.set_window_position(h, "靠左"))
                    left_button.grid(row=1, column=0, padx=5, pady=5)

                    # 右按钮
                    right_button = tk.Button(container2, text="右", bg=self.config['bg_color'], fg='white',
                                             command=lambda h=target_handle: windows.set_window_position(h, "靠右"))
                    right_button.grid(row=1, column=2, padx=5, pady=5)

                    # 下按钮
                    down_button = tk.Button(container2, text="下", bg=self.config['bg_color'], fg='white',
                                            command=lambda h=target_handle: windows.set_window_position(h, "靠下"))
                    down_button.grid(row=2, column=1, padx=5, pady=5)

                    # 新增容器 3 用于存放新按钮
                    container3 = tk.Frame(button_frame, bg=self.config['bg_color'])
                    container3.pack(side='left', padx=10)

                    import win32gui
                    import win32con

                    def maximize_window(handle):
                        win32gui.ShowWindow(handle, win32con.SW_MAXIMIZE)

                    def minimize_window(handle):
                        win32gui.ShowWindow(handle, win32con.SW_MINIMIZE)

                    def activate_window(handle):
                        win32gui.ShowWindow(handle, win32con.SW_SHOW)
                        win32gui.SetForegroundWindow(handle)

                    def restore_window(handle):
                        win32gui.ShowWindow(handle, win32con.SW_RESTORE)

                    def close_window(handle):
                        win32gui.PostMessage(handle, win32con.WM_CLOSE, 0, 0)

                    # 最大化按钮
                    maximize_btn = tk.Button(container3, text="最大化", bg=self.config['bg_color'], fg='white',
                                             command=lambda h=target_handle: maximize_window(h))
                    maximize_btn.pack(pady=2)

                    # 最小化按钮
                    minimize_btn = tk.Button(container3, text="最小化", bg=self.config['bg_color'], fg='white',
                                             command=lambda h=target_handle: minimize_window(h))
                    minimize_btn.pack(pady=2)

                    # 激活按钮
                    activate_btn = tk.Button(container3, text="激活", bg=self.config['bg_color'], fg='white',
                                             command=lambda h=target_handle: activate_window(h))
                    activate_btn.pack(pady=2)

                    # 恢复按钮
                    restore_btn = tk.Button(container3, text="恢复", bg=self.config['bg_color'], fg='white',
                                            command=lambda h=target_handle: restore_window(h))
                    restore_btn.pack(pady=2)

                    # 关闭按钮
                    close_btn = tk.Button(container3, text="关闭", bg=self.config['bg_color'], fg='white',
                                          command=lambda h=target_handle: close_window(h))
                    close_btn.pack(pady=2)

                    # 绑定全局鼠标拖拽事件
                    detail_window.bind("<ButtonPress-1>", lambda e: self.on_global_press(e, detail_window))
                    detail_window.bind("<B1-Motion>", lambda e: self.on_global_drag(e, detail_window))

        return

    def refresh_detail_window(self, detail_window):
        windows = Windows()
        all_windows_info = windows.get_all_windows_info()
        target_handle = detail_window.target_handle

        # 通过句柄查找对应的窗口信息
        selected_info = next((info for info in all_windows_info if info.get("句柄") == target_handle), None)

        if selected_info:
            # 更新标签信息
            for i, (key, value) in enumerate(selected_info.items()):
                if i < len(detail_window.labels):
                    detail_window.labels[i].config(text=f"{key}: {value}")

    def on_global_press(self, event, window):
        window.offset_x = event.x
        window.offset_y = event.y

    def on_global_drag(self, event, window):
        x = window.winfo_x() + (event.x - window.offset_x)
        y = window.winfo_y() + (event.y - window.offset_y)
        window.geometry(f"+{x}+{y}")

    def on_detail_title_bar_press(self, event, window):
        window.offset_x = event.x
        window.offset_y = event.y

    def on_detail_title_bar_drag(self, event, window):
        x = window.winfo_x() + (event.x - window.offset_x)
        y = window.winfo_y() + (event.y - window.offset_y)
        window.geometry(f"+{x}+{y}")

    def on_title_bar_press(self, event):
        self.offset_x = event.x
        self.offset_y = event.y

    def on_title_bar_drag(self, event):
        x = self.root.winfo_x() + (event.x - self.offset_x)
        y = self.root.winfo_y() + (event.y - self.offset_y)
        self.root.geometry(f"+{x}+{y}")

    pass


def resize(root, resize_direction, event):
    """
    调整窗口大小

    :param root: 主窗口对象
    :param resize_direction: 调整大小的方向
    :param event: 鼠标拖拽事件对象
    """
    # 获取当前窗口的位置和大小
    current_x = root.winfo_x()
    current_y = root.winfo_y()
    current_width = root.winfo_width()
    current_height = root.winfo_height()

    # 获取鼠标相对于屏幕的坐标
    mouse_x = event.x_root
    mouse_y = event.y_root

    new_x = current_x
    new_y = current_y
    new_width = current_width
    new_height = current_height

    # 根据不同的拖拽方向更新窗口的位置和大小
    if 'n' in resize_direction:
        new_y = mouse_y
        new_height = current_height + (current_y - new_y)
    elif 's' in resize_direction:
        new_height = mouse_y - current_y

    if 'w' in resize_direction:
        new_x = mouse_x
        new_width = current_width + (current_x - new_x)
    elif 'e' in resize_direction:
        new_width = mouse_x - current_x
        # 右侧拖拽时，窗口 x 坐标不应改变
        new_x = current_x

    # 确保窗口大小不小于最小值
    min_width = 50
    min_height = 50
    if new_width < min_width:
        if 'w' in resize_direction:
            new_x = current_x + current_width - min_width
        new_width = min_width
    if new_height < min_height:
        if 'n' in resize_direction:
            new_y = current_y + current_height - min_height
        new_height = min_height

    # 确保窗口不会超出屏幕范围
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    if new_x < 0:
        new_width += new_x
        new_x = 0
    if new_y < 0:
        new_height += new_y
        new_y = 0
    if new_x + new_width > screen_width:
        new_width = screen_width - new_x
    if new_y + new_height > screen_height:
        new_height = screen_height - new_y

    root.geometry(f"{new_width}x{new_height}+{new_x}+{new_y}")
    return
