import time

from PyQt5.QtCore import QEvent, Qt, QPoint
from PyQt5.QtGui import QMouseEvent, QKeyEvent

from lw0_0_3.data.Data import g_data
from lw0_0_3.data.Obj import g_obj
from lw0_0_3.entity.WindowObj import WindowObj
from lw0_0_3.interface.event.tab_home.Bottom import Bottom
from lw0_0_3.interface.event.tab_home.Table import Table
from lw0_0_3.interface.window import Ui_window_root


class Status:
    ui: Ui_window_root = None

    def __init__(self, ui: Ui_window_root):
        self.ui = ui
        self.init_status()
        return

    def init_status(self):
        def fn(model: str):
            if g_data.select_window is None:
                print("请先选择窗口")
                return

            def fn():
                time.sleep(0.1)
                g_obj.mouse_right_click_event(QMouseEvent(
                    QMouseEvent.MouseButtonPress,
                    QPoint(1, 1),
                    Qt.RightButton,
                    Qt.NoButton,
                    Qt.NoModifier
                ))

            window: WindowObj = g_data.select_window
            if model == 'show':
                window.activate_window().update()
            elif model == 'hide':
                window.hide_window().update()
                fn()
            elif model == 'max':
                window.maximize_window().update()
            elif model == 'min':
                window.minimize_window().update()
            elif model == 'close':
                window.close_window().update()
                fn()

            return

        self.ui.button_window_show.clicked.connect(lambda: fn('show'))
        self.ui.button_window_hide.clicked.connect(lambda: fn('hide'))
        self.ui.button_window_max.clicked.connect(lambda: fn('max'))
        self.ui.button_window_min.clicked.connect(lambda: fn('min'))
        self.ui.button_window_close.clicked.connect(lambda: fn('close'))

    pass
