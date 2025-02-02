from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeyEvent, QMouseEvent
from PyQt5.QtWidgets import QTableWidgetItem, QAbstractItemView, QMenu, QMainWindow

from lw0_0_3.config.Config import g_config
from lw0_0_3.data.Data import g_data
from lw0_0_3.entity.WindowObj import WindowObj
from lw0_0_3.entity.Windows import Windows
from lw0_0_3.interface.event.EventKey import EventKey
from lw0_0_3.interface.event.tab_home.PinToTop import PinToTop
from lw0_0_3.interface.event.tab_home.Table import Table
from lw0_0_3.interface.window import Ui_window_root


class TabHome:
    ui: Ui_window_root = None
    main_window: QMainWindow = None

    def __init__(self, ui: Ui_window_root, event_key: EventKey, main_window: QMainWindow):
        self.ui = ui
        self.main_window = main_window

        # 初始化置顶按钮
        self.pin_to_top = PinToTop(self.ui, self.main_window)
        # 初始化表格
        self.table = Table(self.ui, event_key)
        # 初始化底部 具体信息

        return
