import win32api
import win32gui
import win32process
import psutil
import re

from typing import List


# 定义路径通配符和对应标题的映射
PATH_PATTERN_ALIAS = {
    # 电脑上自带的软件
    r'.*WindowsTerminal.exe': "CMD",
    r'.*explorer.exe': "文件资源管理器",
    r'.*msedge.exe': "Edge",

    # 我的必装软件
    r'.*notepad\+\+\.exe': "Notepad++",

    # Jet Brains 软件
    r'.*datagrip64.exe': "DataGrip",
    r'.*pycharm64.exe': "PyCharm",
    r'.*idea64.exe': "IDEA",
    r'.*webstorm64.exe': "WebStorm",
    r'.*phpstorm64.exe': "PHPStorm",

    # 其他软件
    r'.*Trae\ CN.exe': "TraeCN",
    r'.*DingTalk.exe': "钉钉",
    r'.*ShadowBot\.Shell\.exe': "影刀",
}


def get_my_title_by_path(path: str) -> str:
    """
    根据传入的路径和预定义的通配符规则，返回对应的自定义标题。

    :param path: 待匹配的文件路径
    :return: 匹配到的自定义标题，如果没有匹配则返回空字符串
    """
    for pattern, alias in PATH_PATTERN_ALIAS.items():
        if re.match(pattern, path):
            # print("alias = ", alias)
            return alias
    return "?" 



# 这是一个窗口类
class Window:
    """最关键的两个属性：句柄and进程id"""
    handle: int  # 句柄
    pid: int  # 进程id

    """其他属性"""
    title: str  # 标题
    position: tuple  # 位置
    size: tuple  # 大小
    launch_path: str  # 启动路径

    """自定义属性"""
    # 我给起的标题
    my_title: str = ""


    def __init__(self, handle: int):
        self.handle = handle
        # 根据句柄获取窗口标题
        self.title = win32gui.GetWindowText(handle)
        # 根据句柄获取窗口位置
        self.position = win32gui.GetWindowRect(handle)
        # 根据句柄获取窗口大小
        left, top, right, bottom = win32gui.GetWindowRect(handle)
        self.size = (right - left, bottom - top)
        # 初始化pid和启动路径
        self.pid = None
        self.launch_path = None
        
        try:
            # 获取窗口所属进程的PID
            thread_id, pid = win32process.GetWindowThreadProcessId(handle)
            self.pid = pid
            
            # 尝试方法1: 使用psutil获取进程路径
            try:
                process = psutil.Process(pid)
                self.launch_path = process.exe()
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                # 方法1失败，尝试方法2: 使用win32api和psapi获取进程路径
                try:
                    import ctypes
                    from ctypes import wintypes
                    
                    psapi = ctypes.WinDLL('psapi')
                    kernel32 = ctypes.WinDLL('kernel32')
                    
                    # 打开进程
                    PROCESS_QUERY_INFORMATION = 0x0400
                    PROCESS_VM_READ = 0x0010
                    h_process = kernel32.OpenProcess(
                        PROCESS_QUERY_INFORMATION | PROCESS_VM_READ,
                        False,
                        pid
                    )
                    
                    if h_process:
                        # 获取进程路径
                        path_buf = ctypes.create_string_buffer(1024)
                        if psapi.GetModuleFileNameExA(h_process, None, path_buf, ctypes.sizeof(path_buf)):
                            self.launch_path = path_buf.value.decode('utf-8')
                        kernel32.CloseHandle(h_process)
                except Exception:
                    # 所有方法都失败，保留launch_path为None
                    pass
            
            # 如果成功获取到路径，则设置自定义标题
            if self.launch_path:
                self.my_title = get_my_title_by_path(self.launch_path)
            else:
                self.my_title = "??"
        except Exception as e:
            # 记录异常信息但不中断程序
            print(f"获取窗口信息时出错: {e}")

            pass
        return
        
    pass


# 这是一个核心类
class Core:
    # 获取显示器的分辨率
    @staticmethod
    def get_screen_size() -> tuple:
        return win32api.GetSystemMetrics(0), win32api.GetSystemMetrics(1)
    
    # 获取当前电脑的所有窗口 包装数据到Window中 返回List[Window]
    @staticmethod
    def get_all_windows(include_invisible=False, include_child_windows=False, filter_no_title=True) -> List[Window]:
        windows = []
        
        # 定义一个回调函数 用于枚举窗口
        def enum_window_callback(hwnd, lParam):
            # 根据参数决定是否包含不可见窗口
            if include_invisible or win32gui.IsWindowVisible(hwnd):
                windows.append(Window(hwnd))
                
            # 如果需要包含子窗口，递归枚举
            if include_child_windows:
                win32gui.EnumChildWindows(hwnd, enum_window_callback, None)
        
        # 枚举所有顶级窗口
        win32gui.EnumWindows(enum_window_callback, None)
        
        # 根据参数决定是否过滤没有标题的窗口
        if filter_no_title:
            windows = [window for window in windows if window.title]
        
        # 过滤掉没有位置的窗口（位置为(0,0,0,0)通常是无效窗口）
        windows = [window for window in windows if window.position != (0, 0, 0, 0)]
        
        return windows

def print_help():
    """显示帮助信息"""
    print("窗口管理工具使用帮助")
    print("====================")
    print("可用命令:")
    print("  window list [选项]    - 列出所有窗口")
    print("    选项:")
    print("      -t, --title       - 显示窗口标题")
    print("      -mt, --my-title   - 显示自定义标题")
    print("      -pid, --process-id - 显示进程ID")
    print("      -exe, --path      - 显示启动路径")
    print("      -wh, --size       - 显示窗口大小")
    print("      -xy, --position   - 显示窗口位置")
    print("  window info <pid>     - 显示指定PID的窗口详细信息")
    print("  window use <pid>      - 使用指定PID的窗口（预留功能）")
    print("  help                  - 显示此帮助信息")
    print("  exit, quit            - 退出程序")
    print("\n示例:")
    print("  window list                     # 列出所有窗口的基本信息")
    print("  window list --title --my-title  # 显示标题和自定义标题")
    print("  window list -pid -exe           # 显示PID和启动路径")
    print("  window info 1234                # 显示PID为1234的窗口详细信息")


def parse_command(command):
    """解析命令行参数"""
    parts = command.strip().lower().split()
    if not parts:
        return [], []
    
    main_cmd = parts[0]
    args = parts[1:]
    
    return main_cmd, args


if __name__ == '__main__':
    print("窗口管理终端模式启动成功！")
    print("输入 'help' 获取帮助信息。")
    
    while True:
        try:
            command = input("\nSystem: ").strip()
            
            if command in ['exit', 'quit']:
                print("程序已退出。")
                break
            
            if command == 'help':
                print_help()
                continue
            
            main_cmd, args = parse_command(command)
            
            # 获取所有窗口
            windows = Core.get_all_windows()
            
            if main_cmd == 'window' and args and args[0] == 'list':
                # 处理 window list 命令
                show_title = False
                show_my_title = False
                show_pid = False
                show_path = False
                show_size = False
                show_position = False
                
                # 如果没有指定任何选项，默认显示标题和PID
                if len(args) == 1:
                    show_title = True
                    show_pid = True
                
                # 解析选项
                for arg in args[1:]:
                    if arg in ['-t', '--title']:
                        show_title = True
                    elif arg in ['-mt', '--my-title']:
                        show_my_title = True
                    elif arg in ['-pid', '--process-id']:
                        show_pid = True
                    elif arg in ['-exe', '--path']:
                        show_path = True
                    elif arg in ['-wh', '--size']:
                        show_size = True
                    elif arg in ['-xy', '--position']:
                        show_position = True
                    elif arg in ['-handle', '--handle']:
                        show_handle = True

                    else:
                        print(f"未知选项: {arg}")
                        print("使用 'window list --help' 查看帮助")
                        break
                else:
                    # 没有break，继续执行
                    print(f"共找到 {len(windows)} 个窗口:")
                    idx_width = len(str(len(windows)))
                    handle_max_width = max(len(str(window.handle)) for window in windows)
                    pid_max_width = max(len(str(window.pid)) for window in windows)

                    for idx, window in enumerate(windows, 1):
                        line = f"{idx:{idx_width}}. "

                        parts = []
                        if show_pid:
                            parts.append(f"PID: {window.pid:{pid_max_width}}")
                        if show_handle:
                            parts.append(f"句柄: {window.handle:{handle_max_width}}")
                        if show_title:
                            parts.append(f"标题: {window.title}")
                        if show_my_title:
                            parts.append(f"自定义标题: {window.my_title}")
                        if show_path:
                            path = window.launch_path if window.launch_path else '无法获取'
                            parts.append(f"路径: {path}")
                        if show_size:
                            parts.append(f"大小: {window.size}")
                        if show_position:
                            parts.append(f"位置: {window.position}")
                        
                        print(line + " | ".join(parts))
            
            elif main_cmd == 'window' and args and args[0] == 'info' and len(args) > 1:
                # 处理 window info <pid> 命令
                try:
                    pid = int(args[1])
                    target_windows = [w for w in windows if w.pid == pid]
                    
                    if not target_windows:
                        print(f"未找到PID为 {pid} 的窗口。")
                    else:
                        print(f"找到 {len(target_windows)} 个PID为 {pid} 的窗口:")
                        for window in target_windows:
                            print("窗口信息:")
                            print(f"  句柄: {window.handle}")
                            print(f"  PID: {window.pid}")
                            print(f"  标题: {window.title}")
                            print(f"  自定义标题: {window.my_title}")
                            print(f"  位置: {window.position}")
                            print(f"  大小: {window.size}")
                            print(f"  启动路径: {window.launch_path if window.launch_path else '无法获取'}")
                            print("----------------" * 5)
                except ValueError:
                    print("无效的PID格式。请使用 'window info <数字>' 格式。")
            
            elif main_cmd == 'window' and args and args[0] == 'use' and len(args) > 1:
                # 处理 window use <pid> 命令（预留功能）
                try:
                    pid = int(args[1])
                    target_windows = [w for w in windows if w.pid == pid]
                    
                    if not target_windows:
                        print(f"未找到PID为 {pid} 的窗口。")
                    else:
                        print(f"准备使用PID为 {pid} 的窗口...")
                        print("注意: 此功能尚未实现。")
                        # 这里可以添加窗口操作的代码
                except ValueError:
                    print("无效的PID格式。请使用 'window use <数字>' 格式。")
                # 处理 window info <pid> 命令
                try:
                    pid = int(args[1])
                    target_windows = [w for w in windows if w.pid == pid]
                    
                    if not target_windows:
                        print(f"未找到PID为 {pid} 的窗口。")
                    else:
                        print(f"找到 {len(target_windows)} 个PID为 {pid} 的窗口:")
                        for window in target_windows:
                            print("窗口信息:")
                            print(f"  句柄: {window.handle}")
                            print(f"  PID: {window.pid}")
                            print(f"  标题: {window.title}")
                            print(f"  自定义标题: {window.my_title}")
                            print(f"  位置: {window.position}")
                            print(f"  大小: {window.size}")
                            print(f"  启动路径: {window.launch_path if window.launch_path else '无法获取'}")
                            print("----------------" * 5)
                except ValueError:
                    print("无效的PID格式。请使用 'window info <数字>' 格式。")
            
            else:
                print("未知命令。输入 'help' 获取帮助信息。")
        
        except KeyboardInterrupt:
            print("\n程序已中断。")
            break
        except Exception as e:
            print(f"执行命令时出错: {e}")
    


# 命令行规范设计说明
# 1. 采用层级式命令结构，主命令为 'window'
# 2. 支持多种子命令和选项，提供灵活的窗口信息查询方式
# 3. 选项可以组合使用，如 'window list -t -mt -pid'
# 4. 所有命令和选项支持简写和全写两种形式
# 5. 'window use' 命令为预留功能，可用于后续扩展窗口操作功能




