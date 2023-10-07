import pandas as pd

from PySide6.QtWidgets import QTableView, QApplication, QMainWindow, QDockWidget, QListWidget, QLabel, QTextEdit, QHBoxLayout, QTabWidget, \
                            QWidget, QMenu, QMenuBar, QToolBar, QCheckBox, QStatusBar
from PySide6.QtCore import QAbstractTableModel, Qt, QModelIndex, QSize
from PySide6.QtGui import QAction, QIcon, QKeySequence
import sys
from modules.dataframe_model import PandasModel

class AppMainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Pandas Model")
        self.resize(800, 500)
        toolbar = QToolBar("My main toolbar")
        toolbar.setIconSize(QSize(16, 16))
        self.addToolBar(toolbar)

        button_action = QAction("&Your button", self)
        button_action.setStatusTip("This is your button")
        button_action.triggered.connect(self.onMyToolBarButtonClick)
        button_action.setCheckable(True)
        toolbar.addAction(button_action)

        toolbar.addSeparator()

        button_action2 = QAction("Your &button2", self)
        button_action2.setStatusTip("This is your button2")
        button_action2.triggered.connect(self.onMyToolBarButtonClick)
        button_action2.setCheckable(True)
        toolbar.addAction(button_action2)

        toolbar.addWidget(QLabel("Hello"))
        toolbar.addWidget(QCheckBox())

        self.setStatusBar(QStatusBar(self))

        view = QTableView()
        view.horizontalHeader().setStretchLastSection(True)
        view.setAlternatingRowColors(True)
        view.setSelectionBehavior(QTableView.SelectRows)
        df = pd.read_csv("iris.csv")
        model = PandasModel(df)
        view.setModel(model)

        self.tabWidget = QTabWidget(self)
        self.tabWidget.addTab(view, "iris.csv")
        self.setCentralWidget(self.tabWidget)
        self.createDockWidget()

    def create_menu(self):
        self._menu_bar = QMenuBar()

        self._file_menu = QMenu("&File", self)
        self._file_menu.addAction("E&xit")
        self._menu_bar.addMenu(self._file_menu)

    def createDockWidget(self):
        dockWidget = QDockWidget("可关闭/右侧栏", self)
        listWidget = QListWidget()
        listWidget.addItem(f"dock1-item1")
        listWidget.addItem(f"dock2-item2")
        listWidget.addItem(f"dock3-item3")
        dockWidget.setWidget(listWidget)
        self.addDockWidget(Qt.RightDockWidgetArea, dockWidget)
        dockWidget.setFeatures(QDockWidget.DockWidgetClosable)

    def onMyToolBarButtonClick(self, s):
        print("click", s)

if __name__ == "__main__":

    app = QApplication(sys.argv)
    window = AppMainWindow()
    window.show()
    app.exec()