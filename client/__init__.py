import ast
import csv
import sys, os

from pandas import DataFrame, to_datetime
from PyQt5 import uic
from PyQt5.QtChart import QChartView, QValueAxis, QBarCategoryAxis, QBarSet, QBarSeries, QChart
from PyQt5.QtCore import QFile, QTextStream, Qt
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QApplication, QComboBox, QHeaderView, QLineEdit, QMainWindow, QPushButton, QTableWidget, QTableView,QTableWidgetItem, QMessageBox, QFileDialog

from client.charts import Piechart, Barchart
from client.datahandler import DataHandler
from client.logs import PandasModel
from modules.Processor import ProcessData
from modules.Parser import export_to_file

class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        #Load the UI Page
        uic.loadUi('client/main.ui', self)

        # upload
        self.actionUpload.triggered.connect(self.upload)
        
        # Exit
        self.actionExit.triggered.connect(self.exit)

        self.df = None
        self.searchdata = None
        
        # Export Protocols and IP
        self.actionSummary.triggered.connect(self.Summary)
        
        # Exporting table details
        self.actionTableDetails.triggered.connect(self.TableDetails)

    def popup(self):
        '''
        Popup Dialog to request file to be uploaded
        '''
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setWindowTitle("New File")
        msgBox.setText("Upload New File to Analyze.")
        msgBox.setStandardButtons(QMessageBox.Open)
        msgBox.buttonClicked.connect(self.upload)
        msgBox.exec()
        
    def upload(self):
        '''
        Uploads file to application
        '''
        fileName, _ = QFileDialog.getOpenFileName(None, "Select File", "", "Log Files (*.csv *.tsv *.json *.xls *.xlsx)")

        if fileName is not '':
            proc = ProcessData(fileName)
            proc.parse()
            data = proc.analyse()
            self.df = DataFrame.from_dict(data)

            self.display()
        else:
            self.showMessageBox("File Not Uploaded", "File Not Uploaded Successfully")
    
    def display(self):
        '''
        Calls the data processor DataHandler and displays the result
        '''
        if self.df is not None:
            self.data = DataHandler(self.df)
            QApplication.processEvents()

            # self.summary = self.data.getSummary()
            self.chartseries = self.data.getSeries()
            
            # Displays Charts and Tables
            self.displaychart("attackchart", self.chartseries, "Attack Types")
            self.displaytable("datatable", self.df)
            self.displaytop("topip", self.data.getTopIPs(), ['IP Addresses', 'Count'])
            self.displaytop("topports", self.data.getTopProtocols(), ['Protocol : Port', 'Count'])
            QApplication.processEvents()

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
            QApplication.processEvents()

            self.bargraph()
            QApplication.processEvents()

    def bargraph(self):
        '''
        Processes and Creates Bar Graph.
        '''
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
        '''
        Clears Search Form
        '''
        self.isatksearch.setCurrentIndex(0)
        self.ipsearch.clear()
        self.protocolsearch.clear()
        self.portsearch.clear()
        self.atksearch.clear()
        self.timesearch.clear()

        self.pdmdl.clear()
        self.searchdata = None
        self.logtable.setModel(self.pdmdl)
        
    def displaychart(self, widgetname, chartseries, title):
        '''
        Displays PieChart
        ------------------
        widgetname : str of widget to call in .ui file
        chartseries: PyQT Series to be displayed on chart
        title: str of title to be header of chart
        '''
        self.piechart = self.findChild(QChartView, widgetname)
        chartdata = Piechart(chartseries, title).create()
        self.piechart.setChart(chartdata)
        self.piechart.setRenderHint(QPainter.Antialiasing)

    def displaytop(self, widgetname, data, header):
        '''
        Displays Top IP/Protocols Table
        Parameters
        ------------------
        widgetname : str of widget to call in .ui file
        data: dict of top ip/protocol data to display
        title: str of title to be header of chart
        '''
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
        '''
        Displays Log Table
        Parameters
        ------------------
        widgetname: str of widget to call in .ui file
        data: Pandas Dataframe
        '''
        self.logtable = self.findChild(QTableView, widgetname)
        self.logtable.setSortingEnabled(True)
        self.pdmdl = PandasModel(data)
        self.logtable.setModel(self.pdmdl)
        self.logtable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.logtable.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def search(self):
        '''
        Checks Search Form to be sent to table
        '''
        # get searchquery as dictionary
        searchquery = {'IsAtk': self.isatksearch.currentText(), 'IP': self.ipsearch.text(), 'Protocol': self.protocolsearch.text(), 'Port': self.portsearch.text(), 'Atk': self.atksearch.text(), 'Time': self.timesearch.text()}
        # check if search query is not empty
        searchquery = {k: v for k, v in searchquery.items() if v != ''}

        atk = {'Yes': 1, 'No':0}

        if searchquery.get('IsAtk', None) == '-':
            del searchquery['IsAtk']
        elif searchquery.get('IsAtk', None) != None:
            searchquery['IsAtk'] = atk[searchquery['IsAtk']]

        # check if the searchquery is empty
        if bool(searchquery) is True:
            self.searchdata = self.pdmdl.search(searchquery)
            if self.searchdata is not None:
                self.logtable.setModel(PandasModel(self.searchdata, search=True))
            else:
                self.clear()
        else:
            self.clear()
            
    def Summary(self):
        '''
        Exports summary
        '''
        protocol = self.data.getTopProtocols()
        ip = self.data.getTopIPs()
        fileName = QFileDialog.getSaveFileName(self, "Save File", "", "Log Files (*.csv *.tsv *.json *.xls *.xlsx)")
        if fileName[0]:
            export_data = [x + y for x, y in zip(protocol.items(), ip.items())]
            export_dataframe = ['Protocol & Ports','Counts','IP Address','Counts']
            export_dataframe = DataFrame(export_data, columns=export_dataframe)
            export_to_file(fileName[0], export_dataframe)
            self.showMessageBox('File Exported',"File Exported successfully")
        else:
            self.showMessageBox('File not Exported',"File not Exported successfully")
            
    def TableDetails(self):
        '''
        Exports table data
        '''
        fileName = QFileDialog.getSaveFileName(self, "Save File", "", "Log Files (*.csv *.tsv *.json *.xls *.xlsx)")
        if self.searchdata is None:
            exportdata = self.data.getData()
            formatteddata = exportdata.transpose()
            formatteddata['IsAtk'] = formatteddata['IsAtk'].map({1:'Yes', 0:'No'}) # Changes 1 and 0 to Yes and No for table
            formatteddata['Time'] = to_datetime(formatteddata['Time'],unit='s') # Convert epoch time to human readable
        else:
            formatteddata = self.searchdata
        
        if fileName[0]:
            try:
                export_to_file(str(fileName[0]), formatteddata)
            except Exception as e:
                print(e)
                self.showMessageBox('File not Exported',"File not Exported successfully")
            else:
                self.showMessageBox('File Exported',"File Exported successfully")
            
    def showMessageBox(self,title,message):
        '''
        Display message box
        Parameters
        ----------
        title : str of title
        message : str of message to display
        '''
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setWindowTitle(title)
        msgBox.setText(message)
        msgBox.setStandardButtons(QMessageBox.Ok)
        msgBox.exec()

    def exit(self):
        sys.exit()

def start():
    app = QApplication(sys.argv)
    main = MainWindow()
    main.showMaximized()
    main.popup()
    sys.exit(app.exec_())

