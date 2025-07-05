# 务必要导入
import threading
import time

import pyautogui

w, h = pyautogui.size()
print(f"screen: {w}x{h}")

# 负责Python环境找到改脚本的内容根路径
import os
import sys

sys.path.append(r'D:\JetBrainsCode\PyCharm_code\Lyz\LyzWindows')
print("this:", sys.argv[0])
path = os.path.join(os.path.dirname(sys.argv[0]), "path.txt")
print("path:", path)
with open(path, "r") as f:
    config_dir_path = f.read()
    sys.path.append(config_dir_path)
print("path:")
for i, item in enumerate(sys.path):
    print(f"{i + 1:>3}", item)
print()

from PyQt5 import QtWidgets

from lw0_0_3.data.Obj import g_obj
from lw0_0_3.interface.window import Ui_window_root
from lw0_0_3.interface.event.Event import Event

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)  # 创建一个QApplication，也就是你要开发的应用程序
    mainWindow = QtWidgets.QMainWindow()  # 创建一个QMainWindow，用来装载你需要的各种组件、控件
    tabWidget = QtWidgets.QTabWidget()  # 创建一个QTabWidget，用来装载多个页面
    ui = Ui_window_root()  # ui是你创建的ui类的实例化对象，这里调用的便是刚才生成的register.py中的Ui_MainWindow类
    ui.setupUi(tabWidget)  # 执行类中的setupUi方法，方法的参数是第二步中创建的QMainWindow4

    # 绑定事件
    event = Event(ui, mainWindow, tabWidget)
    g_obj.event_key = event.event_key

    mainWindow.setCentralWidget(tabWidget)  # 将QTabWidget设置为QMainWindow的中心组件
    mainWindow.resize(tabWidget.size())  # 设置窗口大小
    # mainWindow.setFixedSize(tabWidget.size())
    mainWindow.move(525, 166)
    mainWindow.show()  # 执行QMainWindow的show()方法，显示这个QMainWindow

    # 获取窗口的宽高和位置
    # 多线程
    # def fn():
    #     while True:
    #         print("window:", mainWindow.size(), mainWindow.pos())
    #         time.sleep(1)
    # thread = threading.Thread(target=fn)
    # thread.start()
    sys.exit(app.exec())  # 使用exit()或者点击关闭按钮退出QApplication
