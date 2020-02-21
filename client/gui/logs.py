from PyQt5.QtWidgets import QHeaderView, QTableWidgetItem
import time

class DataTable:
    def __init__(self, tableobj, tabledata):
        self.tableobj = tableobj
        self.tabledata = tabledata
        self.tableobj.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableobj.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

    def create(self):
        self.tableobj.setColumnCount(len(self.tabledata.values))
        self.tableobj.setRowCount(len(self.tabledata.keys()))
        self.tableobj.setHorizontalHeaderLabels(["Is Attack", "IP Address", "Protocol", "Port", "Attack", "Time"])
        for k,v in self.tabledata.items():
            index = k
            rowcount = 0

            for k,v in v.items():
                if k == 'IsAtk':
                    if v == 1:
                        v = 'Yes'
                    else:
                        v = 'No'

                if k == 'Time':
                    v = time.strftime('%m/%d/%Y %H:%M:%S', time.gmtime(v))

                self.tableobj.setItem(int(index), rowcount, QTableWidgetItem(str(v)))
                rowcount += 1

    def search(self, query):
        for rowIndex in range(self.tableobj.rowCount()):
            srchflag = 0
            for column in range(self.tableobj.columnCount()):
                twItem = self.tableobj.item(rowIndex, column)

                if query is None:
                    self.tableobj.setRowHidden(rowIndex, False)
                else:
                    if column == 3:
                        if query[column] != '':
                                if twItem.text().lower() == query[column].lower():
                                    if srchflag == 0:
                                        self.tableobj.setRowHidden(rowIndex, False)
                                    else:
                                        self.tableobj.setRowHidden(rowIndex, True)
                                else:
                                    srchflag = 1
                                    self.tableobj.setRowHidden(rowIndex, True)
                    else:
                        if column == 0:
                            if query[column] == '-':
                                self.tableobj.setRowHidden(rowIndex, False)
                            else:
                                if twItem.text().lower() == query[column].lower():
                                    if srchflag == 0:
                                        self.tableobj.setRowHidden(rowIndex, False)
                                    else:
                                        self.tableobj.setRowHidden(rowIndex, True)
                                else:
                                    srchflag = 1
                                    self.tableobj.setRowHidden(rowIndex, True)
                        else:
                            if twItem.text().lower().find(query[column].lower()) != -1:
                                if srchflag == 0:
                                    self.tableobj.setRowHidden(rowIndex, False)
                                else:
                                    self.tableobj.setRowHidden(rowIndex, True)
                            else:
                                srchflag = 1
                                self.tableobj.setRowHidden(rowIndex, True)
