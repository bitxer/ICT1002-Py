import ast
import sys
from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidget, QTableWidgetItem, QHeaderView, QPushButton, QComboBox, QLineEdit
from PyQt5.QtChart import QChartView
from PyQt5.QtGui import QPainter
from PyQt5.QtCore import QFile, QTextStream
from devtools import filedata
import pandas as pd
import csv
from datahandler import DataHandler
from logs import DataTable
from charts import Piechart


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        #Load the UI Page
        uic.loadUi('main.ui', self)

        rawdata = filedata().strip("\n")
        rawdata = ast.literal_eval(rawdata)
        df = pd.DataFrame.from_dict(rawdata)

        self.data = DataHandler(df)
        self.summary = self.data.getSummary()
        self.chartseries = self.data.getSeries()
        
        # displays
        self.displaychart("attackchart", self.chartseries, "Attack Types")
        self.displaytable("datatable", self.data.getData())

        self.displaytop("topip", self.data.getTopIPs(), ['IP Addresses', 'Count'])
        self.displaytop("topports", self.data.getTopProtocols(), ['Protocol : Port', 'Count'])

        # search
        self.isatksearch = self.findChild(QComboBox, "isAtk")
        self.ipsearch = self.findChild(QLineEdit, "ipaddr")
        self.protocolsearch = self.findChild(QLineEdit, "protocol")
        self.portsearch = self.findChild(QLineEdit, "port")
        self.atksearch = self.findChild(QLineEdit, "atk")
        self.timesearch = self.findChild(QLineEdit, "time")

        self.searchbtn = self.findChild(QPushButton, "searchbtn")
        self.searchbtn.clicked.connect(self.search)

        self.clearbtn = self.findChild(QPushButton, "clearbtn")
        self.clearbtn.clicked.connect(self.clear)

        # upload
        self.actionUpload.triggered.connect(self.addItem)
        
        # Exit
        self.actionExit.triggered.connect(self.exit)
        
        # Export Protocols and IP
        self.actionSummary.triggered.connect(self.Summary)
        
        # Exporting table details
        self.actionTableDetails.triggered.connect(self.TableDetails)

    def clear(self):
        self.isatksearch.setCurrentIndex(0)
        self.ipsearch.clear()
        self.protocolsearch.clear()
        self.portsearch.clear()
        self.atksearch.clear()
        self.timesearch.clear()

        table = self.findChild(QTableWidget, "datatable")
        table.setSortingEnabled(True)
        DataTable(table, self.data.getData()).search(query=None)

    def search(self):
        searchquery = [self.isatksearch.currentText(), self.ipsearch.text(), self.protocolsearch.text(),self.portsearch.text(), self.atksearch.text(), self.timesearch.text()]

        table = self.findChild(QTableWidget, "datatable")
        table.setSortingEnabled(True)
        DataTable(table, self.data.getData()).search(searchquery)

    def displaychart(self, widgetname, chartseries, header):
        self.piechart = self.findChild(QChartView, widgetname)
        chartdata = Piechart(chartseries, header).create()
        self.piechart.setChart(chartdata)
        self.piechart.setRenderHint(QPainter.Antialiasing)

    def displaytop(self, widgetname, data, header):
        table = self.findChild(QTableWidget, widgetname)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        table.setColumnCount(2)
        table.setRowCount(5)
        table.setHorizontalHeaderLabels(header)
        index = 0
        for k,v in data.items():
            # print(k,v)
            table.setItem(int(index),0, QTableWidgetItem(k))
            table.setItem(int(index),1, QTableWidgetItem(str(v)))
            index += 1

    def displaytable(self, widgetname, data):
        table = self.findChild(QTableWidget, widgetname)
        table.setSortingEnabled(True)
        DataTable(table, data).create()

    def addItem(self):
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(None, "Select Text File", "", "Text Files (*.txt)")
        print (fileName)
        
            
    def Summary(self):
        protocol = self.data.getTopProtocols()
        ip = self.data.getTopIPs()
        fileName = QtWidgets.QFileDialog.getSaveFileName(None,  "Save CSV File", "", "CSV Files (*.csv)")
        if fileName[0]:
            with open(fileName[0], 'w') as csv_file:
                fieldnames = ['Protocol & Ports', 'Counts', 'IP Address', 'Counts']
                writer = csv.writer(csv_file,lineterminator='\n')
                writer.writerow(fieldnames)

                for proto, ips in zip(protocol.items(), ip.items()):
                    writer.writerow(proto + ips)
            self.showMessageBox('File Exported',"File Exported successfully")
        else:
            self.showMessageBox('File not Exported',"File not Exported successfully")
            
            
    def TableDetails(self):
        fileName = QtWidgets.QFileDialog.getSaveFileName(None,  "Save CSV File", "", "CSV Files (*.csv)")
        if fileName[0]:
            with open(fileName[0], 'w') as csv_file:
                fieldnames = ['IS Attack', 'IP Address', 'Protocol', 'Port', 'Attack','Time']
                writer = csv.writer(csv_file, lineterminator='\n')   
                writer.writerow(fieldnames)
                for row in range(self.datatable.rowCount()):
                    rowdata = []
                    for column in range(self.datatable.columnCount()):
                        item = self.datatable.item(row, column)
                        if item is not None:                        
                            rowdata.append(item.text())                  
                        else:
                            rowdata.append('')
                    writer.writerow(rowdata)
            self.showMessageBox('File Exported',"File Exported successfully")
        else:
            self.showMessageBox('File not Exported',"File not Exported successfully")
    
            
    def showMessageBox(self,title,message):
        msgBox = QtWidgets.QMessageBox()
        msgBox.setIcon(QtWidgets.QMessageBox.Information)
        msgBox.setWindowTitle(title)
        msgBox.setText(message)
        msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msgBox.exec()


    def exit(self):
        sys.exit()

def main():
    app = QApplication(sys.argv)

    main = MainWindow()
    main.showMaximized()
    sys.exit(app.exec_())

if __name__ == '__main__':         
    main()