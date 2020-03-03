import socket
from modules.Parser import Reader
from modules.Predict import run_predict_main

class ProcessData():
    def __init__(self, filename, format='csv'):
        self.filename = filename
        self.format = format
    
    def parse(self):
        self.reader = Reader(self.filename)
        self.df = self.reader.read()
        return self.df
    
    def analyse(self):
        self.analysis = run_predict_main(self.df)
        return self.analysis
