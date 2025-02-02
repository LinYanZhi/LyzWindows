from lw0_0_3.data.Data import g_data
from lw0_0_3.interface.window import Ui_window_root


class Dock:
    ui: Ui_window_root = None

    def __init__(self, ui: Ui_window_root):
        self.ui = ui
        self.init_dock()
        self.init_dock2()
        return

    def init_dock(self):
        def fn(model: str):
            if g_data.select_window is None:
                print("当前没有选择窗口")
                return
            g_data.select_window.dock_window_simple(model, activate=False).update()

        # 靠上方
        button_dock_up = self.ui.button_dock_up
        button_dock_up.clicked.connect(lambda: fn("up"))
        # 靠下方
        button_dock_down = self.ui.button_dock_down
        button_dock_down.clicked.connect(lambda: fn("down"))
        # 靠左方
        button_dock_left = self.ui.button_dock_left
        button_dock_left.clicked.connect(lambda: fn("left"))
        # 靠右方
        button_dock_right = self.ui.button_dock_right
        button_dock_right.clicked.connect(lambda: fn("right"))
        # 水平居中
        button_dock_h_center = self.ui.button_dock_h_center
        button_dock_h_center.clicked.connect(lambda: fn("h_center"))
        # 垂直居中
        button_dock_v_center = self.ui.button_dock_v_center
        button_dock_v_center.clicked.connect(lambda: fn("v_center"))

        return

    def init_dock2(self):
        def fn2(num: int):
            if g_data.select_window is None:
                print("当前没有选择窗口")
                return
            g_data.select_window.dock_window(num, activate=False).update()

        # 左上角
        button_dock_7 = self.ui.button_dock_7
        button_dock_7.clicked.connect(lambda: fn2(7))
        # 正上方
        button_dock_8 = self.ui.button_dock_8
        button_dock_8.clicked.connect(lambda: fn2(8))
        # 右上角
        button_dock_9 = self.ui.button_dock_9
        button_dock_9.clicked.connect(lambda: fn2(9))
        # 正左方
        button_dock_4 = self.ui.button_dock_4
        button_dock_4.clicked.connect(lambda: fn2(4))
        # 正中央
        button_dock_5 = self.ui.button_dock_5
        button_dock_5.clicked.connect(lambda: fn2(5))
        # 正右方
        button_dock_6 = self.ui.button_dock_6
        button_dock_6.clicked.connect(lambda: fn2(6))
        # 左下角
        button_dock_1 = self.ui.button_dock_1
        button_dock_1.clicked.connect(lambda: fn2(1))
        # 正下方
        button_dock_2 = self.ui.button_dock_2
        button_dock_2.clicked.connect(lambda: fn2(2))
        # 右下角
        button_dock_3 = self.ui.button_dock_3
        button_dock_3.clicked.connect(lambda: fn2(3))
        return

    pass
