from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidget,QTableWidgetItem, QHeaderView
from PyQt5.QtChart import QChart, QChartView, QPieSeries, QPieSlice
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtCore import Qt
from devtools import filedata
import ast
import sys
from PyQt5.QtCore import QFile, QTextStream
from PyQt5.QtWidgets import QApplication
import breeze_resources
import time

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        #Load the UI Page
        uic.loadUi('main.ui', self)

        rawdata = filedata().strip("\n")
        rawdata = ast.literal_eval(rawdata)

        self.data = DataHandler(rawdata)

        self.summary = self.data.getSummary()
        self.chartseries = self.data.getSeries()
        self.actionUpload.triggered.connect(self.addItem)
        self.actionExit.triggered.connect(self.exit)
        self.displaychart("attackchart", self.chartseries, "Attack Types")
        self.displaytable("datatable")

    def displaychart(self, widgetname, chartseries, header):
        piechart = self.findChild(QChartView, widgetname)
        chartdata = Piechart(chartseries, header).create()
        piechart.setChart(chartdata)
        piechart.setRenderHint(QPainter.Antialiasing)

    def displaytable(self, widgetname):
        table = self.findChild(QTableWidget, widgetname)
        display = DataTable(table, self.data.getData()).create()
    
    def addItem(self):
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(None, "Select Text File", "", "Text Files (*.txt)")
        print (fileName)
        
    def exit(self):
        sys.exit()



class DataHandler:
    def __init__(self, data):
        self.data = data
        self.process()

    def process(self):
        summary = {
            'AtkCount' : 0,
            'IP': {},
            'Protocol': {},
            'Port': {},
            'Atk' : {},
        }

        series = QPieSeries()
        
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
                summary['Protocol'][v['Protocol']] = 1
            else:
                summary['Protocol'][v['Protocol']] += 1

            if v['Port'] not in summary['Port']:
                summary['Port'][v['Port']] = 1
            else:
                summary['Port'][v['Port']] += 1

        print(summary)

        for atk, val in summary['Atk'].items():
            series.append(atk, val)

        self.summary = summary
        self.series = series

    def getSummary(self):
        return self.summary

    def getSeries(self):
        return self.series

    def getData(self):
        return self.data

class DataTable:
    def __init__(self, tableobj, tabledata):
        self.tableobj = tableobj
        self.tabledata = tabledata

    def create(self):
        self.tableobj.setColumnCount(6)
        self.tableobj.setRowCount(len(self.tabledata.keys()))
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

class Piechart:
    def __init__(self, chartseries, title):
        self.chartseries = chartseries
        self.title = title

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
        return chart


def main():
    app = QApplication(sys.argv)
    themefile = QFile(":/dark.qss")
    themefile.open(QFile.ReadOnly | QFile.Text)
    stream = QTextStream(themefile)
    app.setStyleSheet(stream.readAll())
    main = MainWindow()
    # main.showMaximized()
    main.show()
    sys.exit(app.exec_())

if __name__ == '__main__':         
    main()