'''
可视化菜单
'''

from PySide6.QtWidgets import QMenu, QToolBar, QWidget, QDockWidget, QComboBox, QFormLayout, QGroupBox, QLabel
from PySide6.QtCore import QAbstractTableModel, Qt, QModelIndex, QSize
from PySide6.QtGui import QAction, QIcon, QKeySequence

class PlotAction(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        # self.scatter_action = QAction("散点图", self)
        # self.scatter_action.triggered.connect(self.create_scatter_dock)

    def create_scatter_dock(self):
        dockWidget = QDockWidget("可关闭/右侧栏", self)
        grid_group_box = QGroupBox("Grid layout")
        layout = QFormLayout()
        # xaixs 是 下拉选项卡，内容是 self.current_table 中的列名
        xaixs = QComboBox()
        xaixs.addItems(self.parent.current_table.columns.tolist())

        layout.addRow(QLabel("x 轴"), xaixs)
        # yaixs 是 下拉选项卡，内容是 self.current_table 中的列名
        yaixs = QComboBox()
        yaixs.addItems(self.parent.current_table.columns.tolist())
        layout.addRow(QLabel("y 轴"), yaixs)
        grid_group_box.setLayout(layout)
        dockWidget.setWidget(grid_group_box)

        self.parent.addDockWidget(Qt.RightDockWidgetArea, dockWidget)
        dockWidget.setFeatures(QDockWidget.DockWidgetClosable)