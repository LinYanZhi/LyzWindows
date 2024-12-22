import sys
import time

import pygetwindow as gw

from list import main as list_main
from list_all import main as list_all_main
from size import resize_window
from move import move_window_to, move_window_by_num
from _ import get_window_info_by_title

# 接收参数
command = """\
查看
    lw list
    lw list all
    lw get 窗口标题
宽高
    lw size 窗口标题 模板0~9
    lw size 窗口标题 宽x高
位置
    lw move 窗口标题 模式1~9
    lw move 窗口标题 horizontal vertical
"""

refer = [
    ["1938", "1098", "full"],
    ["1920", "1080", "screen"],
    ["1770", "1000", "jetbrains"],
    ["1663", "938", "智谱清言"],
    ["1550", "980", "~"],
    ["1410", "809", "夸克,钉钉"],
    ["1321", "940", "music"],
    ["1313", "750", "explorer"],
    ["1259", "770", "cmd"],
    ["1080", "800", "微信"],
]


def main():
    print(sys.argv)
    global command

    if len(sys.argv) < 2:
        print("用法： lw <命令> [选项]")
        print(command)
        print("参考：")
        # 格式化输出
        count = 0
        for i in refer:
            # f""格式化 左对齐输出
            print(f"{count:>2}    {i[0]:>4},{i[1]:<4} {i[2]}", end="   *\n" if i[2] == 'explorer' else "\n")
            count += 1

        return

    command = sys.argv[1]

    # lw list
    if command in ["list", "ls"] and len(sys.argv) == 2:
        list_main()
        return

    # lw list all
    elif command in ["list", "ls"] and len(sys.argv) == 3:
        if sys.argv[2] in ["all", "a", "-a"]:
            list_all_main()
        elif sys.argv[2].startswith(("time=", "t=")):
            sleep_second = float(sys.argv[2].split("=")[1])
            print(f"稍等...{sleep_second}s")
            time.sleep(sleep_second)
            list_main()
        return

    elif command == "size":
        # lw size <window_title> <size>
        if len(sys.argv) == 4:
            window_title = sys.argv[2]
            size = sys.argv[3]
            if "," in size or "x" in size:
                width, height = size.split("," if "," in size else "x")
            else:
                # 数字 直接对应大小
                width, height, _ = refer[int(size)]
            resize_window(window_title, int(width), int(height))
            move_window_to(window_title)
        else:
            print("有效的输入：lw size <window_title> <size>")
            exit(1)
        return

    elif command == "move":
        if len(sys.argv) != 4 and len(sys.argv) != 5:
            print("有效的输入：lw move <window_title> <num>")
            print("有效的输入：lw move <window_title> <horizontal> <vertical>")
            exit(1)

        # lw move <window_title> <num>
        window_title = sys.argv[2]
        if len(sys.argv) == 4:
            num = sys.argv[3]
            key_value = {
                "7": ["left", "top"],
                "8": ["middle", "top"],
                "9": ["right", "top"],
                "4": ["left", "middle"],
                "5": ["middle", "middle"],
                "6": ["right", "middle"],
                "1": ["left", "bottom"],
                "2": ["middle", "bottom"],
                "3": ["right", "bottom"],
            }
            if num not in key_value:
                print("无效的数字，请输入1-9")
                exit(1)
            value = key_value[num]
            move_window_to(window_title, *value)
            return

        horizontal = sys.argv[3]
        vertical = sys.argv[4]

        # lw move <window_title> <x> <y>
        _ = False
        try:
            x = int(horizontal)
            y = int(vertical)
            _ = True
            move_window_by_num(window_title, x, y)
            return
        except ValueError:
            pass

        # lw move <window_title> <horizontal> <vertical>
        move_window_to(window_title, horizontal, vertical)
        return

    elif command == "get" and len(sys.argv) == 3:
        window_title = sys.argv[2]
        get_window_info_by_title(window_title)
        return

    elif command in ["help", "h", "-h", "--help"]:
        print("作者：林彦智")
        print("版本：1.0.0")
        print("功能：根据窗口标题修改窗体大小和位置。")
        print("命令：")
        print("1.查看窗口标题    lw list|ls [all]")
        print("2.修改窗口大小    lw size <window_title> <size>   size: 宽x高|宽,高|0-9")
        print("3.移动窗口位置    lw move <window_title> <size>   size: x y|水平 垂直")
        print("4.获取具体窗口    lw get <window_title>")
        print("5.帮助           lw help|h")
        return

    else:
        print("无效的命令或参数。")


if __name__ == "__main__":
    main()
