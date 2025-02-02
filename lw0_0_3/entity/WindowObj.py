import psutil
import pyautogui
import win32con
import win32gui
import win32process

"""
SWP_NOSIZE : 不改变窗口的大小
SWP_NOMOVE : 不改变窗口的位置
SWP_NOZORDER : 不改变窗口在Z序中的位置（在Z序中，一个窗口上方可以有多个窗口）
SWP_NOACTIVATE : 不激活窗口。若设置了这个标志，窗口不会获得键盘输入焦点
SWP_SHOWWINDOW : 显示窗口
SWP_HIDEWINDOW : 隐藏窗口
SWP_NOOWNERZORDER : 不改变拥有者窗口在Z序中的位置
SWP_NOREPOSITION : 不改变窗口在屏幕上的位置（无论是否设置这个标志，总是改变窗口在Z序中的位置）
SWP_DEFERERASE : 延迟重绘直到调用UpdateWindow或RedrawWindow函数
SWP_ASYNCWINDOWPOS : 异步更新窗口，如果未设置这个标志，窗口会立即更新
"""


# Windows10操作系统 窗口信息类
class WindowObj:
    # 标题
    title: str = None
    # 窗口大小
    size: tuple | list = None
    # 窗口位置
    xy: tuple | list = None
    # 窗口状态
    status: str = None

    # 窗口句柄
    hwnd: int = None
    # 窗口进程号
    pid: int = None
    # 窗口线程号
    tid: int = None
    # 窗口启动程序路径
    process_path: str = None

    # 构造
    def __init__(self, hwnd: int):
        # 获取窗口标题
        title = win32gui.GetWindowText(hwnd)
        # 获取窗口位置和大小
        left, top, right, bottom = win32gui.GetWindowRect(hwnd)
        width = right - left
        height = bottom - top
        # 获取进程ID和线程ID
        tid, pid = win32process.GetWindowThreadProcessId(hwnd)
        # 获取进程路径
        process = psutil.Process(pid)
        process_path = process.exe()
        # 获取窗口状态
        placement = win32gui.GetWindowPlacement(hwnd)
        window_state = placement[1]
        state_name = {
            win32con.SW_HIDE: '隐藏',
            win32con.SW_MINIMIZE: '最小化',
            win32con.SW_RESTORE: '还原',
            win32con.SW_SHOW: '显示',
            win32con.SW_SHOWMAXIMIZED: '最大化',
            win32con.SW_SHOWMINIMIZED: '最小化',
            win32con.SW_SHOWMINNOACTIVE: '最小化无激活',
            win32con.SW_SHOWNA: '无激活',
            win32con.SW_SHOWNOACTIVATE: '显示无激活',
            win32con.SW_SHOWNORMAL: '正常显示'
        }.get(window_state, '未知状态')

        # 赋值
        self.title = title
        self.size = (width, height)
        self.xy = (left, top)
        self.status = state_name
        # 赋值
        self.hwnd = hwnd
        self.pid = pid
        self.tid = tid
        self.process_path = process_path
        self.opacity = None
        return

    # 更新
    def update(self):
        self.__init__(self.hwnd)
        return self

    # 打印
    def __str__(self):
        return (f"title={self.title}, size={self.size}, xy={self.xy}, status={self.status}, hwnd={self.hwnd}, "
                f"pid={self.pid}, tid={self.tid}, process_path={self.process_path}, "
                f"opacity={self.opacity}, dock={self.dock}")
        # return ("{\n"
        #         f"\t标题='{self.title}'\n"
        #         f"\t大小={self.size}\n"
        #         f"\t位置={self.xy}\n"
        #         f"\t状态='{self.status}'\n"
        #         f"\thwnd={self.hwnd}\n"
        #         f"\tpid={self.pid}\n"
        #         f"\ttid={self.tid}\n"
        #         f"\t启动程序='{self.process_path}'\n"
        #         f"\t透明度={self.opacity}\n"
        #         f"\t停靠='{self.dock}'\n"
        #         "}")

    def log(self):
        print(self.__str__())
        return self

    """ 操作 """

    # 窗口透明度
    opacity: float = None

    # 设置窗口透明度
    def set_window_opacity(self, opacity):
        # 确保透明度值在0.0到1.0之间
        opacity = max(0.0, min(1.0, opacity))
        # 设置窗口扩展样式以支持透明度
        win32gui.SetWindowLong(self.hwnd, win32con.GWL_EXSTYLE,
                               win32gui.GetWindowLong(self.hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)
        # 设置透明度
        win32gui.SetLayeredWindowAttributes(self.hwnd, 0, int(opacity * 255), win32con.LWA_ALPHA)
        self.opacity = opacity
        return self

    # 获取窗口透明度
    def get_window_opacity(self):
        return self.opacity

    # 设置窗口位置
    def set_window_position(self, x, y, activate: bool = True):
        flags = win32con.SWP_NOSIZE | win32con.SWP_NOZORDER
        if not activate:
            flags |= win32con.SWP_NOACTIVATE
        win32gui.SetWindowPos(self.hwnd, None, x, y, 0, 0, flags)
        self.dock = ''
        return self

    # 获取窗口大小
    def get_window_size(self):
        rect = win32gui.GetWindowRect(self.hwnd)
        return rect[2] - rect[0], rect[3] - rect[1]

    # 设置窗口大小
    def set_window_size(self, width, height, center: bool = False, activate: bool = True):
        if width < 0 or height < 0:
            print("窗口大小不能为负数")
        width = int(width)
        height = int(height)
        flags = win32con.SWP_NOMOVE | win32con.SWP_NOZORDER
        if not activate:
            flags |= win32con.SWP_NOACTIVATE
        win32gui.SetWindowPos(self.hwnd, None, 0, 0, width, height, flags)
        self.update()
        if center:
            return self.dock_window(5, activate=activate)
        return self

    # 设置窗口大小：等比例缩放
    def set_window_proportional_scaling(self, px: int, center: bool = False, activate: bool = True):
        width, height = self.size
        ratio = width / height
        new_width = width + px
        new_height = int(new_width / ratio)
        self.set_window_size(new_width, new_height, center, activate)
        return self

    # 激活并显示窗口
    def activate_window(self):
        win32gui.ShowWindow(self.hwnd, win32con.SW_RESTORE)
        win32gui.SetForegroundWindow(self.hwnd)
        return self

    # 显示窗口
    def __show_window(self):
        win32gui.ShowWindow(self.hwnd, win32con.SW_SHOW)
        return self

    # 隐藏窗口
    def hide_window(self):
        win32gui.ShowWindow(self.hwnd, win32con.SW_HIDE)
        return self

    # 最大化窗口
    def maximize_window(self):
        win32gui.ShowWindow(self.hwnd, win32con.SW_MAXIMIZE)
        return self

    # 最小化窗口
    def minimize_window(self):
        win32gui.ShowWindow(self.hwnd, win32con.SW_MINIMIZE)
        return self

    # 关闭窗口
    def close_window(self):
        win32gui.PostMessage(self.hwnd, win32con.WM_CLOSE, 0, 0)
        return self

    # 停靠位置
    dock: str = None

    # 窗口停靠：左侧 顶部 底部 右侧 居中
    def dock_window(self, model: int, activate: bool = True):

        # 居中坐标
        screen_width, screen_height = pyautogui.size()
        width, height = self.size
        center_x = (screen_width - width) // 2
        center_y = (screen_height - height) // 2

        # 7 8 9 4 5 6 1 2 3
        if model == 7:
            self.set_window_position(0, 0, activate)
            self.dock = '左上角'
        elif model == 8:
            self.set_window_position(center_x, 0, activate)
            self.dock = '正上方'
        elif model == 9:
            self.set_window_position(screen_width - width, 0, activate)
            self.dock = '右上角'
        elif model == 4:
            self.set_window_position(0, center_y, activate)
            self.dock = '左居中'
        elif model == 5:
            self.set_window_position(center_x, center_y, activate)
            self.dock = '正居中'
        elif model == 6:
            self.set_window_position(screen_width - width, center_y, activate)
            self.dock = '右居中'
        elif model == 1:
            self.set_window_position(0, screen_height - height, activate)
            self.dock = '左下角'
        elif model == 2:
            self.set_window_position(center_x, screen_height - height, activate)
            self.dock = '正下方'
        elif model == 3:
            self.set_window_position(screen_width - width, screen_height - height, activate)
            self.dock = '右下角'
        else:
            raise ValueError("无效的停靠模式，必须为 1~9")
        return self

    # 窗口停靠：上 下 左 右 (up down left right )
    def dock_window_simple(self, model: str, activate: bool = True):

        if model == 'up':
            self.set_window_position(self.xy[0], 0, activate)
            self.dock = '紧靠上方'
        elif model == 'down':
            self.set_window_position(self.xy[0], pyautogui.size()[1] - self.size[1], activate)
            self.dock = '紧靠下方'
        elif model == 'left':
            self.set_window_position(0, self.xy[1], activate)
            self.dock = '紧靠左侧'
        elif model == 'right':
            self.set_window_position(pyautogui.size()[0] - self.size[0], self.xy[1], activate)
            self.dock = '紧靠右侧'
        elif model == 'h_center':
            self.set_window_position((pyautogui.size()[0] - self.size[0]) // 2, self.xy[1], activate)
            self.dock = '水平居中'
        elif model == 'v_center':
            self.set_window_position(self.xy[0], (pyautogui.size()[1] - self.size[1]) // 2, activate)
            self.dock = '垂直居中'
        else:
            raise ValueError("无效的停靠模式，必须为 'up' 'down' 'left' 'right'")
        return self

    # 缩放窗口 在原本的位置
    def resize_window(self, target_width, target_height, center: bool = False, activate: bool = True):
        target_width = int(target_width)
        target_height = int(target_height)
        x, y = self.xy
        flags = win32con.SWP_NOZORDER | win32con.SWP_NOACTIVATE
        if not activate:
            flags |= win32con.SWP_SHOWWINDOW

        # 设置窗口新的大小和位置
        win32gui.SetWindowPos(self.hwnd, win32con.HWND_TOP, x, y, target_width, target_height, flags)
        self.update()
        if center:
            return self.dock_window(5, activate=activate)

        return self

    pass
