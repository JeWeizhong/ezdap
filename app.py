import sys
import pandas as pd

from PySide6.QtWidgets import *
from PySide6.QtCore import QAbstractTableModel, Qt, QModelIndex, QSize
from PySide6.QtGui import QAction, QIcon, QKeySequence

from modules.dataframe_model import PandasModel
from modules.mpl_plot import PlotWidget
from modules.visualization import PlotAction

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure


class AppMainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Pandas Model")
        self.resize(800, 500)

        self.create_menu()
        # 创建一个空的表格
        self.table_widget = QTableWidget()
        self.setCentralWidget(self.table_widget)
        # self.create_tool_bar()
        # self.setStatusBar(QStatusBar(self))

    def create_table_widget(self, data_frame):
        view = QTableView()
        view.horizontalHeader().setStretchLastSection(True)
        view.setAlternatingRowColors(True)
        view.setSelectionBehavior(QTableView.SelectRows)
        # df = pd.read_csv(data_frame)
        model = PandasModel(data_frame)
        view.setModel(model)
        self.current_table = data_frame
        self.tabWidget = QTabWidget(self)
        self.tabWidget.addTab(view, "iris.csv")
        self.setCentralWidget(self.tabWidget)


    def create_tool_bar(self):

        toolbar = QToolBar("My main toolbar")
        toolbar.setIconSize(QSize(16, 16))

        button_action = QAction("&button", self)
        button_action.setStatusTip("This is your button")
        button_action.triggered.connect(self.onMyToolBarButtonClick)
        button_action.setCheckable(True)
        toolbar.addAction(button_action)

        toolbar.addSeparator()

        button_action2 = QAction("&button2", self)
        button_action2.setStatusTip("This is your button2")
        button_action2.triggered.connect(self.onMyToolBarButtonClick)
        button_action2.setCheckable(True)
        toolbar.addAction(button_action2)

        self.addToolBar(toolbar)

    def create_menu(self):
        menubar = self.menuBar()
        file_menu = menubar.addMenu("文件")

        new_action = QAction("新建", self)
        # new_action.triggered.connect(self.new_document)
        file_menu.addAction(new_action)

        open_action = QAction("打开", self)
        open_action.triggered.connect(self.open_document)
        file_menu.addAction(open_action)

        save_action = QAction("保存", self)
        save_action.triggered.connect(self.save_document)
        file_menu.addAction(save_action)

        exit_action = QAction("退出", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        edit_menu = menubar.addMenu("编辑")
        edit_menu.addAction(QAction("剪切", self))

        stat_menu = menubar.addMenu("统计")
        t_test = QAction("T检验", self)
        stat_menu.addAction(t_test)

        plot_action = PlotAction(self)
        plot_menu = menubar.addMenu("可视化")
        scatter_action = QAction("散点图", self)
        scatter_action.triggered.connect(plot_action.create_scatter_dock)
        plot_menu.addAction(scatter_action)
        
        help_menu = menubar.addMenu("帮助")


    def onMyToolBarButtonClick(self, s):
        print("click", s)


    def new_document(self):
        self.table_widget.clear()

    def open_document(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_name, _ = QFileDialog.getOpenFileName(self, "打开表格文件", "", "表格文件 (*.csv *.xlsx);;所有文件 (*)", options=options)
        if file_name:
            try:
                # 读取表格文件并加载到QTableWidget中
                df = pd.read_csv(file_name)  # 也可以使用 pd.read_excel() 处理.xlsx文件
                self.create_table_widget(df)
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

if __name__ == "__main__":

    app = QApplication(sys.argv)
    window = AppMainWindow()
    window.show()
    app.exec()