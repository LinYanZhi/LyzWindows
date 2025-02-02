from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic.Compiler.qtproxies import QtWidgets

from lw0_0_3.config.Config import g_config
from lw0_0_3.interface.window import Ui_window_root


class PinToTop:
    obj: QtWidgets.QPushButton
    main_window: QMainWindow

    def __init__(self, ui: Ui_window_root, main_window: QMainWindow):
        self.obj = ui.pin_to_top
        self.main_window = main_window

        # 是否置顶当前窗口
        pin_to_top = self.obj
        # 更改值为配置文件中的
        is_select = g_config.data['tab1']['pin_to_top']
        pin_to_top.setChecked(is_select)
        self.set_on_top(is_select)

        # 状态改变事件
        def change_event():
            is_checked = pin_to_top.isChecked()
            # 更新至配置文件
            g_config.data['tab1']['pin_to_top'] = is_checked
            g_config.update()
            if is_checked:
                print("tab1: 置顶")
                self.set_on_top(True)
            else:
                print("tab1: 取消置顶")
                self.set_on_top(False)

        # 绑定状态改变事件
        pin_to_top.stateChanged.connect(change_event)

    # 设置窗口置顶
    def set_on_top(self, on_top):
        self.main_window.original_flags = self.main_window.windowFlags()
        if on_top:
            self.main_window.setWindowFlags(self.main_window.original_flags | Qt.WindowStaysOnTopHint)
        else:
            self.main_window.setWindowFlags(self.main_window.original_flags & ~Qt.WindowStaysOnTopHint)
        self.main_window.show()  # 重新显示窗口以应用新的窗口标志

    pass