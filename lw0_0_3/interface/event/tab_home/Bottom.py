from lw0_0_3.entity.WindowObj import WindowObj
from lw0_0_3.interface.window import Ui_window_root


class Bottom:
    ui: Ui_window_root

    def __init__(self, ui: Ui_window_root):
        self.ui = ui
        self.text_window_title = self.ui.text_window_title
        self.text_size = self.ui.text_size
        self.text_xy = self.ui.text_xy
        self.text_pid = self.ui.text_pid
        self.text_tid = self.ui.text_tid
        self.text_process_path = self.ui.text_process_path
        self.text_status = self.ui.text_status
        self.text_opacity = self.ui.text_opacity
        self.clear()
        return

    def clear(self):
        self.text_window_title.setText("")
        self.text_size.setText("")
        self.text_xy.setText("")
        self.text_pid.setText("")
        self.text_tid.setText("")
        self.text_process_path.setText("")
        self.text_status.setText("")
        self.text_opacity.setText("")
        return

    def update(self, select_window: WindowObj):
        # 标题窗口
        self.text_window_title.setText(select_window.title)
        # 窗口大小
        self.text_size.setText(f"{select_window.size[0]}x{select_window.size[1]}")
        # 窗口位置
        self.text_xy.setText(f"{select_window.xy[0]}x{select_window.xy[1]}")
        # 进程号
        self.text_pid.setText(f"{select_window.pid}")
        # 线程号
        self.text_tid.setText(f"{select_window.tid}")
        # 进程启动路径
        self.text_process_path.setText(select_window.process_path)
        # 窗口状态
        self.text_status.setText(select_window.status)
        # 透明度
        self.text_opacity.setText(f"{select_window.opacity if select_window.opacity is not None else ''}")
        return

    pass
