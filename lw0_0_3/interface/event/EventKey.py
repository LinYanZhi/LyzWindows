from PyQt5.QtGui import QMouseEvent, QKeyEvent
from PyQt5.QtWidgets import QMainWindow


# 全局按键事件
class EventKey:
    main_window: QMainWindow = None
    tab_widget: QMainWindow = None
    default_event: QMainWindow.keyPressEvent = None

    def keyPressEvent(self, event: QKeyEvent):
        count = self.tab_widget.count()
        current_index = self.tab_widget.currentIndex()
        if event.text() == 'a':
            self.tab_widget.setCurrentIndex(max(current_index - 1, 0))
        elif event.text() == 'd':
            self.tab_widget.setCurrentIndex(min(current_index + 1, count - 1))
        else:
            self.default_event(event)

    def __init__(self, main_window: QMainWindow, tab_widget: QMainWindow):
        self.main_window = main_window
        self.tab_widget = tab_widget
        self.default_event = self.main_window.keyPressEvent
        self.main_window.keyPressEvent = self.keyPressEvent

    pass
