import ast
import csv
import sys, os

import pandas as pd
from PyQt5 import uic
from PyQt5.QtChart import QChartView, QValueAxis, QBarCategoryAxis, QBarSet, QBarSeries, QChart
from PyQt5.QtCore import QFile, QTextStream, Qt
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import (QApplication, QComboBox, QHeaderView, QLineEdit,
                             QMainWindow, QPushButton, QTableWidget, QTableView,
                             QTableWidgetItem, QMessageBox, QFileDialog)

from charts import Piechart, Barchart
from datahandler import DataHandler
from devtools import filedata # remove for integration
from logs import PandasModel


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        #Load the UI Page
        uic.loadUi('main.ui', self)

        # upload
        self.actionUpload.triggered.connect(self.upload)
        
        # Exit
        self.actionExit.triggered.connect(self.exit)

        self.df = None
        
        # Export Protocols and IP
        self.actionSummary.triggered.connect(self.Summary)
        
        # Exporting table details
        self.actionTableDetails.triggered.connect(self.TableDetails)

    def popup(self):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setWindowTitle("New File")
        msgBox.setText("Upload New File to Analyze.")
        msgBox.setStandardButtons(QMessageBox.Open)
        msgBox.buttonClicked.connect(self.upload)
        msgBox.exec()
        
    def upload(self):
        fileName, _ = QFileDialog.getOpenFileName(None, "Select Text File", "", "Text Files (*.txt)")
        f = open(fileName, "r")

        # fileName, _ = QFileDialog.getOpenFileName(None, "Select Pcap File", "", "Text Files (*.pcap)") # use this line to open pcap

        ### insert handing over to ML side code here

        # if fileName:
        #     Clientsock.send(fileName)
        #     self.showMessageBox('File uploaded successfully',"File not uploaded successfully")




        # else:
        #     self.showMessageBox('File not Uploaded',"File not uploaded successfully")

        # return from ML code
        data = f.readline().strip("\n")
        data = ast.literal_eval(data)
        self.df = pd.DataFrame.from_dict(data)

        self.display()
    
    def display(self):
        if self.df is not None:
            self.data = DataHandler(self.df)

            self.summary = self.data.getSummary()
            self.chartseries = self.data.getSeries()
            
            # Displays Charts and Tables
            self.displaychart("attackchart", self.chartseries, "Attack Types")
            self.displaytable("datatable", self.data.getData())
            self.displaytop("topip", self.data.getTopIPs(), ['IP Addresses', 'Count'])
            self.displaytop("topports", self.data.getTopProtocols(), ['Protocol : Port', 'Count'])

            # Search Fields and Buttons
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

            self.bargraph()

    def bargraph(self):
        """
        Processes and Creates Bar Graph.
        """
        self.barchart = self.findChild(QChartView, "attackgraph")
        bardata = self.data.getBar()
        chartobj = Barchart(bardata)
        chartseries = chartobj.getSeries()

        # create QChart object and add data
        chart = QChart()
        chart.addSeries(chartseries)
        chart.setTitle("Attacks Over the Past 12 Months")
        chart.setAnimationOptions(QChart.SeriesAnimations)

        axisX = QBarCategoryAxis()
        axisX.append(chartobj.getKeys())
        chart.addAxis(axisX, Qt.AlignBottom)

        axisY = QValueAxis()
        axisY.setRange(0, chartobj.getMax())
        chart.addAxis(axisY, Qt.AlignLeft)

        chart.legend().setVisible(False)

        self.barchart.setChart(chart)

    def clear(self):
        """
        Clears Search Form
        """
        self.isatksearch.setCurrentIndex(0)
        self.ipsearch.clear()
        self.protocolsearch.clear()
        self.portsearch.clear()
        self.atksearch.clear()
        self.timesearch.clear()

        self.logtable.setModel(self.pdmdl)
        
    def displaychart(self, widgetname, chartseries, header):
        """
        Displays PieChart
        """
        self.piechart = self.findChild(QChartView, widgetname)
        chartdata = Piechart(chartseries, header).create()
        self.piechart.setChart(chartdata)
        self.piechart.setRenderHint(QPainter.Antialiasing)

    def displaytop(self, widgetname, data, header):
        """
        Displays Top Table
        """
        table = self.findChild(QTableWidget, widgetname)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        table.setColumnCount(2)
        table.setRowCount(5)
        table.setHorizontalHeaderLabels(header)
        index = 0
        for k,v in data.items():
            table.setItem(int(index),0, QTableWidgetItem(k))
            table.setItem(int(index),1, QTableWidgetItem(str(v)))
            index += 1

    def displaytable(self, widgetname, data):
        """
        Displays Log Table
        """
        self.logtable = self.findChild(QTableView, widgetname)
        self.logtable.setSortingEnabled(True)
        self.pdmdl = PandasModel(data)
        self.logtable.setModel(self.pdmdl)
        self.logtable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.logtable.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
    
    def search(self):
        """
        Checks search form to be sent to table
        """
        searchquery = {'IsAtk': self.isatksearch.currentText(), 'IP': self.ipsearch.text(), 'Protocol': self.protocolsearch.text(), 'Port': self.portsearch.text(), 'Atk': self.atksearch.text(), 'Time': self.timesearch.text()}
        searchquery = {k: v for k, v in searchquery.items() if v != '' or searchquery['IsAtk'] != '-'}
        if bool(searchquery) is True:
            search = self.pdmdl.search(searchquery)
            if search is not None:
                self.logtable.setModel(PandasModel(search, search=True))
            else:
                self.clear()
        else:
            self.clear()
            
    def Summary(self):
        protocol = self.data.getTopProtocols()
        ip = self.data.getTopIPs()
        fileName = QFileDialog.getSaveFileName(None,  "Save CSV File", "", "CSV Files (*.csv)")
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
        fileName = QFileDialog.getSaveFileName(None,  "Save CSV File", "", "CSV Files (*.csv)")
        exportdata = self.data.getData()
        formatteddata = exportdata.transpose()
        formatteddata['IsAtk'] = formatteddata['IsAtk'].map({1:'Yes', 0:'No'}) # Changes 1 and 0 to Yes and No for table
        formatteddata['Time'] = pd.to_datetime(formatteddata['Time'],unit='s') # Convert epoch time to human readable
        if fileName[0]:
            try:
                formatteddata.to_csv(str(fileName[0]), header=True)
            except:
                self.showMessageBox('File not Exported',"File not Exported successfully")
            else:
                self.showMessageBox('File Exported',"File Exported successfully")
            
    def showMessageBox(self,title,message):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setWindowTitle(title)
        msgBox.setText(message)
        msgBox.setStandardButtons(QMessageBox.Ok)
        msgBox.exec()

    def exit(self):
        sys.exit()

def main():
    app = QApplication(sys.argv)
    main = MainWindow()
    main.showMaximized()
    # main.show()
    main.popup()
    sys.exit(app.exec_())

if __name__ == '__main__':         
    main()
