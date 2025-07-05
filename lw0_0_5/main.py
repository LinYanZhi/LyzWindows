import win32gui
import win32process
import psutil
import keyboard
import win32con
import win32api
from pynput import mouse
import time
from win10toast import ToastNotifier
from datetime import datetime

# 缩放比例步长
SCALE_STEP = 0.1

# 移动步长
MOVE_STEP = 10

# Shift 模式标志，True 表示垂直移动，False 表示水平移动
shift_vertical_move = True

# Ctrl 模式标志，True 表示高度缩放，False 表示宽度缩放
ctrl_vertical_scale = True

# 记录上次按下 Shift 键的时间
last_shift_press_time = 0
# 记录上次按下 Ctrl 键的时间
last_ctrl_press_time = 0

# 初始化 esc_first_press 变量
esc_first_press = True
last_esc_press_time = 0

# 双击超时时间
DOUBLE_CLICK_TIMEOUT = 0.5

# 新增变量，设置 win10toast 通知提示持续时间（秒）
NOTIFICATION_DURATION = 2

# 新增变量，设置防止用户长按的防抖时长（秒）
ANTI_SHAKE_DURATION = 3


def get_top_window_info():
    # 获取当前顶级窗口句柄
    hwnd = win32gui.GetForegroundWindow()

    # 获取窗口标题
    title = win32gui.GetWindowText(hwnd)

    # 获取窗口位置和大小
    left, top, right, bottom = win32gui.GetWindowRect(hwnd)
    width = right - left
    height = bottom - top

    # 获取窗口对应的进程ID
    _, pid = win32process.GetWindowThreadProcessId(hwnd)

    # 获取进程路径
    try:
        process = psutil.Process(pid)
        path = process.exe()
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
        path = "无法获取进程路径"

    return {
        "标题": title,
        "宽度": width,
        "高度": height,
        "句柄": hwnd,
        "启动程序路径": path
    }


def move_window(hwnd, x, y):
    win32gui.SetWindowPos(hwnd, None, x, y, 0, 0, win32con.SWP_NOSIZE)


def scale_window(hwnd, scale_factor):
    left, top, right, bottom = win32gui.GetWindowRect(hwnd)
    width = right - left
    height = bottom - top
    new_width = int(width * (1 + scale_factor))
    new_height = int(height * (1 + scale_factor))

    # 获取屏幕分辨率
    screen_width = win32api.GetSystemMetrics(0)
    screen_height = win32api.GetSystemMetrics(1)

    # 确保窗口不会超出屏幕边界
    new_width = min(new_width, screen_width)
    new_height = min(new_height, screen_height)

    # 重新计算窗口位置以保持居中
    new_left = (screen_width - new_width) // 2
    new_top = (screen_height - new_height) // 2

    win32gui.SetWindowPos(hwnd, None, new_left, new_top, new_width, new_height, win32con.SWP_NOZORDER)


def format_output(hwnd):
    left, top, right, bottom = win32gui.GetWindowRect(hwnd)
    width = right - left
    height = bottom - top
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return f"{current_time} 位置({left}, {top}), 大小({width}x{height})"


def on_hotkey(key, position):
    hwnd = win32gui.GetForegroundWindow()
    if hwnd:
        # 修改为使用 win32api 获取屏幕分辨率
        screen_width = win32api.GetSystemMetrics(0)
        screen_height = win32api.GetSystemMetrics(1)

        window_info = get_top_window_info()
        window_width = window_info["宽度"]
        window_height = window_info["高度"]

        positions = {
            '1': (0, screen_height - window_height),
            '2': ((screen_width - window_width) // 2, screen_height - window_height),
            '3': (screen_width - window_width, screen_height - window_height),
            '4': (0, (screen_height - window_height) // 2),
            '5': ((screen_width - window_width) // 2, (screen_height - window_height) // 2),
            '6': (screen_width - window_width, (screen_height - window_height) // 2),
            '7': (0, 0),
            '8': ((screen_width - window_width) // 2, 0),
            '9': (screen_width - window_width, 0)
        }

        if key in positions:
            x, y = positions[key]
            move_window(hwnd, x, y)
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"{current_time}, alt+{key}, {format_output(hwnd)}")


def on_scale_up():
    hwnd = win32gui.GetForegroundWindow()
    if hwnd:
        scale_window(hwnd, SCALE_STEP)
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"{current_time}, 缩放按键, {format_output(hwnd)}")


def on_scale_down():
    hwnd = win32gui.GetForegroundWindow()
    if hwnd:
        scale_window(hwnd, -SCALE_STEP)
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"{current_time}, 缩放按键, {format_output(hwnd)}")


def on_mouse_wheel(x, y, dx, dy):
    scale_factor = SCALE_STEP if dy > 0 else -SCALE_STEP
    hwnd = win32gui.GetForegroundWindow()
    if hwnd:
        left, top, right, bottom = win32gui.GetWindowRect(hwnd)
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if keyboard.is_pressed('alt'):
            scale_window(hwnd, scale_factor)
            print(f"{current_time}, alt+鼠标滚轮, {format_output(hwnd)}")
        elif keyboard.is_pressed('shift'):
            if shift_vertical_move:
                # 垂直移动
                new_top = top - dy * MOVE_STEP
                move_window(hwnd, left, new_top)
                print(f"{current_time}, shift+鼠标滚轮, 垂直移动, 位置:({left}, {new_top})")
            else:
                # 水平移动
                new_left = left - dy * MOVE_STEP
                move_window(hwnd, new_left, top)
                print(f"{current_time}, shift+鼠标滚轮, 水平移动, 位置:({new_left}, {top})")
        elif keyboard.is_pressed('ctrl'):
            if ctrl_vertical_scale:
                # 高度缩放
                scale_height(hwnd, scale_factor)
                print(f"{current_time}, ctrl+鼠标滚轮, 缩放高度, {format_output(hwnd)}")
            else:
                # 宽度缩放
                scale_width(hwnd, scale_factor)
                print(f"{current_time}, ctrl+鼠标滚轮, 缩放宽度, {format_output(hwnd)}")


def scale_width(hwnd, scale_factor):
    left, top, right, bottom = win32gui.GetWindowRect(hwnd)
    width = right - left
    new_width = int(width * (1 + scale_factor))

    # 获取屏幕分辨率
    screen_width = win32api.GetSystemMetrics(0)

    # 确保窗口宽度不会超出屏幕边界
    new_width = min(new_width, screen_width)

    # 重新计算窗口位置以保持居中
    new_left = (screen_width - new_width) // 2

    win32gui.SetWindowPos(hwnd, None, new_left, top, new_width, bottom - top, win32con.SWP_NOZORDER)


def scale_height(hwnd, scale_factor):
    left, top, right, bottom = win32gui.GetWindowRect(hwnd)
    height = bottom - top
    new_height = int(height * (1 + scale_factor))

    # 获取屏幕分辨率
    screen_height = win32api.GetSystemMetrics(1)

    # 确保窗口高度不会超出屏幕边界
    new_height = min(new_height, screen_height)

    # 重新计算窗口位置以保持居中
    new_top = (screen_height - new_height) // 2

    win32gui.SetWindowPos(hwnd, None, left, new_top, right - left, new_height, win32con.SWP_NOZORDER)


toaster = ToastNotifier()


def show_notification(title, message):
    # 使用 win10toast 显示通知，使用全局变量设置持续时间
    toaster.show_toast(title, message, duration=NOTIFICATION_DURATION, threaded=True)


def on_shift_double_press():
    global shift_vertical_move
    shift_vertical_move = not shift_vertical_move
    message = "垂直移动" if shift_vertical_move else "水平移动"
    show_notification("Shift 模式切换", message)


def on_ctrl_double_press():
    global ctrl_vertical_scale
    ctrl_vertical_scale = not ctrl_vertical_scale
    message = "高度缩放" if ctrl_vertical_scale else "宽度缩放"
    show_notification("Ctrl 模式切换", message)

# 新增标志位，记录 Shift 和 Ctrl 键是否是首次按下
shift_first_press = True
ctrl_first_press = True


def on_shift_press():
    global last_shift_press_time, shift_first_press
    current_time = time.time()
    if shift_first_press:
        # 首次按下，记录时间
        last_shift_press_time = current_time
        shift_first_press = False
    else:
        # 非首次按下，检查是否是双击
        if current_time - last_shift_press_time < DOUBLE_CLICK_TIMEOUT:
            on_shift_double_press()
            # 双击后重置标志位
            shift_first_press = True
            last_shift_press_time = 0


def on_shift_release():
    global shift_first_press
    # 按键释放时重置标志位
    shift_first_press = True


def on_ctrl_press():
    global last_ctrl_press_time, ctrl_first_press
    current_time = time.time()
    if ctrl_first_press:
        # 首次按下，记录时间
        last_ctrl_press_time = current_time
        ctrl_first_press = False
    else:
        # 非首次按下，检查是否是双击
        if current_time - last_ctrl_press_time < DOUBLE_CLICK_TIMEOUT:
            on_ctrl_double_press()
            # 双击后重置标志位
            ctrl_first_press = True
            last_ctrl_press_time = 0


def on_ctrl_release():
    global ctrl_first_press
    # 按键释放时重置标志位
    ctrl_first_press = True


def on_mouse_wheel(x, y, dx, dy):
    scale_factor = SCALE_STEP if dy > 0 else -SCALE_STEP
    hwnd = win32gui.GetForegroundWindow()
    if hwnd:
        left, top, right, bottom = win32gui.GetWindowRect(hwnd)
        if keyboard.is_pressed('alt'):
            scale_window(hwnd, scale_factor)
            left, top, right, bottom = win32gui.GetWindowRect(hwnd)
            width = right - left
            height = bottom - top
            if dy > 0:
                print(f"等比例放大, 位置:({left}, {top}), 大小:{width}x{height}")
            else:
                print(f"等比例缩小, 位置:({left}, {top}), 大小:{width}x{height}")
        elif keyboard.is_pressed('shift'):
            if shift_vertical_move:
                # 垂直移动
                new_top = top - dy * MOVE_STEP
                move_window(hwnd, left, new_top)
                print(f"垂直移动, 位置:({left}, {new_top})")
            else:
                # 水平移动
                new_left = left - dy * MOVE_STEP
                move_window(hwnd, new_left, top)
                print(f"水平移动, 位置:({new_left}, {top})")
        elif keyboard.is_pressed('ctrl'):
            if ctrl_vertical_scale:
                # 高度缩放
                scale_height(hwnd, scale_factor)
                left, top, right, bottom = win32gui.GetWindowRect(hwnd)
                width = right - left
                height = bottom - top
                print(f"缩放高度, 位置:({left}, {top}), 大小:{width}x{height}")
            else:
                # 宽度缩放
                scale_width(hwnd, scale_factor)
                left, top, right, bottom = win32gui.GetWindowRect(hwnd)
                width = right - left
                height = bottom - top
                print(f"缩放宽度, 位置:({left}, {top}), 大小: {width}x{height}")


# 删除 last_left_click_time 变量的定义

def on_click(x, y, button, pressed):
    global shift_vertical_move, ctrl_vertical_scale
    if button == mouse.Button.middle and pressed:
        if keyboard.is_pressed('shift'):
            on_shift_double_press()
        elif keyboard.is_pressed('ctrl'):
            on_ctrl_double_press()
    return


# 新增标志位，控制监听状态
listening_enabled = True

# 新增变量，记录上次切换的时间
last_esc_switch_time = 0

def on_esc_double_press():
    global listening_enabled, last_esc_switch_time
    current_time = time.time()
    # 检查是否距离上次切换超过全局变量设置的防抖时长
    if current_time - last_esc_switch_time < ANTI_SHAKE_DURATION:
        return
    listening_enabled = not listening_enabled
    message = "按键监听已启用 ✔" if listening_enabled else "按键监听已禁用 ❌"
    show_notification("监听状态切换", message)
    print(message)
    manage_listeners()
    # 更新上次切换时间
    last_esc_switch_time = current_time

def on_esc_press():
    global last_esc_press_time, esc_first_press
    current_time = time.time()
    if esc_first_press:
        # 首次按下，记录时间
        last_esc_press_time = current_time
        esc_first_press = False
    else:
        # 非首次按下，检查是否是双击
        if current_time - last_esc_press_time < DOUBLE_CLICK_TIMEOUT:
            on_esc_double_press()
            # 双击后重置标志位
            esc_first_press = True
            last_esc_press_time = 0
        else:
            # 未达到双击时间，更新时间
            last_esc_press_time = current_time

def on_esc_release():
    global esc_first_press
    # 按键释放时重置标志位
    esc_first_press = True

# 新增列表用于记录注册的热键
registered_hotkeys = []

def register_hotkeys():
    global registered_hotkeys
    hotkeys = [
        ('alt+7', on_hotkey, ('7', '左上角')),
        ('alt+8', on_hotkey, ('8', '正上方')),
        ('alt+9', on_hotkey, ('9', '右上角')),
        ('alt+4', on_hotkey, ('4', '左中')),
        ('alt+5', on_hotkey, ('5', '中间')),
        ('alt+6', on_hotkey, ('6', '右中')),
        ('alt+1', on_hotkey, ('1', '左下角')),
        ('alt+2', on_hotkey, ('2', '正下方')),
        ('alt+3', on_hotkey, ('3', '右下角')),
        # 假设添加 alt+方向键的逻辑
        ('shift+left', on_move_left, ()),  # 注册 alt+左方向键，调用 on_move_left 函数
        ('shift+right', on_move_right, ()),  # 注册 alt+右方向键，调用 on_move_right 函数
        ('shift+up', on_move_up, ()),  # 注册 alt+上方向键，调用 on_move_up 函数
        ('shift+down', on_move_down, ())  # 注册 alt+下方向键，调用 on_move_down 函数
    ]
    for hotkey, func, args in hotkeys:
        handle = keyboard.add_hotkey(hotkey, func, args=args)
        registered_hotkeys.append(hotkey)

# 定义 alt+左方向键的处理函数
def on_move_left():
    hwnd = win32gui.GetForegroundWindow()
    if hwnd:
        left, top, right, bottom = win32gui.GetWindowRect(hwnd)
        move_window(hwnd, 0, top)  # 移动窗口到新位置
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"{current_time}, alt+左方向键, {format_output(hwnd)}")

# 定义 alt+右方向键的处理函数
def on_move_right():
    hwnd = win32gui.GetForegroundWindow()
    if hwnd:
        left, top, right, bottom = win32gui.GetWindowRect(hwnd)
        # 屏幕 - 窗口宽度
        new_left = win32api.GetSystemMetrics(0) - (right - left)
        move_window(hwnd, new_left, top)  # 移动窗口到新位置
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"{current_time}, alt+右方向键, {format_output(hwnd)}")

# 定义 alt+上方向键的处理函数
def on_move_up():
    hwnd = win32gui.GetForegroundWindow()
    if hwnd:
        left, top, right, bottom = win32gui.GetWindowRect(hwnd)
        move_window(hwnd, left, 0)  # 移动窗口到新位置
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"{current_time}, alt+上方向键, {format_output(hwnd)}")

# 定义 alt+下方向键的处理函数
def on_move_down():
    hwnd = win32gui.GetForegroundWindow()
    if hwnd:
        left, top, right, bottom = win32gui.GetWindowRect(hwnd)
        new_top = win32api.GetSystemMetrics(1) - (bottom - top)
        move_window(hwnd, left, new_top)  # 移动窗口到新位置
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"{current_time}, alt+下方向键, {format_output(hwnd)}")

def manage_listeners():
    global listener, registered_hotkeys
    if listening_enabled:
        # 启用监听
        if not listener.is_alive():
            listener = mouse.Listener(on_click=on_click, on_scroll=on_mouse_wheel)
            listener.start()
        # 重新注册热键
        register_hotkeys()
    else:
        # 禁用监听
        if listener.is_alive():
            listener.stop()
        # 清除除了 Esc 键之外的所有热键
        for hotkey in registered_hotkeys:
            keyboard.remove_hotkey(hotkey)
        registered_hotkeys = []

if __name__ == "__main__":
    # 注册 Esc 键监听
    keyboard.on_press_key('esc', lambda e: on_esc_press())
    keyboard.on_release_key('esc', lambda e: on_esc_release())

    # 注册初始热键
    register_hotkeys()

    # 使用 pynput 监听鼠标点击事件
    listener = mouse.Listener(on_click=on_click, on_scroll=on_mouse_wheel)
    listener.start()

    print(
        "开始监听热键，请按 Alt + 数字键移动窗口，按 Alt + 滚轮等比例缩放窗口，Shift + 滚轮移动窗口，Ctrl + 滚轮缩放窗口...")
    try:
        keyboard.wait()
    except KeyboardInterrupt:
        print("程序已退出")


