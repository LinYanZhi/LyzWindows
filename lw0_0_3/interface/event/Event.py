# 为窗口上的动态交互设置事件
from PyQt5.QtWidgets import QMainWindow, QTabWidget

from lw0_0_3.interface.event.EventKey import EventKey
from lw0_0_3.interface.event.tab_home.TabHome import TabHome
from lw0_0_3.interface.event.tab_operate.TabOperate import TabOperate
from lw0_0_3.interface.window import Ui_window_root


class Event:
    ui: Ui_window_root = None
    main_window: QMainWindow = None
    tabWidget: QTabWidget = None

    event_key: EventKey = None

    def __init__(self, ui: Ui_window_root, main_window: QMainWindow, tabWidget: QTabWidget):
        self.ui = ui
        self.main_window = main_window
        self.tabWidget = tabWidget

        # 全局事件
        eventKey = EventKey(self.main_window, self.tabWidget)
        self.event_key = eventKey

        # 首页初始化
        self.tabHome = TabHome(self.ui, self.event_key, self.main_window)
        # 操作页初始化
        self.tabOperate = TabOperate(self.ui)



        return

    pass
