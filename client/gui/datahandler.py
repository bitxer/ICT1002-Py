from PyQt5.QtChart import QPieSeries
import pandas as pd

class DataHandler:
    """
    DataHandler Class to process data
    """
    def __init__(self, data):
        self.data = data
        self.process()
        self.topIPs()
        self.topProtocols()

    def process(self):
        """
        Processes Summary and Chart Data
        """
        self.summary = {
            'AtkCount' : self.data.loc['IsAtk'].value_counts()[1], # count number of 1s in the column
            'IP': self.data.loc['IP'].value_counts().to_dict(),
            'Protocol': self.data.loc['Protocol'].value_counts().to_dict(),
            'Port': self.data.loc['Port'].value_counts(),
            'Atk' : self.data.loc['Atk'].value_counts(),
        }

        # process piechart data
        series = QPieSeries()
        for atk, val in self.summary['Atk'].items():
            series.append(str(atk), int(val))
        self.series = series

        # process top protocol data
        self.protoports = self.data.transpose().groupby(["Protocol", "Port"]).size().to_dict()
        self.protoports = {str(key[0])+':'+str(key[1]):value for key, value in self.protoports.items()} # create dictionary with key of format "protocol:port"

        # process barchart data
        self.bardata = self.data.transpose()
        self.bardata = pd.to_datetime(self.bardata['Time'], unit='s')
        self.bardata = self.bardata.groupby([self.bardata.dt.year, self.bardata.dt.month])


    def topIPs(self):
        """
        Process Top IPs List
        """
        top = sorted(self.summary['IP'], key=self.summary['IP'].get, reverse=True)
        output = {}
        for x in top:
            output[x] = self.summary['IP'][x]

        self.topips = output

    def topProtocols(self):
        """
        Process Top Protocols List
        """
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

    def getBar(self):
        return self.bardata