import time

import pyautogui

from _ import find_window_by_title


def move_window(title, x, y):
    window = find_window_by_title(title)
    if window:
        window.moveTo(x, y)
        print(f"窗口 '{title}' 已移动到 {x},{y}")
    else:
        print(f"没有找到标题为 '{title}' 的窗口。")
    return


def move_window_center(title):
    window = find_window_by_title(title)
    new_x = (pyautogui.size().width - window.width) // 2
    new_y = (pyautogui.size().height - window.height) // 2
    if window:
        window.moveTo(new_x, new_y)
        print(f"窗口 '{title}' 已移动到屏幕中心。")
    else:
        print(f"没有找到标题为 '{title}' 的窗口。")
    return


def move_window_by_num(title, x, y):
    window = find_window_by_title(title)
    if not window:
        print(f"没有找到标题为 '{title}' 的窗口。")
        return

    window.moveTo(x, y)
    print(f"窗口 '{title}' 已移动到 {x},{y}")
    return


def move_window_to(title, horizontal='middle', vertical='middle'):
    window = find_window_by_title(title)
    if not window:
        print(f"没有找到标题为 '{title}' 的窗口。")
        return

    screen_width, screen_height = pyautogui.size()
    window_width, window_height = window.size

    # 计算新的 x 位置
    if horizontal == 'left':
        new_x = 0
    elif horizontal == 'right':
        new_x = screen_width - window_width
    else:  # middle
        new_x = (screen_width - window_width) // 2

    # 计算新的 y 位置
    if vertical == 'top':
        new_y = 0
    elif vertical == 'bottom':
        new_y = screen_height - window_height
    else:  # middle
        new_y = (screen_height - window_height) // 2

    # window.restore()
    # window.activate()
    window.moveTo(new_x, new_y)
    # window.minimize()  # 窗口最小化
    window.restore()  # 窗口恢复
    print(f"窗口 '{title}' 已移动到 {horizontal}({new_x}),{vertical}({new_y})")
    return
