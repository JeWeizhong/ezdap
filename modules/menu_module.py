# menu_module.py

from PySide6.QtWidgets import QMenuBar, QMenu, QFileDialog, QTableWidget, QTableWidgetItem, QWidget, QDockWidget
from PySide6.QtGui import QAction
from PySide6.QtCore import Qt
from PySide6.QtCore import Slot

import pandas as pd

from .form_widget import PlotDockWidget


class MainMenu():
    def __init__(self, main_window):
        self.main_window = main_window
        self.menu_bar = self.create_menu_bar()

    def create_menu_bar(self):
        menubar = QMenuBar()
        file_menu = menubar.addMenu("文件")

        new_action = QAction("新建", menubar)
        # new_action.triggered.connect(self.new_document)
        file_menu.addAction(new_action)

        open_action = QAction("打开", menubar)
        open_action.triggered.connect(self.main_window.open_document)
        file_menu.addAction(open_action)

        save_action = QAction("保存", menubar)
        # save_action.triggered.connect(self.save_document)
        file_menu.addAction(save_action)

        exit_action = QAction("退出", menubar)
        # exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        edit_menu = menubar.addMenu("编辑")
        edit_menu.addAction(QAction("剪切", menubar))

        stat_menu = menubar.addMenu("统计")
        t_test = QAction("T检验", menubar)
        stat_menu.addAction(t_test)

        # plot_action = PlotAction(self)
        plot_menu = menubar.addMenu("可视化")
        scatter_action = QAction("散点图", menubar)
        scatter_action.triggered.connect(self.main_window.create_scatter_dock)
        plot_menu.addAction(scatter_action)
        
        help_menu = menubar.addMenu("帮助")
        return menubar


class FileSlot:

    def __init__(self, main_window) -> None:
        self.main_window = main_window  # 存储传递的 AppMainWindow 实例

    def new_document(self):
        self.table_widget.clear()

    def open_document(self):
        print("Open document called")
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_name, _ = QFileDialog.getOpenFileName(None, "打开表格文件", "", "表格文件 (*.csv *.xlsx);;所有文件 (*)", options=options)
        if file_name:
            try:
                # 读取表格文件并加载到QTableWidget中
                df = pd.read_csv(file_name)  # 也可以使用 pd.read_excel() 处理.xlsx文件
                self.main_window.create_table_widget(df)
            except pd.errors.ParserError:
                print("无法打开此文件")

    def save_document(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, "保存文件", "", "文本文件 (*.txt);;所有文件 (*)", options=options)
        if file_name:
            with open(file_name, "w") as file:
                file.write(self.table_to_csv())

    def load_table_data(self, data_frame):
        self.table_widget.setRowCount(data_frame.shape[0])
        self.table_widget.setColumnCount(data_frame.shape[1])

        # 设置表头
        self.table_widget.setHorizontalHeaderLabels(data_frame.columns.tolist())

        for row in range(data_frame.shape[0]):
            for col in range(data_frame.shape[1]):
                item = QTableWidgetItem(str(data_frame.iat[row, col]))
                self.table_widget.setItem(row, col, item)

    def table_to_csv(self):
        num_rows = self.table_widget.rowCount()
        num_cols = self.table_widget.columnCount()
        csv_data = []

        # 获取列名
        column_names = [self.table_widget.horizontalHeaderItem(col).text() for col in range(num_cols)]
        csv_data.append(",".join(column_names))

        for row in range(num_rows):
            row_data = []
            for col in range(num_cols):
                item = self.table_widget.item(row, col)
                if item:
                    row_data.append(item.text())
                else:
                    row_data.append("")
            csv_data.append(",".join(row_data))

        return "\n".join(csv_data)
    

class PlotSlot:

    def __init__(self, main_window) -> None:
        self.main_window = main_window  # 存储传递的 AppMainWindow 实例


    def create_scatter_dock(self):
        print("scatter called")
        # 检查 current_table 是否存在
        if not hasattr(self.main_window, "current_table"):
            print("current_table not found")
            return
        dockWidget = QDockWidget("可关闭/右侧栏", self.main_window)
        grid_group_box = PlotDockWidget().create_scatter(self.main_window.current_table)
        dockWidget.setWidget(grid_group_box)

        self.main_window.addDockWidget(Qt.RightDockWidgetArea, dockWidget)
        dockWidget.setFeatures(QDockWidget.DockWidgetClosable)