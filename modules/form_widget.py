'''
可视化菜单
'''

from PySide6.QtWidgets import QMenu, QToolBar, QWidget, QDockWidget, QComboBox, QFormLayout, QGroupBox, QLabel, QPushButton, QHBoxLayout, QDialog, QVBoxLayout, QLineEdit
from PySide6.QtCore import QAbstractTableModel, Qt, QModelIndex, QSize
from PySide6.QtGui import QAction, QIcon, QKeySequence

class FormWidget(QWidget):

    def __init__(self, title="Grid layout", data_frame=None, app_name=None):
        super().__init__()
        self.title = title
        self.data_frame = data_frame
        self.layout = QFormLayout()
        self.grid_group_box = QGroupBox(self.title)
        self.grid_group_box.setLayout(self.layout)
        self.app_name = app_name
        if self.app_name == 'scatter':
            self.grid_group_box = self.create_scatter(self.data_frame)
    
    def create_scatter(self, data_frame):
        submit_button = QPushButton()
        submit_button.setText("对话框5-模式窗口2(exec)")
        # layout.addWidget(self.submit_button)
        submit_button.clicked.connect(self.showdialog_model2)
        grid_group_box = QGroupBox("Grid layout")
        layout = QFormLayout()
        xaixs = QComboBox()
        xaixs.addItems(data_frame.columns.tolist())

        layout.addRow(QLabel("x 轴"), xaixs)
        yaixs = QComboBox()
        yaixs.addItems(data_frame.columns.tolist())
        layout.addRow(QLabel("y 轴"), yaixs)
        # 提交按钮, 重置按钮
        # 水平布局
        h_layout = QHBoxLayout() 
        # submit_button = QPushButton("Submit")
        reset_button = QPushButton("Reset")
        h_layout.addWidget(submit_button)
        h_layout.addWidget(reset_button)
        layout.addRow(h_layout)
        grid_group_box.setLayout(layout)

        return grid_group_box
    
    
    def showdialog_model2(self):
        dialog = QDialog(self)
        button = QPushButton("OK", dialog)
        button.clicked.connect(dialog.accept)
        dialog.setWindowTitle("Dialog 案例-模式窗口2(exec)")
        dialog.setMinimumWidth(250)
        dialog.setWindowModality(Qt.WindowModal)
        self.label.setText('修改默认模式：“%s” \n 我有父类，我能影响父窗口，不能影响兄弟窗口' % dialog.windowTitle())
        dialog.exec()

class FormDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("表单对话框")

        layout = QVBoxLayout()

        label = QLabel("请输入一些文本:")
        self.text_field = QLineEdit()
        ok_button = QPushButton("确定")

        layout.addWidget(label)
        layout.addWidget(self.text_field)
        layout.addWidget(ok_button)

        ok_button.clicked.connect(self.accept)

        self.setLayout(layout)