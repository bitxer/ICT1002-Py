from PyQt5.QtChart import QChart, QPieSlice
from PyQt5.QtCore import Qt

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
        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignBottom)
        chart.legend().attachToChart()
        return chart
