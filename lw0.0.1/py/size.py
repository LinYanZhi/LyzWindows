from _ import find_window_by_title


def resize_window(title, width, height):
    window = find_window_by_title(title)
    print(width, height)
    if window:
        window.resizeTo(width, height)
        print(f"窗口 '{title}' 已调整大小为 {width}x{height}")
    else:
        print(f"没有找到标题为 '{title}' 的窗口。")

    return
