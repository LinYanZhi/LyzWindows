from win32process import GetWindowThreadProcessId
import win32gui
import win32api
import win32con
import psutil

TAB = " " * 4


# 别名 根据exe后缀名
ALIAS_DICT_BY_EXE_SUFFIX = {
    "explorer.exe": "文件资源管理器",
    "notepad.exe": "Notepad",
    "notepad++.exe": "Notepad++",
    "WindowsTerminal.exe": "新终端",

    "ShadowBot.Shell.exe": "影刀",
    "DingTalk.exe": "钉钉",
    "msedge.exe": "Edge",

    "pycharm64.exe": "PyCharm",
    "datagrip64.exe": "DataGrip",
    "webstorm64.exe": "WebStorm",
    "TraeCN.exe": "TraeCN",

    "ToDesk.exe": "ToDesk",
    "AweSun.exe": "向日葵",
    "PixPin.exe": "PixPin",
}


# 窗口大小类
class WindowSize:
    width: int = 0  # 窗口宽度
    height: int = 0  # 窗口高度

    def print(self, format=False):
        string = [
            f"Size(",
            f"{TAB}width={self.width}, ",
            f"{TAB}height={self.height}",
            f")"
        ]
        if format:
            return f"\n".join(string)
        else:
            return "".join(string).replace("\n", "").replace(" ", "")

    pass


# 窗口位置类
class WindowPosition:
    x: int = 0  # 窗口横坐标
    y: int = 0  # 窗口纵坐标

    def print(self, format=False):
        string = [
            f"Position(",
            f"{TAB}x={self.x}, ",
            f"{TAB}y={self.y}",
            f")"
        ]
        if format:
            return f"\n".join(string)
        else:
            return "".join(string).replace("\n", "").replace(" ", "")
    pass


# 窗口底层类
class WindowBase:
    handle: int = 0  # 窗口句柄
    pid: int = 0  # 进程ID
    exe_path: str = ""  # 进程路径
    sub_exe_path: str = ""  # 部分路径(有的路径太长)

    # 初始化一个窗口底层
    def __init__(self, handle: int):
        self.handle = handle
        # 修复：GetWindowThreadProcessId 返回 (thread_id, process_id)
        _, self.pid = GetWindowThreadProcessId(handle)
        
        # 修复：使用 psutil 获取进程路径更简单可靠
        try:
            process = psutil.Process(self.pid)
            self.exe_path = process.exe()
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            raise Exception("无法获取进程路径")

        if len(self.exe_path) > 40:
            exe_path_list = self.exe_path.split("\\")
            self.sub_exe_path = "\\".join([
                exe_path_list[0],
                exe_path_list[1],
                "..." ,
                # exe_path_list[-2],
                exe_path_list[-1],
            ])
        else:
            self.sub_exe_path = self.exe_path


    def print(self, format=False, complete=False):
        string = [
            f"WindowBase(",
            f"{TAB}handle={self.handle}, ",
            f"{TAB}pid={self.pid}, ",
            f"{TAB}exe_path={self.exe_path}" if complete else \
            f"{TAB}sub_exe_path={self.sub_exe_path}",
            f")"
        ]
        if format:
            return f"\n".join(string)
        else:
            return "".join(string).replace("\n", "").replace(" ", "")
    pass


# 窗口控制类
class WindowControl:
    handle: int = None  # 窗口句柄
    
    # 初始化一个窗口控制类
    def __init__(self, handle: int):
        self.handle = handle
    
    # 窗口移动
    def move(self, x: int, y: int):
        win32gui.SetWindowPos(self.handle, None, x, y, 0, 0, win32con.SWP_NOSIZE)
    # 窗口大小
    def resize(self, width: int, height: int):
        win32gui.SetWindowPos(self.handle, None, 0, 0, width, height, win32con.SWP_NOMOVE)



    pass



# 窗口类
class Windows:
    title: str = ""  # 窗口标题
    name: str = ""  # 根据title自定义名称
    size: WindowSize = None  # 窗口大小
    position: WindowPosition = None  # 窗口位置
    base: WindowBase = None  # 窗口底层
    control: WindowControl = None  # 窗口控制类

    def print(self, format=False, deep_format=False, complete=False):

        self_size = f"\n{TAB}".join(self.size.print(deep_format).split("\n"))
        self_position = f"\n{TAB}".join(self.position.print(deep_format).split("\n"))
        self_base = f"\n{TAB}".join(self.base.print(deep_format, complete).split("\n"))

        string = [
            f"Windows(",
            f"{TAB}name={self.name}, ",
            f"{TAB}title={self.title}, ",
            f"{TAB}size={self_size}, ",
            f"{TAB}position={self_position}, ",
            f"{TAB}base={self_base}",
            f")"
        ]

        if format:
            return "\n".join(string)
        else:
            return "".join(string).replace("\n", "").replace(" ", "")

    # 初始化一个窗口
    def __init__(self, handle: int):
        if not win32gui.IsWindowVisible(handle):
            raise Exception("窗口句柄无效")

        # 初始化底层
        self.base = WindowBase(handle)
        # 初始化窗口信息
        self.title = win32gui.GetWindowText(handle)
        self.size = WindowSize()
        self.size.width, self.size.height = win32gui.GetWindowRect(handle)[2:]
        self.position = WindowPosition()
        self.position.x, self.position.y = win32gui.GetWindowRect(handle)[:2]
        # 别名
        self.name = '?'
        # 别名根据exe后缀名
        exe_suffix = self.base.exe_path.split("\\")[-1]
        if exe_suffix in ALIAS_DICT_BY_EXE_SUFFIX:
            self.name = ALIAS_DICT_BY_EXE_SUFFIX[exe_suffix]
        # 初始化窗口控制类
        self.control = WindowControl(handle)



    # 判断窗口是否可见
    def is_visible(self) -> bool:
        return win32gui.IsWindowVisible(self.base.handle) == 1

    # 判断窗口大小是否正常
    def is_size_normal(self) -> bool:
        if self.size.width == 0 and self.size.height == 0:
            return False
        if self.size.width == 1 and self.size.height == 1:
            return False
        else:
            return True


    pass


# 窗口工具类
class WindowTool:
    # 获取顶层窗口句柄
    @staticmethod
    def get_top_window_handle() -> int:
        return win32gui.GetForegroundWindow()

    # 获取所有窗口句柄
    @staticmethod
    def get_all_window_handle() -> list:
        window_handle_list = []
        def enum_windows_callback(hwnd, lParam):
            if win32gui.IsWindowVisible(hwnd):
                window_handle_list.append(hwnd)
        win32gui.EnumWindows(enum_windows_callback, None)
        return window_handle_list

    # 更新窗口
    @staticmethod
    def update_window(window: Windows):
        return Windows(window.base.handle)

    # 获取屏幕宽高像素
    @staticmethod
    def get_screen_size() -> WindowSize:
        screen_size = WindowSize()
        screen_size.width, screen_size.height = win32api.GetSystemMetrics(0), win32api.GetSystemMetrics(1)
        return screen_size

    

