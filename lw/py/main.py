import os

from MyWindowUtils import *

text = """\
LyzWindows 0.0.2
+----------+-------------
| ls       |
| get  <?> | <?> title=? pid=? exec=?
| move <?> | <?> title=? pid=? exec=?
| size <?> |1,1
+----------+------------
"""

while True:
    os.system('cls')
    print(text)

    user_input = input("> ")
    my_windows = get_my_windows_use()

    if user_input == "ls":
        for i, window in enumerate(my_windows):
            print(i + 1)
            print(window)
            print("-" * 50)
        pass

    if user_input.startswith("get "):
        user_input = user_input[4:]
        if '=' not in user_input:
            print("错误：参数无效")
            continue
        param1, param2 = user_input.split("=")
        if param1 == 'title':
            my_windows = get_mw_by_title(my_windows, param2)
        elif param1 == 'pid':
            my_windows = get_mw_by_pid(my_windows, param2)
        elif param1 == 'exec':
            my_windows = get_mw_by_exec(my_windows, param2)
        else:
            print("错误：参数无效")
            continue
        for i, window in enumerate(my_windows):
            print(i + 1)
            print(window)
            print("-" * 50)
        pass

    os.system('pause>nul')
