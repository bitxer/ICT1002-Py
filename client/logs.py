import time

from PyQt5.QtCore import QAbstractTableModel, QVariant
from PyQt5.QtCore import Qt, QItemSelectionModel
from PyQt5.QtWidgets import QHeaderView, QTableWidgetItem
import pandas as pd
import numpy as np

class PandasModel(QAbstractTableModel):
    header = ["Time", "IP Address", "Protocol", "Port", "Attack"]
    def __init__(self, data, parent=None, search=None):
        '''
        Table Model for Log Table
        Parameters
        --------------------------
        data : Pandas DataFrame to be processed and displayed
        search : Boolean, if search is True (not None), will be processing it as a search function
        '''
        QAbstractTableModel.__init__(self, parent)
        self.header = ["Time", "IP", "Protocol", "Port", "Atk"]

        if search is None:
            self.ogdata = data.transpose() # for search
            self.ogdata['Time'] = pd.to_datetime(self.ogdata['Time'],unit='s') # Convert epoch time to human readable
            self._data = data.transpose()
            self._data = self._data[self.header]
        else:
            self._data = data
        
        self.rowcount = len(self._data.values)
        self._data['Atk'] = self._data['Atk'].fillna('Not Attack') # replace nan with Not Attack
        self._data['Time'] = pd.to_datetime(self._data['Time'],unit='s') # Convert epoch time to human readable

    def rowCount(self, parent=None):
        '''
        Return Row Count
        '''
        return self.rowcount

    def columnCount(self, parent=None):
        '''
        Return Column Count
        '''
        return self._data.columns.size

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        '''
        Set the Headers of the table
        '''
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return self.header[section]
        return QAbstractTableModel.headerData(self, section, orientation, role)
    
    def data(self, index, role=Qt.DisplayRole):
        '''
        Set data of the table
        '''
        if index.isValid():
            if role == Qt.DisplayRole:
                return QVariant(str(
                    self._data.values[index.row()][index.column()]))
        return QVariant()
    
    def sort(self, Ncol, order):
        '''
        Sort table by given column number.
        '''
        try:
            self.layoutAboutToBeChanged.emit()
            self._data = self._data.sort_values(self._data.columns[Ncol], ascending=not order)
            self.layoutChanged.emit()
        except Exception as e:
            print(e)

    def _search(self):
        '''
        Recursive function to process search query
        '''
        if len(self.query.keys()) == 0:
            return False

        key = list(self.query.keys())[0]
        value = self.query.pop(key)
        result = None
        con = '(?i){}'.format(value)
        if key != 'Time':
            result = self.ogdata[key].astype(str).str.contains(con)
        else:
            result = self.ogdata[key].dt.strftime("%Y-%m-%d %H:%M:%S").str.contains(con) 
        
        if self.query == {}:
            return result
        else:
            return result & self._search()


    def search(self, query):
        '''
        Process and Returns Search Dataframe
        '''
        self.query = query

        result = self._search()
        result = self.ogdata[result]
        self.rowcount = len(result)
        return result[self.header]
    
    def clear(self):
        self.rowcount = len(self._data.values)
