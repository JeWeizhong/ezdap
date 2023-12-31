import sys
import pandas as pd

from PySide6.QtWidgets import *
from PySide6.QtCore import QAbstractTableModel, Qt, QModelIndex, QSize, QRect
from PySide6.QtGui import QAction, QIcon, QKeySequence, QGuiApplication

from modules.dataframe_model import PandasModel
from modules.mpl_plot import PlotWidget
# from modules.form_widget import FormWidget, FormDialog
# from modules.menu_module import MainMenu, FileSlot, PlotSlot
from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT
# from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar


class AppMainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("EZDAP")
        # self.resize(800, 500)

        self.create_menu()
        # self.file_menu = FileSlot(self)
        # self.plot_menu = PlotSlot(self)
        # self.table_widget = QTableWidget()
        # self.setCentralWidget(self.table_widget)

        self.main = QWidget(self)
        self.tabs = QTabWidget(self.main)
        layout = QHBoxLayout(self.main)
        layout.addWidget(self.tabs)
        screen_resolution = QGuiApplication.primaryScreen().availableGeometry()
        width, height = int(screen_resolution.width()*0.7), int(screen_resolution.height()*.7)
        if screen_resolution.width()>1024:
            self.setGeometry(QRect(200, 200, width, height))
        self.setMinimumSize(400,300)
        self.setLayout(layout)
        self.main.setFocus()
        self.setCentralWidget(self.main)

    def create_table_widget(self, data_frame=None):
        view = QTableView()
        view.horizontalHeader().setStretchLastSection(False)
        view.setAlternatingRowColors(True)
        view.setSelectionBehavior(QTableView.SelectRows)
        # df = pd.read_csv(data_frame)
        self.data_model = PandasModel(data_frame)
        view.setModel(self.data_model)
        self.splitter = QSplitter(Qt.Horizontal)
        self.splitter.addWidget(view)
        layout = QFormLayout()
        grid_group_box = QGroupBox("Plot")
        grid_group_box.setLayout(layout)
        self.right_form = grid_group_box
        self.splitter.addWidget(self.right_form)
        self.splitter.setSizes((500,200))
        # self.current_table = None
        self.tabs.removeTab(0)
        self.tabs.insertTab(0, self.splitter, "demo")
        self.setCentralWidget(self.tabs)


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
        menubar = QMenuBar(self)
        file_menu = menubar.addMenu("文件")

        new_action = QAction("新建", menubar)
        # 打开一个空表格
        new_action.triggered.connect(self.new_document)
        file_menu.addAction(new_action)

        open_action = QAction("打开", menubar)
        # 打开一个表格文件
        open_action.triggered.connect(self.open_document)
        file_menu.addAction(open_action)

        save_action = QAction("保存", menubar)
        # todo
        # save_action.triggered.connect(self.save_document)
        file_menu.addAction(save_action)

        exit_action = QAction("退出", menubar)
        # 退出程序
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        edit_menu = menubar.addMenu("编辑")
        edit_menu.addAction(QAction("剪切", menubar))

        stat_menu = menubar.addMenu("统计")
        t_test = QAction("T检验", menubar)
        stat_menu.addAction(t_test)

        # plot_action = PlotAction(self)
        plot_menu = menubar.addMenu("可视化")
        scatter_action = QAction("散点图", menubar)
        scatter_action.triggered.connect(self.create_plot_dialog)
        plot_menu.addAction(scatter_action)
        
        help_menu = menubar.addMenu("帮助")

        self.setMenuBar(menubar)

    # def create_plot_dock(self):
    #     # 检查 current_table 是否存在
    #     if not hasattr(self, "data_model"):
    #         print("请先打开一个表格")
    #         return
    #     # form = FormWidget(data_frame=self.data_model._dataframe, app_name='scatter')
    #     # self.splitter.removeWidget(self.right_form)
    #     grid_group_box = QGroupBox("Grid layout")
    #     self.right_form = grid_group_box
    #     self.splitter.replaceWidget(1, self.right_form)
    #     return

    def create_plot_dialog(self):
        
        dialog = QDialog()
        dialog.setWindowTitle("散点图")
        dialog.setMinimumWidth(250)
        dialog.setWindowModality(Qt.WindowModal)
        layout = QFormLayout()
        xaixs = QComboBox()
        xaixs.addItems(self.data_model._dataframe.columns.tolist())

        layout.addRow(QLabel("x 轴"), xaixs)
        yaixs = QComboBox()
        yaixs.addItems(self.data_model._dataframe.columns.tolist())
        layout.addRow(QLabel("y 轴"), yaixs)

        h_layout = QHBoxLayout() 
        submit_button = QPushButton("开始运行", dialog)
        submit_button.clicked.connect(self.mpl_plot_scatter)
        reset_button = QPushButton("Reset")
        h_layout.addWidget(submit_button)
        h_layout.addWidget(reset_button)
        
        layout.addRow(h_layout)
        dialog.setLayout(layout)
        
        if dialog.exec() == QDialog.Accepted:
            print(f"执行成功")

    def new_document(self):
        """
        新建一个表格在左边，右边显示可视化界面
        """
        self.create_table_widget(None)


    
    def open_document(self):
        print("Open document called")
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_name, _ = QFileDialog.getOpenFileName(None, "打开表格文件", "", "表格文件 (*.csv *.xlsx);;所有文件 (*)", options=options)
        if file_name:
            try:
                # 读取表格文件并加载到QTableWidget中
                df = pd.read_csv(file_name)  # 也可以使用 pd.read_excel() 处理.xlsx文件
                self.create_table_widget(df)
            except pd.errors.ParserError:
                print("无法打开此文件")

    def close(self) -> bool:
        return super().close()
    
    def mpl_plot_scatter(self):
        print("开始绘制散点图")
        dockWidget = QDockWidget("可关闭/右侧栏", self)
        # layout = QVBoxLayout()
        # view = FigureCanvas(Figure(figsize=(5, 3)))
        # axes = view.figure.subplots()
        # axes.plot([0,1,2,3,4], [10,1,20,3,40])
        # toolbar = NavigationToolbar2QT(view)
        # layout.addWidget(toolbar)
        # layout.addWidget(view)
        listWidget = QListWidget()
        listWidget.addItem(f"dock1-item1")
        listWidget.addItem(f"dock2-item2")
        listWidget.addItem(f"dock3-item3")
        dockWidget.setWidget(listWidget)
        dockWidget.setFeatures(QDockWidget.DockWidgetClosable | QDockWidget.DockWidgetMovable)

        self.addDockWidget(Qt.RightDockWidgetArea, dockWidget)
        # view.draw()

if __name__ == "__main__":

    app = QApplication(sys.argv)
    window = AppMainWindow()
    window.show()
    app.exec()