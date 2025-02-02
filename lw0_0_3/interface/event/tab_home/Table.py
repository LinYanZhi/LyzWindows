from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtGui import QKeyEvent, QMouseEvent
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QAbstractItemView

from lw0_0_3.config.NickName import g_nickname
from lw0_0_3.data.Data import g_data
from lw0_0_3.data.Obj import g_obj
from lw0_0_3.entity.WindowObj import WindowObj
from lw0_0_3.interface.event.EventKey import EventKey
from lw0_0_3.interface.event.tab_home.Bottom import Bottom
from lw0_0_3.interface.window import Ui_window_root


class Table:
    obj: QTableWidget = None
    ui: Ui_window_root = None
    event_key: EventKey = None
    default_mouse_event: QTableWidget.mousePressEvent = None
    default_key_event: QTableWidget.keyPressEvent = None

    def __init__(self, ui: Ui_window_root, event_key: EventKey):
        self.obj = ui.table_info_data
        self.ui = ui
        self.event_key = event_key

        # 初始化表格内容
        self.__init_data()
        # 设置表格内容不可修改
        self.__cannot_update()
        # 设置表格整行选中 只能选中一行
        self.__select_row()
        # 设置表格行的样式
        self.__set_style()
        # 绑定事件
        self.__bind_selected_row_event()
        self.__bind_key_event()
        self.__bind_mouse_event()

        return

    # 初始化表格内容
    def __init_data(self):
        table: QTableWidget = self.obj
        # 清空原先内容
        columns = ['title', 'nickname']
        windows: list[WindowObj] = g_data.get_window_process_info()
        # 清空数据
        table.clearContents()
        # 初始化表格数据
        table.setColumnCount(len(columns))
        table.setHorizontalHeaderLabels(columns)
        table.setRowCount(len(windows))
        # 设置表格内容
        for i, window in enumerate(windows):
            nickname = g_nickname.data.get(window.process_path, '')
            table.setItem(i, 1, QTableWidgetItem(window.title))
            table.setItem(i, 0, QTableWidgetItem(f" {nickname} "))
        return

    # 设置表格内容不可修改
    def __cannot_update(self):
        table: QTableWidget = self.obj
        for row in range(table.rowCount()):
            for column in range(table.columnCount()):
                item = table.item(row, column)
                if item is not None:
                    item.setFlags(item.flags() & ~Qt.ItemIsEditable)
        return

    # 设置表格整行选中 只能选中一行
    def __select_row(self):
        table: QTableWidget = self.obj
        # 设置表格内容选中方式为整行选中
        table.setSelectionBehavior(QAbstractItemView.SelectRows)
        # 设置表格只能选中一行
        table.setSelectionMode(QAbstractItemView.SingleSelection)
        return

    # 设置表格行的样式
    def __set_style(self):
        table: QTableWidget = self.obj
        # 将行和列的高度、宽度设置为与所显示内容的宽度、高度相匹配
        table.resizeRowsToContents()
        table.resizeColumnsToContents()
        # 设置列宽度和行高度
        row_count = table.rowCount()
        for row in range(row_count):
            # 设置行高度为15
            table.setRowHeight(row, 9)
            table.setColumnWidth(0, 200)
            table.setColumnWidth(1, 400)
            # 设置字体大小为13px
            font = table.font()
            font.setPointSize(11)
        return

    # 行选中事件
    def __bind_selected_row_event(self):
        table: QTableWidget = self.obj

        # 行选中事件
        def click_row(row, column):
            g_data.select_window = g_data.window_process_info[row]
            select_window: WindowObj = g_data.select_window
            # 赋值
            self.bottom = Bottom(self.ui)
            self.bottom.update(select_window)
            return

        # 绑定点击事件，获取点击行的内容
        table.cellClicked.connect(click_row)

        return

    # 鼠标点击事件
    def __bind_mouse_event(self):
        table: QTableWidget = self.obj
        if self.default_mouse_event is None:
            self.default_mouse_event = table.mousePressEvent

        # 鼠标事件
        def mouse_event(event: QMouseEvent):
            # 右键
            if event.button() == Qt.RightButton:
                g_data.select_window = None
                Bottom(self.ui)
                self.__init__(self.ui, self.event_key)
            else:
                self.default_mouse_event(event)
            return

        g_obj.mouse_right_click_event = mouse_event

        table.mousePressEvent = mouse_event
        return

    # 按键点击事件
    def __bind_key_event(self):
        table: QTableWidget = self.obj
        if self.default_key_event is None:
            self.default_key_event = table.keyPressEvent

        # 按键事件
        def key_event(event: QKeyEvent):

            key_text = key_map.get(event.key(), None)
            if key_text == "w":
                self.default_key_event(QKeyEvent(
                    QEvent.KeyPress,
                    Qt.Key_Up,
                    Qt.NoModifier
                ))
            elif key_text == "s":
                self.default_key_event(QKeyEvent(
                    QEvent.KeyPress,
                    Qt.Key_Down,
                    Qt.NoModifier
                ))
            else:
                self.event_key.keyPressEvent(event)
            # 遍历表格 判断哪些数据被选中了
            select_row_index = None
            for row in range(table.rowCount()):
                if table.item(row, 0).isSelected():
                    select_row_index = row
                    break
            if select_row_index is None:
                return
            select_window: WindowObj = g_data.window_process_info[select_row_index]
            g_data.select_window = select_window
            self.bottom = Bottom(self.ui)
            self.bottom.update(select_window)
            return

        table.keyPressEvent = key_event
        return

    pass


key_map = {
    87: 'w',
    83: 's',
    65: 'a',
    68: 'd'
}
