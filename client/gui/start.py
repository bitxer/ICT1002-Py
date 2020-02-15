from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtChart import QChart, QChartView, QPieSeries
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtCore import Qt

import sys

class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        #Load the UI Page
        uic.loadUi('main.ui', self)

        self.create_piechart()

    def create_piechart(self):
        series = QPieSeries()
        series.append("Bot", 10)
        series.append("Brute Force -Web", 10)
        series.append("Brute Force -XSS", 50)
        series.append("DDOS attack -HOIC", 30)

        chart = QChart()
        chart.addSeries(series)
        chart.setAnimationOptions(QChart.SeriesAnimations)
        chart.setTitle("Attacks")

        piechart1 = self.findChild(QChartView, "piechart1")
        piechart1.setChart(chart)
        piechart1.setRenderHint(QPainter.Antialiasing)


def main():
    app = QApplication(sys.argv)
    main = MainWindow()
    main.showMaximized()
    sys.exit(app.exec_())

if __name__ == '__main__':         
    main()
