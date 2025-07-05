# 负责所有窗口信息与控制
import win32gui
import win32con
import win32process
import psutil


class Windows:
    # 获取所有窗口信息：句柄、大小、位置、标题、启动程序、启动程序路径、窗口状态（最大化、显示、最小化……）
    @staticmethod
    def get_all_windows_info():
        windows_info = []

        def enum_windows_callback(hwnd, windows_info):
            if win32gui.IsWindowVisible(hwnd):
                window_title = win32gui.GetWindowText(hwnd)
                left, top, right, bottom = win32gui.GetWindowRect(hwnd)
                width = right - left
                height = bottom - top
                _, pid = win32process.GetWindowThreadProcessId(hwnd)
                try:
                    process = psutil.Process(pid)
                    process_name = process.name()
                    process_path = process.exe()
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    process_name = ""
                    process_path = ""
                if win32gui.IsIconic(hwnd):
                    window_state = "最小化"
                else:
                    # 使用 GetWindowPlacement 检查窗口是否最大化
                    placement = win32gui.GetWindowPlacement(hwnd)
                    if placement[1] == win32con.SW_SHOWMAXIMIZED:
                        window_state = "最大化"
                    else:
                        window_state = "显示"
                windows_info.append({
                    "句柄": hwnd,
                    "大小": (width, height),
                    "位置": (left, top),
                    "标题": window_title,
                    "启动程序": process_name,
                    "启动程序路径": process_path,
                    "窗口状态": window_state
                })

        win32gui.EnumWindows(enum_windows_callback, windows_info)
        return windows_info

    # 根据句柄获取窗口的信息
    @staticmethod
    def get_window_info_by_hwnd(hwnd):
        if win32gui.IsWindow(hwnd):
            window_title = win32gui.GetWindowText(hwnd)
            left, top, right, bottom = win32gui.GetWindowRect(hwnd)
            width = right - left
            height = bottom - top
            _, pid = win32process.GetWindowThreadProcessId(hwnd)
            try:
                process = psutil.Process(pid)
                process_name = process.name()
                process_path = process.exe()
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                process_name = ""
                process_path = ""
            if win32gui.IsIconic(hwnd):
                window_state = "最小化"
            else:
                # 使用 GetWindowPlacement 检查窗口是否最大化
                placement = win32gui.GetWindowPlacement(hwnd)
                if placement[1] == win32con.SW_SHOWMAXIMIZED:
                    window_state = "最大化"
                else:
                    window_state = "显示"
            return {
                "句柄": hwnd,
                "大小": (width, height),
                "位置": (left, top),
                "标题": window_title,
                "启动程序": process_name,
                "启动程序路径": process_path,
                "窗口状态": window_state
            }
        else:
            return None

    # 设置窗口的位置：x,y 或者 左上角 正上方 右上角 左侧 居中 右侧 左下角 正下方 右下角
    @staticmethod
    def set_window_position(hwnd, position):
        try:
            import win32api  # 导入 win32api 用于获取屏幕尺寸
            screen_width = win32api.GetSystemMetrics(0)
            screen_height = win32api.GetSystemMetrics(1)

            # 获取窗口当前的宽度和高度
            left, top, right, bottom = win32gui.GetWindowRect(hwnd)
            window_width = right - left
            window_height = bottom - top

            if isinstance(position, tuple) and len(position) == 2:
                x, y = position
                win32gui.SetWindowPos(hwnd, None, x, y, 0, 0, win32con.SWP_NOSIZE)
            elif isinstance(position, str):
                if position == "左上角":
                    x, y = 0, 0
                elif position == "正上方":
                    x, y = screen_width // 2 - window_width // 2, 0
                elif position == "右上角":
                    x, y = screen_width - window_width, 0
                elif position == "左侧":
                    x = 0
                    y = screen_height // 2 - window_height // 2
                elif position == "居中":
                    x, y = screen_width // 2 - window_width // 2, screen_height // 2 - window_height // 2
                elif position == "右侧":
                    x = screen_width - window_width
                    y = screen_height // 2 - window_height // 2
                elif position == "左下角":
                    x, y = 0, screen_height - window_height
                elif position == "正下方":
                    x, y = screen_width // 2 - window_width // 2, screen_height - window_height
                elif position == "右下角":
                    x, y = screen_width - window_width, screen_height - window_height
                elif position == "靠上":
                    x, y = left, 0
                elif position == "靠左":
                    x, y = 0, top
                elif position == "靠右":
                    x, y = screen_width - window_width, top
                elif position == "靠下":
                    x, y = left, screen_height - window_height
                win32gui.SetWindowPos(hwnd, None, x, y, 0, 0, win32con.SWP_NOSIZE)
        except Exception as e:
            print(f"设置窗口位置时出错: {e}")

    # 设置窗口的大小：width,height 或者 预设大小
    @staticmethod
    def set_window_size(hwnd, size):
        if isinstance(size, tuple) and len(size) == 2:
            width, height = size
            win32gui.SetWindowPos(hwnd, win32con.HWND_TOP, 0, 0, width, height, win32con.SWP_NOMOVE)
        # 这里可以添加预设大小的逻辑

    # 设置窗口的标题
    @staticmethod
    def set_window_title(hwnd, new_title):
        if win32gui.IsWindow(hwnd):
            win32gui.SetWindowText(hwnd, new_title)

    # 设置窗口的状态：最大化、显示、最小化……
    @staticmethod
    def set_window_state(hwnd, state):
        if win32gui.IsWindow(hwnd):
            if state == "最大化":
                win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
            elif state == "最小化":
                win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)
            elif state == "显示":
                win32gui.ShowWindow(hwnd, win32con.SW_SHOW)

    # 关闭窗口
    @staticmethod
    def close_window(hwnd):
        if win32gui.IsWindow(hwnd):
            win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)

        return

    pass


if __name__ == '__main__':
    # 测试
    # 创建 Windows 类的实例
    windows = Windows()

    # 测试获取所有窗口信息
    all_windows_info = windows.get_all_windows_info()
    print("所有窗口信息：")
    for info in all_windows_info:
        print(info)

    # 若有窗口信息，取第一个窗口的句柄进行后续测试
    if all_windows_info:
        test_hwnd = all_windows_info[0]["句柄"]

        # 测试根据句柄获取窗口信息
        window_info = windows.get_window_info_by_hwnd(test_hwnd)
        print("\n根据句柄获取的窗口信息：")
        print(window_info)

        # # 测试设置窗口位置到居中
        # windows.set_window_position(test_hwnd, "居中")
        # print("\n窗口位置已设置为居中")

        # # 测试设置窗口大小
        # windows.set_window_size(test_hwnd, (800, 600))
        # print("窗口大小已设置为 800x600")

        # # 测试设置窗口标题
        # new_title = "测试窗口标题"
        # windows.set_window_title(test_hwnd, new_title)
        # print(f"窗口标题已设置为 {new_title}")

        # # 测试设置窗口状态为最小化
        # windows.set_window_state(test_hwnd, "最小化")
        # print("窗口状态已设置为最小化")

        # # 测试关闭窗口
        # windows.close_window(test_hwnd)
        # print("窗口已发送关闭请求")
    else:
        print("未找到可见窗口，无法进行测试。")
    pass
