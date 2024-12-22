import os
import sys
import pygetwindow as gw
import pyautogui as pg

from _ import get_active_window, print_len
from exclude import init

# 初始化
exclude_list = init(
    dir=os.path.dirname(sys.argv[0]),
    exclude_name="exclude.txt"
)


# 获取所有窗口标题
def list_windows():
    # print("查看窗口标题：")
    windows = gw.getAllTitles()
    count = 1
    limit_len = 1
    active_title = get_active_window().title
    for i, win_title in enumerate(windows):
        wh = gw.getWindowsWithTitle(win_title)[0].size
        if win_title not in exclude_list and wh.width > limit_len and wh.height > limit_len and win_title:
            _ = " " if active_title != win_title else "*"
            print(f"{_}{f'({str(count)})'.rjust(4)}", end=' ')
            print(f"{str(wh.width).rjust(print_len)} x {str(wh.height).ljust(print_len)}", end='   ')
            print(f"{win_title}")
            count += 1
    else:
        print()


def main():
    list_windows()


if __name__ == "__main__":
    main()
