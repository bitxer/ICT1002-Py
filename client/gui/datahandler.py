from PyQt5.QtChart import QPieSeries


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

            if v['Protocol'] + ':' + str(v['Port']) not in protoports:
                protoports[v['Protocol'] + ':' + str(v['Port'])] = 1
            else:
                protoports[v['Protocol'] + ':' + str(v['Port'])] += 1

            atktime.append(v['Time'])

        for atk, val in summary['Atk'].items():
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
