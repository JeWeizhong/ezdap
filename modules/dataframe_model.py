# Copyright (C) 2022 The Qt Company Ltd.
# SPDX-License-Identifier: LicenseRef-Qt-Commercial OR BSD-3-Clause

import pandas as pd

from PySide6.QtWidgets import QTableView, QApplication, QWidget, QSplitter, QGridLayout
from PySide6.QtCore import QAbstractTableModel, Qt, QModelIndex

import modules.uil as uil


class PandasModel(QAbstractTableModel):
    """A model to interface a Qt view with pandas dataframe """

    def __init__(self, dataframe: pd.DataFrame, parent=None):
        QAbstractTableModel.__init__(self, parent)
        if dataframe is None:
            self._dataframe = uil.getEmptyData()
        else:
            self._dataframe = dataframe

    def rowCount(self, parent=QModelIndex()) -> int:
        """ Override method from QAbstractTableModel

        Return row count of the pandas DataFrame
        """
        if parent == QModelIndex():
            return len(self._dataframe)

        return 0

    def columnCount(self, parent=QModelIndex()) -> int:
        """Override method from QAbstractTableModel

        Return column count of the pandas DataFrame
        """
        if parent == QModelIndex():
            return len(self._dataframe.columns)
        return 0

    def data(self, index: QModelIndex, role=Qt.ItemDataRole):
        """Override method from QAbstractTableModel

        Return data cell from the pandas DataFrame
        """
        i = index.row()
        j = index.column()

        if not index.isValid():
            return None

        if role == Qt.DisplayRole:
            value = self._dataframe.iloc[i, j]
            if pd.isnull(value):
                return ''
            return str(value)
        elif role == Qt.EditRole:
            return str(value)
        
        return None

    def headerData(
        self, section: int, orientation: Qt.Orientation, role: Qt.ItemDataRole
    ):
        """Override method from QAbstractTableModel

        Return dataframe index as vertical header data and columns as horizontal header data.
        """
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self._dataframe.columns[section])

            if orientation == Qt.Vertical:
                return str(self._dataframe.index[section])

        return None


class DataFrameWidget(QWidget):
    """Widget containing a tableview and toolbars"""
    def __init__(self, parent=None, dataframe=None, app=None):

        super().__init__()
        self.splitter = QSplitter(Qt.Vertical, self)
        l = self.layout = QGridLayout()
        l.setSpacing(2)
        l.addWidget(self.splitter,1,1)
        self.table = PandasModel(self, dataframe)
        self.splitter.addWidget(self.table)
        self.splitter.setSizes((500,200))
        # if toolbar == True:
        #     self.createToolbar()
        # if statusbar == True:
        #     self.statusBar()
        # self.pf = None
        # self.app = app
        # self.pyconsole = None
        # self.subtabledock = None
        # self.subtable = None
        # self.filterdock = None
        # self.finddock = None
        # self.mode = 'default'
        # self.table.model.dataChanged.connect(self.stateChanged)
        return