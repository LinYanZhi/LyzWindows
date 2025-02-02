import threading
import time

from lw0_0_3.data.Data import g_data
from lw0_0_3.interface.event.tab_operate.Dock import Dock
from lw0_0_3.interface.event.tab_operate.Location import Location
from lw0_0_3.interface.event.tab_operate.Opacity import Opacity
from lw0_0_3.interface.event.tab_operate.Size import Size
from lw0_0_3.interface.event.tab_operate.Status import Status
from lw0_0_3.interface.window import Ui_window_root


class TabOperate:
    ui: Ui_window_root = None

    def __init__(self, ui: Ui_window_root):
        self.ui = ui
        # 窗口紧靠
        dock = Dock(self.ui)
        # 窗口预设大小
        size = Size(self.ui)
        # 窗口位置
        location = Location(self.ui)
        # 窗口状态
        status = Status(self.ui)
        # 窗口透明度
        opacity = Opacity(self.ui)

        return

    pass
