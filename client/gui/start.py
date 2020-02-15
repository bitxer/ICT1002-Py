from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtChart import QChart, QChartView, QPieSeries
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtCore import Qt
from devtools import filedata
import ast

import sys

class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        #Load the UI Page
        uic.loadUi('main.ui', self)

        data = filedata().strip("\n")
        data = ast.literal_eval(data)

        self.displaychart("piechart1", data)
    

    def displaychart(self, widgetname, data):
        piechart = self.findChild(QChartView, widgetname)
        chartdata = Piechart(data, "Attacks").create()
        piechart.setChart(chartdata)
        piechart.setRenderHint(QPainter.Antialiasing)

class Piechart:
    def __init__(self, data, title):
        self.data = data
        self.title = title

    def datahandler(self):
        summary = {
            'AtkCount' : 0,
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

        print(summary)

        for atk, val in summary['Atk'].items():
            series.append(atk, val)

        return series
            

    def create(self):
        series = self.datahandler()

        chart = QChart()
        chart.addSeries(series)
        chart.setAnimationOptions(QChart.SeriesAnimations)
        chart.setTitle(self.title)

        return chart


def main():
    app = QApplication(sys.argv)
    main = MainWindow()
    main.showMaximized()
    sys.exit(app.exec_())

if __name__ == '__main__':         
    main()
