import pygetwindow as gw
import pyautogui
import win32gui
import win32process
import psutil
from pygetwindow import Win32Window


class MyWindow:
    # 标题
    title = None
    # 窗口大小
    size = (0, 0)
    # 窗口位置
    position = (0, 0)
    # 窗口进程号
    pid = None
    # 窗口句柄
    hwnd = None
    # 窗口启动程序
    exec = None
    # 窗口启动程序路径
    exec_path = None
    # 是否激活
    is_active = False
    # 是否最大化
    is_max = False
    # 是否最小化
    is_min = False
    # 窗口对象
    win_obj = None

    # 设置窗口大小 (100,100) '100x100' '100,100'
    def set_size(self, size: tuple | str):
        if isinstance(size, str):
            if 'x' in size:
                size = tuple(map(int, size.split('x')))
            elif ',' in size:
                size = tuple(map(int, size.split(',')))
            else:
                raise ValueError("size 格式错误, 需含 'x' or ','")
        elif isinstance(size, tuple):
            size = (int(size[0]), int(size[1]))
        else:
            raise ValueError("size 格式错误, 需为 tuple 或 str")
        # 设置
        self.win_obj.resizeTo(*size)
        self.size = size[0], size[1]
        # 居中
        self.set_dock_opt()
        return

    # 设置窗口位置 (100,100) '100x100' '100,100'
    def set_position(self, position: tuple | str):
        if isinstance(position, str):
            if ',' in position:
                position = tuple(map(int, position.split(',')))
            else:
                raise ValueError("position 格式错误, 需含 ','")
        elif isinstance(position, tuple):
            position = (int(position[0]), int(position[1]))
        else:
            raise ValueError("position 格式错误, 需为 tuple 或 str")
        # 设置
        self.win_obj.moveTo(*position)
        self.position = position[0], position[1]
        return

    # 设置窗口停靠
    def set_dock(self, horizontal='middle', vertical='middle'):
        if horizontal == 'left':
            x = 0
        elif horizontal == 'middle':
            x = pyautogui.size()[0] // 2 - self.size[0] // 2
        elif horizontal == 'right':
            x = pyautogui.size()[0] - self.size[0]
        else:
            raise ValueError("horizontal 错误, 需为 'left', 'middle', 'right'")
        if vertical == 'top':
            y = 0
        elif vertical == 'middle':
            y = pyautogui.size()[1] // 2 - self.size[1] // 2
        elif vertical == 'bottom':
            y = pyautogui.size()[1] - self.size[1]
        else:
            raise ValueError("vertical 错误, 需为 'top', 'middle', 'bottom'")
        self.set_position((x, y))
        return

    # 窗口停靠优化
    def set_dock_opt(self, model=5):
        model = int(model)
        if model == 7:
            self.set_dock('left', 'top')
        elif model == 8:
            self.set_dock('middle', 'top')
        elif model == 9:
            self.set_dock('right', 'top')
        elif model == 4:
            self.set_dock('left', 'middle')
        elif model == 5:
            self.set_dock('middle', 'middle')
        elif model == 6:
            self.set_dock('right', 'middle')
        elif model == 1:
            self.set_dock('left', 'bottom')
        elif model == 2:
            self.set_dock('middle', 'bottom')
        elif model == 3:
            self.set_dock('right', 'bottom')
        else:
            raise ValueError("model 错误, 需为 1-9")
        return

    # 重写打印函数
    def __str__(self):
        _ = [
            'title',
            'size',
            'position',
            'pid',
            'hwnd',
            'exec',
            'exec_path',
            'is_active',
            'is_max',
            'is_min'
        ]
        _max_len = max([len(i) for i in _]) + 2
        return (
                f"title: ".rjust(_max_len) + self.title + "\n" +
                f"size: ".rjust(_max_len) + str(self.size) + "\n" +
                f"position: ".rjust(_max_len) + str(self.position) + "\n" +
                f"pid: ".rjust(_max_len) + str(self.pid) + "\n" +
                f"hwnd: ".rjust(_max_len) + str(self.hwnd) + "\n" +
                f"exec: ".rjust(_max_len) + self.exec + "\n" +
                f"exec_path: ".rjust(_max_len) + self.exec_path + "\n" +
                f"is_active: ".rjust(_max_len) + str(self.is_active) + "\n" +
                f"is_max: ".rjust(_max_len) + str(self.is_max) + "\n" +
                f"is_min: ".rjust(_max_len) + str(self.is_min)
        )

    def __repr__(self):
        return "." + self.__str__()

    # 构造
    def __init__(self, win_obj: Win32Window):
        self.win_obj = win_obj
        self.title = win_obj.title
        self.size = win_obj.width, win_obj.height
        self.position = win_obj.left, win_obj.top
        self.is_active = win_obj.isActive
        self.is_max = win_obj.isMaximized
        self.is_min = win_obj.isMinimized

        # 使用 win32gui 和 win32process 获取进程ID
        self.hwnd = win_obj._hWnd
        _, self.pid = win32process.GetWindowThreadProcessId(self.hwnd)

        # 使用psutil获取进程信息
        try:
            proc = psutil.Process(self.pid)
            self.exec = proc.name()
            self.exec_path = proc.exe()
        except psutil.NoSuchProcess:
            print("根据pid解析进行信息失败，无法获取进程信息。")
        return

    # 获取值
    def to_list(self):
        return [
            self.title,
            self.exec,
            f"{self.size[0]}x{self.size[1]}",
            f"{self.position[0]},{self.position[1]}",
            self.pid,
            self.hwnd,
            self.exec_path,
            self.is_active,
            self.is_max,
            self.is_min
        ]

    pass
