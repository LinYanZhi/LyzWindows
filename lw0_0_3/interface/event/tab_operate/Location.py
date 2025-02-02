import pyautogui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeyEvent
from PyQt5.QtWidgets import QLineEdit

from lw0_0_3.config.Config import g_config
from lw0_0_3.data.Data import g_data
from lw0_0_3.data.Obj import g_obj
from lw0_0_3.entity.WindowObj import WindowObj
from lw0_0_3.interface.window import Ui_window_root


class Location:
    ui: Ui_window_root = None

    def __init__(self, ui: Ui_window_root):
        self.ui = ui
        self.init_location()
        return

    def init_location(self):
        input_left = self.ui.input_left
        input_up = self.ui.input_up
        input_right = self.ui.input_right
        input_down = self.ui.input_down

        def enter(model: str, input: QLineEdit):
            try:
                input = int(input.text())
            except:
                print("请输入整数")
                return
            if g_data.select_window is None:
                print("请先选择窗口")
                return
            window: WindowObj = g_data.select_window
            if model == "left":
                window.set_window_position(input, window.xy[1], False).update()
                g_config.data['tab2']['left'] = input
                g_config.update()
            elif model == "up":
                window.set_window_position(window.xy[0], input, False).update()
                g_config.data['tab2']['up'] = input
                g_config.update()
            elif model == "right":
                window.set_window_position(pyautogui.size()[0] - window.size[0] - input, window.xy[1], False).update()
                g_config.data['tab2']['right'] = input
                g_config.update()
            elif model == "down":
                window.set_window_position(window.xy[0], pyautogui.size()[1] - window.size[1] - input, False).update()
                g_config.data['tab2']['down'] = input
                g_config.update()
            return

        input_left.returnPressed.connect(lambda: enter('left', input_left))
        input_up.returnPressed.connect(lambda: enter('up', input_up))
        input_right.returnPressed.connect(lambda: enter('right', input_right))
        input_down.returnPressed.connect(lambda: enter('down', input_down))

        def change(obj: QLineEdit):
            input_text = obj.text()
            if input_text == '':
                return
            input_text = input_text[-1]
            # 如果是int则退出
            if input_text.isdigit():
                return
            if input_text == 'a':
                obj.setText(obj.text()[:-1])
                g_obj.event_key.keyPressEvent(QKeyEvent(
                    QKeyEvent.KeyPress,
                    Qt.Key_A,
                    Qt.NoModifier,
                    text='a'
                ))
            elif input_text == 'd':
                obj.setText(obj.text()[:-1])
                g_obj.event_key.keyPressEvent(QKeyEvent(
                    QKeyEvent.KeyPress,
                    Qt.Key_D,
                    Qt.NoModifier,
                    text='d'
                ))
            elif input_text == '-' and len(obj.text()) == 1:
                return
            else:
                obj.setText(obj.text()[:-1])
            return

        input_left.textChanged.connect(lambda: change(input_left))
        input_up.textChanged.connect(lambda: change(input_up))
        input_right.textChanged.connect(lambda: change(input_right))
        input_down.textChanged.connect(lambda: change(input_down))

        # 赋值
        input_left.setText(str(g_config.data['tab2']['left']))
        input_up.setText(str(g_config.data['tab2']['up']))
        input_right.setText(str(g_config.data['tab2']['right']))
        input_down.setText(str(g_config.data['tab2']['down']))

        return

    pass
