from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtGui import QKeyEvent
from PyQt5.QtWidgets import QLineEdit, QPushButton

from lw0_0_3.config.Config import g_config
from lw0_0_3.data.Data import g_data
from lw0_0_3.data.Obj import g_obj
from lw0_0_3.interface.window import Ui_window_root


class Size:
    ui: Ui_window_root = None

    def __init__(self, ui: Ui_window_root):
        self.ui = ui
        self.init_size()
        self.init_default_size()
        self.init_size_max_min()

        return

    def init_size(self):
        def change(input_obj: QLineEdit):
            text = input_obj.text()
            obj = input_obj
            if text == '':
                return
            if text.isdigit():
                return
            text = text[-1]
            print(input_obj.text())
            if text == 'a':
                obj.setText(obj.text()[:-1])
                g_obj.event_key.keyPressEvent(QKeyEvent(
                    QKeyEvent.KeyPress,
                    Qt.Key_A,
                    Qt.NoModifier,
                    text='a'
                ))
            elif text == 'd':
                obj.setText(obj.text()[:-1])
                g_obj.event_key.keyPressEvent(QKeyEvent(
                    QKeyEvent.KeyPress,
                    Qt.Key_D,
                    Qt.NoModifier,
                    text='d'
                ))
            elif text == '-' and len(input_obj.text()) == 1:
                return
            else:
                obj.setText(obj.text()[:-1])

        def enter(model: str, input_obj: QLineEdit):
            window = g_data.select_window
            if window is None:
                print("请先选择窗口")
                return
            is_center = g_config.data['tab2']['set_size_center']
            if model == 'width':
                window.set_window_size(int(input_obj.text()), window.size[1], center=is_center, activate=False).update()
                g_config.data['tab2']['width'] = int(input_obj.text())
                g_config.update()
            elif model == 'height':
                window.set_window_size(window.size[0], int(input_obj.text()), center=is_center, activate=False).update()
                g_config.data['tab2']['height'] = int(input_obj.text())
                g_config.update()
            return

        self.ui.input_width.textChanged.connect(lambda: change(self.ui.input_width))
        self.ui.input_width.returnPressed.connect(lambda: enter("width", self.ui.input_width))
        self.ui.input_height.textChanged.connect(lambda: change(self.ui.input_height))
        self.ui.input_height.returnPressed.connect(lambda: enter("height", self.ui.input_height))

        def fn_center():
            is_center = self.ui.width_height_center.isChecked()
            g_config.data['tab2']['set_size_center'] = is_center
            g_config.update()
            return

        is_center = g_config.data['tab2']['set_size_center']
        self.ui.width_height_center.setChecked(is_center)
        self.ui.width_height_center.stateChanged.connect(fn_center)

        # 赋值
        self.ui.input_width.setText(str(g_config.data['tab2']['width']))
        self.ui.input_height.setText(str(g_config.data['tab2']['height']))

        return

    def init_default_size(self):
        def fn(size: str):
            width, height = size.split('x')
            width = int(width)
            height = int(height)
            if g_data.select_window is None:
                print("请先选择窗口")
                return
            is_center = g_config.data['tab2']['set_default_size_center']
            g_data.select_window.set_window_size(width, height, center=is_center, activate=False).update()
            return

        self.ui.button_size_max.clicked.connect(lambda: fn('1938x1098'))
        self.ui.button_size_screen.clicked.connect(lambda: fn('1920x1080'))
        self.ui.button_size_jetbrains.clicked.connect(lambda: fn('1750x1030'))
        self.ui.button_size_chatglm.clicked.connect(lambda: fn('1663x938'))
        self.ui.button_size_default.clicked.connect(lambda: fn('1550x980'))
        self.ui.button_size_dingding.clicked.connect(lambda: fn('1410x809'))
        self.ui.button_size_cloudmusic.clicked.connect(lambda: fn('1321x940'))
        self.ui.button_size_explorer.clicked.connect(lambda: fn('1313x750'))
        self.ui.button_size_cmd.clicked.connect(lambda: fn('1259x770'))
        self.ui.button_size_wechat.clicked.connect(lambda: fn('1080x800'))
        self.ui.button_size_find.clicked.connect(lambda: fn('960x600'))

        def fn_center():
            is_center = self.ui.default_size_center.isChecked()
            g_config.data['tab2']['set_default_size_center'] = is_center
            g_config.update()
            return

        is_center = g_config.data['tab2']['set_default_size_center']
        self.ui.default_size_center.setChecked(is_center)
        self.ui.default_size_center.stateChanged.connect(fn_center)
        return

    def init_size_max_min(self):
        def fn(model: str):
            window = g_data.select_window
            if window is None:
                print("请先选择窗口")
                return
            num = g_config.data['tab2']['big_small_px']
            is_center = g_config.data['tab2']['big_small_center']
            if model == 'big':
                window.set_window_proportional_scaling(num, center=is_center, activate=False).update()
            elif model == 'small':
                window.set_window_proportional_scaling(-num, center=is_center, activate=False).update()
            return

        self.ui.button_big.clicked.connect(lambda: fn("big"))
        self.ui.button_small.clicked.connect(lambda: fn("small"))

        def fn_center():
            is_center = self.ui.max_min_center.isChecked()
            g_config.data['tab2']['big_small_center'] = is_center
            g_config.update()
            return

        is_center = g_config.data['tab2']['big_small_center']
        self.ui.max_min_center.setChecked(is_center)
        self.ui.max_min_center.stateChanged.connect(fn_center)

        def change(input_obj: QLineEdit):
            text = input_obj.text()
            obj = input_obj
            if text == '':
                return
            if text.isdigit():
                g_config.data['tab2']['big_small_px'] = int(input_obj.text())
                g_config.update()
                return
            text = text[-1]
            if text == 'a':
                obj.setText(obj.text()[:-1])
                g_obj.event_key.keyPressEvent(QKeyEvent(
                    QKeyEvent.KeyPress,
                    Qt.Key_A,
                    Qt.NoModifier,
                    text='a'
                ))
            elif text == 'd':
                obj.setText(obj.text()[:-1])
                g_obj.event_key.keyPressEvent(QKeyEvent(
                    QKeyEvent.KeyPress,
                    Qt.Key_D,
                    Qt.NoModifier,
                    text='d'
                ))
            else:
                obj.setText(obj.text()[:-1])
            return

        self.ui.input_big_small_px.setText(str(g_config.data['tab2']['big_small_px']))
        self.ui.input_big_small_px.textChanged.connect(lambda: change(self.ui.input_big_small_px))

        return

    pass
