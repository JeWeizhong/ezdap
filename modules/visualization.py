'''
可视化菜单
'''

from PySide6.QtWidgets import QMenu, QToolBar, QWidget, QDockWidget, QComboBox, QFormLayout, QGroupBox, QLabel
from PySide6.QtCore import QAbstractTableModel, Qt, QModelIndex, QSize
from PySide6.QtGui import QAction, QIcon, QKeySequence

class PlotDockWidget(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
    
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