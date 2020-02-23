from PyQt5.QtChart import QChart, QPieSlice, QBarSet, QBarSeries
from PyQt5.QtCore import Qt
import time
from collections import OrderedDict

class Piechart:
    def __init__(self, chartseries, title):
        self.chartseries = chartseries
        self.title = title

    def create(self):
        slices = QPieSlice()
        for x in range(0, len(self.chartseries.slices())):
            slices = self.chartseries.slices()[x]
            slices.setLabelVisible()
            slices.setLabel(str(slices.label()) + " : " + str(slices.value()))

        chart = QChart()
        chart.addSeries(self.chartseries)
        chart.setAnimationOptions(QChart.SeriesAnimations)
        chart.setTitle(self.title)
        chart.setTheme(5)
        chart.legend().setVisible(False)
        chart.legend().attachToChart()
        return chart

class Barchart:
    def __init__(self, data):
        self.data = data
        self.handler()
    
    def handler(self):
        barset = QBarSet('Attacks')
        countdata = self.data.agg('count')
        self.max = countdata.max()
        now = time.localtime()
        past12months = [time.localtime(time.mktime((now.tm_year, now.tm_mon - n, 1, 0, 0, 0, 0, 0, 0)))[:2] for n in range(12)]
        datadict = {}

        for key in past12months:
            for k,v in countdata.items():
                if k == key:
                    datadict[k] = v

        for k in past12months:
            if k not in datadict.keys():
                datadict[k] = 0

        self.sorteddict = OrderedDict(sorted(datadict.items()))
        setlist = [value for key, value in self.sorteddict.items()]
        
        barset.append(setlist)
        self.series = QBarSeries()
        self.series.append(barset)

    def getSeries(self):
        return self.series

    def getKeys(self):
        months = tuple(self.sorteddict.keys())
        output = []
        for item in months:
            output.append(str(item))
        
        return tuple(output)
    
    def getMax(self):
        return self.max