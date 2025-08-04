# -*- coding: utf-8 -*-
"""
窗口管理工具
功能：通过快捷键实现窗口位置调整和大小缩放
依赖库：pip install pywin32 psutil keyboard pynput win10toast
"""

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

# ===== 全局配置常量 =====
SCALE_STEP = 0.1  # 缩放比例步长
MOVE_STEP = 10  # 移动步长（像素）
NOTIFICATION_DURATION = 2  # 通知显示持续时间（秒）

# ===== 模式状态标志 =====
shift_vertical_move = True  # True: Shift+滚轮垂直移动窗口，False: 水平移动
ctrl_vertical_scale = True  # True: Ctrl+滚轮高度缩放，False: 宽度缩放

# ===== 按键状态管理 =====
last_shift_press_time = 0  # 上次按下Shift键的时间戳
last_ctrl_press_time = 0  # 上次按下Ctrl键的时间戳
shift_first_press = True  # Shift键首次按下标志
ctrl_first_press = True  # Ctrl键首次按下标志

# ===== 鼠标中键监听相关 =====
DOUBLE_CLICK_TIMEOUT = 0.5  # 双击判定时间阈值（秒）
toaster = ToastNotifier()  # Windows通知对象


# ===== 窗口操作函数 =====

def get_top_window_info():
    """
    获取当前活动窗口信息
    返回：包含窗口标题、尺寸、句柄和路径的字典
    """
    # 获取当前激活的窗口句柄
    hwnd = win32gui.GetForegroundWindow()

    # 获取窗口标题
    title = win32gui.GetWindowText(hwnd)

    # 获取窗口位置和尺寸
    left, top, right, bottom = win32gui.GetWindowRect(hwnd)
    width, height = right - left, bottom - top

    # 获取进程信息
    _, pid = win32process.GetWindowThreadProcessId(hwnd)
    try:
        path = psutil.Process(pid).exe()
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        path = "无法获取进程路径"

    return {
        "标题": title,
        "宽度": width,
        "高度": height,
        "句柄": hwnd,
        "启动程序路径": path
    }


def move_window(hwnd, x, y):
    """移动窗口到指定位置，保持原尺寸不变"""
    win32gui.SetWindowPos(hwnd, None, x, y, 0, 0, win32con.SWP_NOSIZE)


def scale_window(hwnd, scale_factor):
    """
    等比例缩放窗口
    scale_factor: 缩放系数，正数放大，负数缩小
    """
    # 获取窗口当前的位置和尺寸
    left, top, right, bottom = win32gui.GetWindowRect(hwnd)
    width, height = right - left, bottom - top

    # 计算新尺寸
    new_width = int(width * (1 + scale_factor))
    new_height = int(height * (1 + scale_factor))

    # 获取屏幕边界
    screen_width = win32api.GetSystemMetrics(0)
    screen_height = win32api.GetSystemMetrics(1)

    # 限制窗口不超出屏幕
    new_width = min(new_width, screen_width)
    new_height = min(new_height, screen_height)

    # 计算居中位置
    new_left = (screen_width - new_width) // 2
    new_top = (screen_height - new_height) // 2

    # 应用新位置和尺寸
    win32gui.SetWindowPos(hwnd, None, new_left, new_top,
                          new_width, new_height, win32con.SWP_NOZORDER)


def scale_width(hwnd, scale_factor):
    """仅缩放窗口宽度"""
    left, top, right, bottom = win32gui.GetWindowRect(hwnd)
    width = right - left
    screen_width = win32api.GetSystemMetrics(0)

    # 计算新宽度
    new_width = int(width * (1 + scale_factor))
    new_width = min(new_width, screen_width)  # 限制不超出屏幕

    # 保持垂直位置不变，水平居中
    new_left = (screen_width - new_width) // 2
    win32gui.SetWindowPos(hwnd, None, new_left, top,
                          new_width, bottom - top, win32con.SWP_NOZORDER)


def scale_height(hwnd, scale_factor):
    """仅缩放窗口高度"""
    left, top, right, bottom = win32gui.GetWindowRect(hwnd)
    height = bottom - top
    screen_height = win32api.GetSystemMetrics(1)

    # 计算新高度
    new_height = int(height * (1 + scale_factor))
    new_height = min(new_height, screen_height)  # 限制不超出屏幕

    # 保持水平位置不变，垂直居中
    new_top = (screen_height - new_height) // 2
    win32gui.SetWindowPos(hwnd, None, left, new_top,
                          right - left, new_height, win32con.SWP_NOZORDER)


def format_output(hwnd):
    """格式化窗口信息用于日志输出"""
    left, top, right, bottom = win32gui.GetWindowRect(hwnd)
    # return f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 位置({left}, {top}), 大小({right - left}x{bottom - top})"
    return f" 位置({left}, {top}), 大小({right - left}x{bottom - top})"


# ===== 快捷键处理函数 =====

def on_hotkey(key, position):
    """处理Alt+数字键位置快捷键"""
    hwnd = win32gui.GetForegroundWindow()
    if not hwnd: return

    # 获取屏幕和窗口尺寸
    screen_width = win32api.GetSystemMetrics(0)
    screen_height = win32api.GetSystemMetrics(1)
    win_width, win_height = win32gui.GetWindowRect(hwnd)[2:]

    # 键盘数字键对应位置映射
    positions = {
        '1': (0, screen_height - win_height),  # 左下
        '2': ((screen_width - win_width) // 2, screen_height - win_height),  # 下中
        '3': (screen_width - win_width, screen_height - win_height),  # 右下
        '4': (0, (screen_height - win_height) // 2),  # 左中
        '5': ((screen_width - win_width) // 2, (screen_height - win_height) // 2),  # 中间
        '6': (screen_width - win_width, (screen_height - win_height) // 2),  # 右中
        '7': (0, 0),  # 左上
        '8': ((screen_width - win_width) // 2, 0),  # 上中
        '9': (screen_width - win_width, 0)  # 右上
    }

    if key in positions:
        x, y = positions[key]
        move_window(hwnd, x, y)
        # print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}, alt+{key}, {format_output(hwnd)}")
        print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}, alt+{key}, {format_output(hwnd)}")


def on_scale_up():
    """放大窗口快捷键处理"""
    hwnd = win32gui.GetForegroundWindow()
    if hwnd:
        scale_window(hwnd, SCALE_STEP)
        print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}, 缩放按键, {format_output(hwnd)}")


def on_scale_down():
    """缩小窗口快捷键处理"""
    hwnd = win32gui.GetForegroundWindow()
    if hwnd:
        scale_window(hwnd, -SCALE_STEP)
        print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}, 缩放按键, {format_output(hwnd)}")


# ===== 鼠标滚轮操作处理 =====

def on_mouse_wheel(x, y, dx, dy):
    """
    处理鼠标滚轮事件
    dy > 0：滚轮上滚（缩小/向上移动）
    dy < 0：滚轮下滚（放大/向下移动）
    """
    scale_factor = SCALE_STEP if dy > 0 else -SCALE_STEP
    hwnd = win32gui.GetForegroundWindow()
    if not hwnd: return

    # 获取窗口当前位置
    left, top, right, bottom = win32gui.GetWindowRect(hwnd)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 根据按下的辅助键执行不同操作
    if keyboard.is_pressed('alt'):
        # Alt+滚轮：等比例缩放
        scale_window(hwnd, scale_factor)
        print(f"{timestamp}, alt+鼠标滚轮, {format_output(hwnd)}")

    elif keyboard.is_pressed('shift'):
        # Shift+滚轮：窗口移动
        if shift_vertical_move:
            new_top = top - dy * MOVE_STEP
            move_window(hwnd, left, new_top)
            print(f"{timestamp}, shift+鼠标滚轮, 垂直移动, 位置:({left}, {new_top})")
        else:
            new_left = left - dy * MOVE_STEP
            move_window(hwnd, new_left, top)
            print(f"{timestamp}, shift+鼠标滚轮, 水平移动, 位置:({new_left}, {top})")

    elif keyboard.is_pressed('ctrl'):
        # Ctrl+滚轮：单轴缩放
        if ctrl_vertical_scale:
            scale_height(hwnd, scale_factor)
            print(f"{timestamp}, ctrl+鼠标滚轮, 缩放高度, {format_output(hwnd)}")
        else:
            scale_width(hwnd, scale_factor)
            print(f"{timestamp}, ctrl+鼠标滚轮, 缩放宽度, {format_output(hwnd)}")


# ===== 操作模式切换函数 =====

def on_shift_double_press():
    """Shift模式切换：水平/垂直移动"""
    global shift_vertical_move
    shift_vertical_move = not shift_vertical_move
    mode = "垂直移动" if shift_vertical_move else "水平移动"
    show_notification("Shift 模式切换", mode)


def on_ctrl_double_press():
    """Ctrl模式切换：高度/宽度缩放"""
    global ctrl_vertical_scale
    ctrl_vertical_scale = not ctrl_vertical_scale
    mode = "高度缩放" if ctrl_vertical_scale else "宽度缩放"
    show_notification("Ctrl 模式切换", mode)


def show_notification(title, message):
    """显示Windows通知"""
    toaster.show_toast(title, message, duration=NOTIFICATION_DURATION, threaded=True)


# ===== 双击检测逻辑 =====

def on_shift_press():
    """Shift键按下事件处理，检测双击"""
    global last_shift_press_time, shift_first_press
    current_time = time.time()

    if shift_first_press:
        last_shift_press_time = current_time
        shift_first_press = False
    elif current_time - last_shift_press_time < DOUBLE_CLICK_TIMEOUT:
        on_shift_double_press()
        shift_first_press = True
        last_shift_press_time = 0


def on_shift_release():
    """Shift键释放事件处理，重置状态"""
    global shift_first_press
    shift_first_press = True


def on_ctrl_press():
    """Ctrl键按下事件处理，检测双击"""
    global last_ctrl_press_time, ctrl_first_press
    current_time = time.time()

    if ctrl_first_press:
        last_ctrl_press_time = current_time
        ctrl_first_press = False
    elif current_time - last_ctrl_press_time < DOUBLE_CLICK_TIMEOUT:
        on_ctrl_double_press()
        ctrl_first_press = True
        last_ctrl_press_time = 0


def on_ctrl_release():
    """Ctrl键释放事件处理，重置状态"""
    global ctrl_first_press
    ctrl_first_press = True


# ===== 鼠标中键处理 =====

def on_click(x, y, button, pressed):
    """处理鼠标点击事件"""
    global shift_vertical_move, ctrl_vertical_scale
    if button == mouse.Button.middle and pressed:
        # Shift+鼠标中键：切换移动模式
        if keyboard.is_pressed('shift'):
            on_shift_double_press()
        # Ctrl+鼠标中键：切换缩放模式
        elif keyboard.is_pressed('ctrl'):
            on_ctrl_double_press()
    return True


# ===== 方向键移动功能 =====

def on_move_left():
    """Shift+左方向键：将窗口移动到屏幕左边缘"""
    hwnd = win32gui.GetForegroundWindow()
    if hwnd:
        left, top, _, _ = win32gui.GetWindowRect(hwnd)
        move_window(hwnd, 0, top)
        print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}, alt+左方向键, {format_output(hwnd)}")


def on_move_right():
    """Shift+右方向键：将窗口移动到屏幕右边缘"""
    hwnd = win32gui.GetForegroundWindow()
    if hwnd:
        left, top, right, bottom = win32gui.GetWindowRect(hwnd)
        screen_width = win32api.GetSystemMetrics(0)
        new_left = screen_width - (right - left)
        move_window(hwnd, new_left, top)
        print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}, alt+右方向键, {format_output(hwnd)}")


def on_move_up():
    """Shift+上方向键：将窗口移动到屏幕顶部"""
    hwnd = win32gui.GetForegroundWindow()
    if hwnd:
        left, top, _, _ = win32gui.GetWindowRect(hwnd)
        move_window(hwnd, left, 0)
        print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}, alt+上方向键, {format_output(hwnd)}")


def on_move_down():
    """Shift+下方向键：将窗口移动到屏幕底部"""
    hwnd = win32gui.GetForegroundWindow()
    if hwnd:
        left, top, right, bottom = win32gui.GetWindowRect(hwnd)
        screen_height = win32api.GetSystemMetrics(1)
        new_top = screen_height - (bottom - top)
        move_window(hwnd, left, new_top)
        print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}, alt+下方向键, {format_output(hwnd)}")


# ===== 注册快捷键 =====

def register_hotkeys():
    """注册所有需要的快捷键"""
    # Alt+数字键：窗口位置预设
    keyboard.add_hotkey('alt+1', on_hotkey, args=('1', '左下角'))
    keyboard.add_hotkey('alt+2', on_hotkey, args=('2', '正下方'))
    keyboard.add_hotkey('alt+3', on_hotkey, args=('3', '右下角'))
    keyboard.add_hotkey('alt+4', on_hotkey, args=('4', '左中'))
    keyboard.add_hotkey('alt+5', on_hotkey, args=('5', '中间'))
    keyboard.add_hotkey('alt+6', on_hotkey, args=('6', '右中'))
    keyboard.add_hotkey('alt+7', on_hotkey, args=('7', '左上角'))
    keyboard.add_hotkey('alt+8', on_hotkey, args=('8', '正上方'))
    keyboard.add_hotkey('alt+9', on_hotkey, args=('9', '右上角'))

    # Shift+方向键：边缘对齐
    keyboard.add_hotkey('shift+left', on_move_left)
    keyboard.add_hotkey('shift+right', on_move_right)
    keyboard.add_hotkey('shift+up', on_move_up)
    keyboard.add_hotkey('shift+down', on_move_down)

    # 键位监听（模式切换）
    keyboard.on_press_key('shift', lambda _: on_shift_press())
    keyboard.on_release_key('shift', lambda _: on_shift_release())
    keyboard.on_press_key('ctrl', lambda _: on_ctrl_press())
    keyboard.on_release_key('ctrl', lambda _: on_ctrl_release())


# ===== 主程序入口 =====

if __name__ == "__main__":
    # 注册所有快捷键
    register_hotkeys()

    # 启动鼠标监听器
    listener = mouse.Listener(on_click=on_click, on_scroll=on_mouse_wheel)
    listener.start()

    print("窗口管理工具已启动")
    print("主要功能:")
    print("1. Alt+1~9: 快速定位窗口到预设位置")
    print("2. Alt+方向键: 对齐到屏幕边缘")
    print("3. Shift+鼠标滚轮: 移动窗口")
    print("4. Ctrl+鼠标滚轮: 缩放窗口")
    print("5. Shift+中键: 切换移动模式(水平/垂直)")
    print("6. Ctrl+中键: 切换缩放模式(宽度/高度)")

    try:
        # 主循环保持程序运行
        keyboard.wait()
    except KeyboardInterrupt:
        print("程序已退出")
