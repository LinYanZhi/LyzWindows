from PyQt5 import QtWidgets

from lw0_0_3.interface.event.EventKey import EventKey


class Obj:
    main_window: QtWidgets.QMainWindow = None
    event_key: EventKey = None
    # 全局事件触发：右键
    mouse_right_click_event = None
    pass


g_obj = Obj()
