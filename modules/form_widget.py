'''
可视化菜单
'''

from PySide6.QtWidgets import QMenu, QToolBar, QWidget, QDockWidget, QComboBox, QFormLayout, QGroupBox, QLabel
from PySide6.QtCore import QAbstractTableModel, Qt, QModelIndex, QSize
from PySide6.QtGui import QAction, QIcon, QKeySequence

class FormWidget:

    def __init__(self, title="Grid layout", data_frame=None, app_name=None):
        self.title = title
        self.data_frame = data_frame
        self.layout = QFormLayout()
        self.grid_group_box = QGroupBox(self.title)
        self.grid_group_box.setLayout(self.layout)
        self.app_name = app_name
        if self.app_name == 'scatter':
            self.grid_group_box = self.create_scatter(self.data_frame)
    
    def create_scatter(self, data_frame):
        grid_group_box = QGroupBox("Grid layout")
        layout = QFormLayout()
        xaixs = QComboBox()
        xaixs.addItems(data_frame.columns.tolist())

        layout.addRow(QLabel("x 轴"), xaixs)
        yaixs = QComboBox()
        yaixs.addItems(data_frame.columns.tolist())
        layout.addRow(QLabel("y 轴"), yaixs)
        grid_group_box.setLayout(layout)

        return grid_group_box