from PyQt5.QtChart import QChart, QPieSlice, QBarSet, QBarSeries
from PyQt5.QtCore import Qt
import time
from collections import OrderedDict

class Piechart:
    """
    Processes Pie Chart
    """
    def __init__(self, chartseries, title):
        self.chartseries = chartseries
        self.title = title

    def create(self):
        """
        Creates Chart Data and returns
        """
        slices = QPieSlice()
        for x in range(0, len(self.chartseries.slices())):
            slices = self.chartseries.slices()[x]
            slices.setLabelVisible()
            slices.setLabel(str(slices.label()) + " : " + str(slices.value()))

        chart = QChart()
        chart.addSeries(self.chartseries)
        chart.setAnimationOptions(QChart.SeriesAnimations)
        chart.setTitle(self.title)
        # chart.setTheme(5)
        chart.legend().setVisible(False)
        chart.legend().attachToChart()
        return chart

class Barchart:
    """
    Processes BarChart Data
    """
    def __init__(self, data):
        self.data = data
        self.handler()
    
    def handler(self):
        """
        Processes Data
        """
        barset = QBarSet('Attacks')
        countdata = self.data.agg('count')
        self.max = countdata.max()
        now = time.localtime()
        past12months = [time.localtime(time.mktime((now.tm_year, now.tm_mon - n, 1, 0, 0, 0, 0, 0, 0)))[:2] for n in range(12)] # get the past 12 months from current date
        datadict = {}

        for key in past12months:
            for k,v in countdata.items():
                if k == key:
                    datadict[k] = v

        # set value to 0 if no attacks in a key (month)
        for k in past12months:
            if k not in datadict.keys():
                datadict[k] = 0

        self.sorteddict = OrderedDict(sorted(datadict.items()))
        setlist = [value for key, value in self.sorteddict.items()] # list of attack counts over the past 12 months to append to barset
        barset.append(setlist)
        self.series = QBarSeries()
        self.series.setLabelsVisible(True)
        self.series.append(barset)

    def getSeries(self):
        """
        Returns Series for QChart
        """
        return self.series

    def getKeys(self):
        """
        Returns the month/year for the X-Axis
        """
        months = tuple(self.sorteddict.keys())
        monthdict = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun', 7: 'Jul', 8: 'Aug', 9: 'Sept', 10: 'Oct', 11: 'Nov', 12: 'Dec'}

        output = []
        for item in months:
            mmyy = str(monthdict[item[1]]) + " " + str(item[0])
            output.append(mmyy)
        
        return tuple(output)
    
    def getMax(self):
        """
        Returns highest attack count for the Y-Axis
        """
        return self.max