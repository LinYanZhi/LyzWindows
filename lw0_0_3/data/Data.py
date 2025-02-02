# 全局数据
from lw0_0_3.entity.WindowObj import WindowObj
from lw0_0_3.entity.Windows import Windows


class Data:
    # 当前窗口线程信息
    window_process_info: list[WindowObj] = []

    # 当前窗口信息
    def get_window_process_info(self):
        self.window_process_info = Windows.exclude()
        return self.window_process_info

    # 当前选中的窗口
    select_window: WindowObj = None

    # 函数
    def set_select_window_obj(self, window_obj: WindowObj):
        self.select_window = window_obj
        return

    pass


g_data = Data()
