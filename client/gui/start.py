from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidget,QTableWidgetItem, QHeaderView, QGraphicsSimpleTextItem, QListWidget, QPushButton, QComboBox, QLineEdit, QGraphicsView
from PyQt5.QtChart import QChart, QChartView, QPieSeries, QPieSlice, QLineSeries, QDateTimeAxis, QDateTimeAxis, QValueAxis
from PyQt5.QtGui import QPainter, QPen, QMouseEvent
from PyQt5.QtCore import Qt
from devtools import filedata
import ast
import sys
from PyQt5.QtCore import QFile, QTextStream
from PyQt5.QtWidgets import QApplication
import time
import pandas as pd
import datetime


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
        
        # Exit
        self.actionExit.triggered.connect(self.exit)
        
         # Export IP 
        self.actionTop_5_IPs_Hits.triggered.connect(self.ExportIP)
        
        # Export Protocols
        self.actionTop_5_Protocols_Hits.triggered.connect(self.ExportProtocol)
        

        # displays
        self.displaychart("attackchart", self.chartseries, "Attack Types")
        self.displaytable("datatable", self.data.getData())
        # print(self.data.getData())
        self.displaytop("topip", self.data.getTopIPs(), ['IP Addresses', 'Count'])
        self.displaytop("topports", self.data.getTopProtocols(), ['Protocol : Port', 'Count'])
        # print(pd.DataFrame(self.data.topIPs(), index=[0]).transform)
        # self.displaytable("toplist", pd.DataFrame(self.data.topIPs(), index=[0]))

        self.isatksearch = self.findChild(QComboBox, "isAtk")
        self.ipsearch = self.findChild(QLineEdit, "ipaddr")
        self.protocolsearch = self.findChild(QLineEdit, "protocol")
        self.portsearch = self.findChild(QLineEdit, "port")
        self.atksearch = self.findChild(QLineEdit, "atk")
        self.timesearch = self.findChild(QLineEdit, "time")

        self.searchbtn = self.findChild(QPushButton, "searchbtn")
        self.searchbtn.clicked.connect(self.search)
        # LineChart(self.data.getAtkTime(), 'Attacks over Time')

        self.clearbtn = self.findChild(QPushButton, "clearbtn")
        self.clearbtn.clicked.connect(self.clear)

        self.graph()

    def graph(self):
        self.attackgraph = self.findChild(QChartView, "attackgraph")
        graph = QChart()
        graph.setAnimationOptions(QChart.AllAnimations)
        graph.setTitle("Attack over Time")
        graph.legend().hide()

        series = QLineSeries()


        # Filling QLineSeries
        for val in self.data.getAtkTime():
            # print("_____")
            # print(val)
            # print("_____")

            series.append(val,10)

        graph.addSeries(series)

        # Setting X-axis
        self.axis_x = QDateTimeAxis()
        self.axis_x.setTickCount(10)
        self.axis_x.setFormat("dd.MM (h:mm)")
        self.axis_x.setTitleText("Date")
        graph.addAxis(self.axis_x, Qt.AlignBottom)
        series.attachAxis(self.axis_x)
        # Setting Y-axis
        self.axis_y = QValueAxis()
        self.axis_y.setTickCount(10)
        self.axis_y.setLabelFormat("%.2f")
        self.axis_y.setTitleText("Attacks")
        graph.addAxis(self.axis_y, Qt.AlignLeft)
        series.attachAxis(self.axis_y)

        self.attackgraph.setChart(graph)
        # self.piechart.setRenderHint(QPainter.Antialiasing)



        # Getting the color from the QChart to use it on the QTableView
        # self.model.color = "{}".format(self.series.pen().color().name())

        # series = QLineSeries()
        # atkdata = self.data.getAtkTime()
        

        # self.attackgraph.setChart(series)

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
        
        
    def ExportIP(self):
        output = self.data.getTopIPs()
        fileName = QtWidgets.QFileDialog.getSaveFileName(None,  "Save CSV File", "", "CSV Files (*.csv)")
        if fileName[0]:
            with open(fileName[0], 'w') as f:
                f.write('IP Address, Counts\n')
                for key in output.keys():
                    f.write("%s,%s\n"%(key,output[key]))
            self.showMessageBox('File Exported',"File Exported successfully")
        else:
            self.showMessageBox('File not Exported',"File not Exported successfully")
        
        
    def ExportProtocol(self):
        output = self.data.getTopProtocols()
        fileName = QtWidgets.QFileDialog.getSaveFileName(None,  "Save CSV File", "", "CSV Files (*.csv)")
        if fileName[0]:
            with open(fileName[0], 'w') as f:
                f.write('Protocol & Ports, Counts\n')
                for key in output.keys():
                    f.write("%s,%s\n"%(key,output[key]))
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

        atktime = []

        protoports = {}
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

            # v = time.strftime('%m%y', time.gmtime(v['Time']))
            atktime.append(v['Time'])
            # if v not in atktime:
            #     atktime[v] = 1
            # else:
            #     atktime[v] += 1

            

        for atk, val in summary['Atk'].items():
            # print(atk)
            series.append(str(atk), int(val))

        self.summary = summary
        self.series = series
        self.protoports = protoports
        self.atktime = atktime

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
    
    def getAtkTime(self):
        return self.atktime

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


# class LineChart:
#     def __init__(self, data, title):
#         self.data = data
#         self.title = title
#         self.create()

#     def create(self):
#         series = QLineSeries()
#         print(self.data)

#         QDateTimeAxis.format()

        # for x in range(0, len(self.data.)):
        # series.append()


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

    main = MainWindow()
    main.showMaximized()
    # main.show()
    sys.exit(app.exec_())

if __name__ == '__main__':         
    main()