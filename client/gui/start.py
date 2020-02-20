from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidget,QTableWidgetItem, QHeaderView, QGraphicsSimpleTextItem, QListWidget, QPushButton, QComboBox, QLineEdit
from PyQt5.QtChart import QChart, QChartView, QPieSeries, QPieSlice
from PyQt5.QtGui import QPainter, QPen, QMouseEvent
from PyQt5.QtCore import Qt
from devtools import filedata
import ast
import sys
from PyQt5.QtCore import QFile, QTextStream
from PyQt5.QtWidgets import QApplication
import breeze_resources
import time
import pandas as pd
import qdarkstyle

class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        #Load the UI Page
        uic.loadUi('main.ui', self)

        rawdata = filedata().strip("\n")
        rawdata = ast.literal_eval(rawdata)

        # data
        df = pd.DataFrame.from_dict(rawdata)

        self.data = DataHandler(df)
        self.summary = self.data.getSummary()
        self.chartseries = self.data.getSeries()
        
        # upload
        self.actionUpload.triggered.connect(self.addItem)
        self.actionExit.triggered.connect(self.exit)

        # displays
        self.displaychart("attackchart", self.chartseries, "Attack Types")
        self.displaytable("datatable", self.data.getData())
        # print(self.data.getData())
        self.displaytop("topip", self.data.getTopIPs(), ['IP Addresses', 'Count'])
        self.displaytop("topports", self.data.getTopProtocols(), ['Protocol : Port', 'Count'])
        # print(pd.DataFrame(self.data.topIPs(), index=[0]).transform)
        # self.displaytable("toplist", pd.DataFrame(self.data.topIPs(), index=[0]))

        self.searchbtn = self.findChild(QPushButton, "searchbtn")
        self.searchbtn.clicked.connect(self.search)

    def search(self):
        self.isatksearch = self.findChild(QComboBox, "isAtk").currentText()
        self.ipsearch = self.findChild(QLineEdit, "ipaddr").text()
        self.protocolsearch = self.findChild(QLineEdit, "protocol").text()
        self.portsearch = self.findChild(QLineEdit, "port").text()
        self.atksearch = self.findChild(QLineEdit, "atk").text()
        self.timesearch = self.findChild(QLineEdit, "time").text()

        searchquery = [self.isatksearch, self.ipsearch, self.protocolsearch,self.portsearch, self.atksearch, self.timesearch]

        print(searchquery)

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

    def exit(self):
        sys.exit()

class DataHandler:
    def __init__(self, data):
        self.data = data
        self.process()
        self.topIPs()
        self.topProtocols()

    def process(self):
        summary = {
            'AtkCount' : 0,
            'IP': {},
            'Protocol': {},
            'Port': {},
            'Atk' : {},
        }

        protoports = {}
        # print(self.data)

        series = QPieSeries()

        counter = 0

        for k,v in self.data.items():
            if v['IsAtk'] == 1:
                summary['AtkCount'] = summary['AtkCount'] + 1

            if v['Atk'] not in summary['Atk']:
                summary['Atk'][v['Atk']] = 1
            else:
                summary['Atk'][v['Atk']] += 1

            if v['IP'] not in summary['IP']:
                summary['IP'][v['IP']] = 1
            else:
                summary['IP'][v['IP']] += 1

            if v['Protocol'] not in summary['Protocol']:
                # print(v)
                # print('----')
                summary['Protocol'][v['Protocol']] = 1
            else:
                summary['Protocol'][v['Protocol']] += 1

            if v['Port'] not in summary['Port']:
                summary['Port'][v['Port']] = 1
            else:
                summary['Port'][v['Port']] += 1

            if v['Protocol'] + ':' + str(v['Port']) not in protoports:
                protoports[v['Protocol'] + ':' + str(v['Port'])] = 1
            else:
                protoports[v['Protocol'] + ':' + str(v['Port'])] += 1

        for atk, val in summary['Atk'].items():
            series.append(atk, val)

        self.summary = summary
        self.series = series
        self.protoports = protoports

    def topIPs(self):
        top = sorted(self.summary['IP'], key=self.summary['IP'].get, reverse=True)
        output = {}
        for x in top:
            output[x] = self.summary['IP'][x]

        self.topips = output

    def topProtocols(self):
        top = sorted(self.protoports, key=self.protoports.get, reverse=True)
        output = {}
        for x in top:
            output[x] = self.protoports[x]
        
        self.protoports = output

    def getSummary(self):
        return self.summary

    def getSeries(self):
        return self.series

    def getData(self):
        return self.data

    def getTopIPs(self):
        return self.topips

    def getTopProtocols(self):
        return self.protoports

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
                    v = 'Yes'

                if k == 'Time':
                    v = time.strftime('%m/%d/%Y %H:%M:%S', time.gmtime(v))

                self.tableobj.setItem(int(index), rowcount, QTableWidgetItem(str(v)))
                rowcount += 1

    def search(self, query):
        for rowIndex in range(self.tableobj.rowCount()):
            srchflag = 0
            for column in range(self.tableobj.columnCount()):
                twItem = self.tableobj.item(rowIndex, column)
                if column != 4 and column != 5:
                    if query[column] != '':
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
                            if twItem.text().lower() == query[column].lower():
                                if srchflag == 0:
                                    self.tableobj.setRowHidden(rowIndex, False)
                                else:
                                    self.tableobj.setRowHidden(rowIndex, True)
                            else:
                                srchflag = 1
                                self.tableobj.setRowHidden(rowIndex, True)
                else:
                    print(query[column])
                    print(twItem.text())
                    if twItem.text().lower().find(query[column].lower()) != -1:
                        if srchflag == 0:
                            self.tableobj.setRowHidden(rowIndex, False)
                        else:
                            self.tableobj.setRowHidden(rowIndex, True)
                    else:
                        srchflag = 1
                        self.tableobj.setRowHidden(rowIndex, True)

class Piechart:
    def __init__(self, chartseries, title):
        self.chartseries = chartseries
        self.title = title

    # def pieclick(self):
    #     print("HI")

    def create(self):
        slices = QPieSlice()
        for x in range(0, len(self.chartseries.slices())):
            slices = self.chartseries.slices()[x]
            slices.setLabelVisible(True)

        chart = QChart()
        chart.addSeries(self.chartseries)
        chart.setAnimationOptions(QChart.SeriesAnimations)
        chart.setTitle(self.title)
        chart.setTheme(5)
        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignBottom)
        chart.legend().attachToChart()
        return chart


def main():
    app = QApplication(sys.argv)

    # themefile = QFile(":/dark.qss")
    # themefile.open(QFile.ReadOnly | QFile.Text)
    # stream = QTextStream(themefile)
    # app.setStyleSheet(stream.readAll())
    # app.setStyleSheet(qdarkstyle.load_stylesheet())
    main = MainWindow()
    main.showMaximized()
    # main.show()
    sys.exit(app.exec_())

if __name__ == '__main__':         
    main()