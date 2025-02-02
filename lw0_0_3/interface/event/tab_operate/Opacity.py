from lw0_0_3.data.Data import g_data
from lw0_0_3.entity.WindowObj import WindowObj
from lw0_0_3.interface.window import Ui_window_root


class Opacity:
    ui: Ui_window_root = None

    def init_opacity(self):
        def fn(opacity: float):
            if g_data.select_window is None:
                print("没有选择窗口")
                return
            window: WindowObj = g_data.select_window
            window.set_window_opacity(opacity)

        self.ui.button_opacity_100.clicked.connect(lambda: fn(1))
        self.ui.button_opacity_90.clicked.connect(lambda: fn(0.9))
        self.ui.button_opacity_80.clicked.connect(lambda: fn(0.8))
        self.ui.button_opacity_70.clicked.connect(lambda: fn(0.7))
        self.ui.button_opacity_60.clicked.connect(lambda: fn(0.6))
        self.ui.button_opacity_50.clicked.connect(lambda: fn(0.5))
        self.ui.button_opacity_40.clicked.connect(lambda: fn(0.4))
        self.ui.button_opacity_30.clicked.connect(lambda: fn(0.3))
        self.ui.button_opacity_20.clicked.connect(lambda: fn(0.2))
        self.ui.button_opacity_10.clicked.connect(lambda: fn(0.1))
        self.ui.button_opacity_0.clicked.connect(lambda: fn(0))

        return

    def __init__(self, ui: Ui_window_root):
        self.ui = ui
        self.init_opacity()

        return

    pass
