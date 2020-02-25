import time

from PyQt5.QtCore import QAbstractTableModel, QVariant
from PyQt5.QtCore import Qt, QItemSelectionModel
from PyQt5.QtWidgets import QHeaderView, QTableWidgetItem
import pandas as pd

class PandasModel(QAbstractTableModel):
    """
    Table Model for Log Table
    """
    header = ["Is Attack", "IP Address", "Protocol", "Port", "Attack", "Time"]

    def __init__(self, data, parent=None, search=None):
        QAbstractTableModel.__init__(self, parent)
        if search is None:
            self._data = data.transpose()
            self._data['IsAtk'] = self._data['IsAtk'].map({1:'Yes', 0:'No'}) # Changes 1 and 0 to Yes and No for table
            self._data['Time'] = pd.to_datetime(self._data['Time'],unit='s') # Convert epoch time to human readable
        else:
            self._data = data

    def rowCount(self, parent=None):
        """
        Return Row Count
        """
        return len(self._data.values)

    def columnCount(self, parent=None):
        """
        Return Column Count
        """
        return self._data.columns.size

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        """
        Set the Headers of the table
        """
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return self.header[section]
        return QAbstractTableModel.headerData(self, section, orientation, role)
    
    def data(self, index, role=Qt.DisplayRole):
        """
        Set data of the table
        """
        if index.isValid():
            if role == Qt.DisplayRole:
                return QVariant(str(
                    self._data.values[index.row()][index.column()]))
        return QVariant()
    
    def sort(self, Ncol, order):
        """Sort table by given column number.
        """
        try:
            self.layoutAboutToBeChanged.emit()
            self._data = self._data.sort_values(self._data.columns[Ncol], ascending=not order)
            self.layoutChanged.emit()
        except Exception as e:
            print(e)

    def search(self, query):
        """
        Process and Returns Search Dataframe
        """
        self.query = query

        if bool(self.query) is True: # check if query is not empty
            pdquery = ''

            for k,v in self.query.items():
                if k != 'Time':
                    pdquery += 'self._data["'+str(k)+'"].str.contains("(?i)' + str(v) + '") & ' # compare string for time
                else:
                    pdquery += 'self._data[\'Time\'].dt.strftime("%Y-%m-%d %H:%M:%S").str.contains("(?i)' + str(v) + '") & ' # check if string contains

            if pdquery == 'self._data["IsAtk"].str.contains("(?i)-") & ': 
                # if the IsAtk field is only - return None to not carry out search
                return None 

            if pdquery != '':
                pdquery = 'self._data[' + pdquery[:-3] + ']'
                searched = eval(pdquery) # evaluate and return search df
                return searched