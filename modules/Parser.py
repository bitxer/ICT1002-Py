import os
from pandas import read_csv, read_excel, read_json
from pandas import DataFrame

class Reader():
    def __init__(self, path, importformat):
        '''
        Initialise reader to read log data
        
        Parameters
        ----------
        path : str
            Path to log file
        importformat : int
            importformat can be one of 4 values [1, 2, 3, 4] to represent
            [csv, tsv, json, excel] file format respectively.
            
        Raise
        -----
        FileExistsError
            Raised when file exists and user does not want to overwrite file
        ValueError
            Raised when a invalid file format is given
        '''
        self.path = path
        # if os.path.exists(path):
        #     self.path = path
        # else:
        #     raise FileNotFoundError("Specified directory not present")
            
        importformats = {1: '_csv', 2: "_tsv", 3: '_json', 4: '_excel'}
        if importformat not in importformats.keys():
            raise ValueError('Invalid format specified')
        
        self.importformat = importformats[importformat]


    def read(self):
        '''
        Reads data from file and return the data in dataframe
        
        Return
        ------
        [Success]
            data : DataFrame
                Data of file loaded into dataframe
        
        Raise
        -----
        Exception
            If read is unsuccessful
        '''
        _csv = lambda : read_csv(self.path)
        _tsv = lambda : read_csv(self.path, sep='\t')
        _json = lambda : read_json(self.path)
        _excel = lambda : read_excel(self.path)

        return eval('{}()'.format(self.importformat))

def export_to_file(path, exporttype, df):
    writer = Writer(path, exporttype, df)
    return writer.write()

class Writer():
    def __init__(self, path, exporttype, df):
        '''
        Initialise writer to write data to file
        
        Parameters
        ----------
        path : str
            Path to write file to
        exporttype : int
            exporttype can be one of 4 values [1, 2 ,3, 4] to represent
            [csv, tsv, json, excel] file format respectively.
        df : pandas dataframe
            pandas dataframe containing data to be exported

        Raise
        -----
        ValueError
            Raised when a invalid file format is given
        '''
        self.path = path
        
        self.df = df

        exporttypes = {1: '_csv', 2: "_tsv", 3: '_json', 4: '_excel'}
        if exporttype not in exporttypes.keys():
            raise ValueError('Invalid type specified')
        
        self.exporttype = exporttypes[exporttype]
    
    def write(self):
        '''
        Writes data from dataframe into file
        
        Returns
        -------
        [Success]
            True : Boolean
                Returns True if data write is successful
            
        Raise
        -----
        Exception
            If write is unsuccessful and an exception is raised
        '''
        _csv = lambda : self.df.to_csv(index=False, header=True, path_or_buf=self.path)
        _tsv = lambda : self.df.to_csv(index=False, header=True,  path_or_buf=self.path, sep='\t')
        _json = lambda : self.df.to_json(index=False, header=True, path_or_buf=self.path)
        _excel = lambda : self.df.to_excel(index=False, header=True, path_or_buf=self.path)

        eval('{}()'.format(self.exporttype))
        return True