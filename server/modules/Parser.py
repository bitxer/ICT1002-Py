import os
from pandas import read_csv, read_excel, read_json

class Reader():
    def __init__(self, data, type):
        '''
        Initialise reader to read log data
        
        Parameters
        ----------
        path : str
            Path to log file
        type : int
            type can be one of 4 values [1, 2, 3, 4, 5, 6] to represent
            [csv, tsv, json, excel, syslog, pcap] file type respectively.
            
        Raise
        -----
        FileExistsError
            Raised when file exists and user does not want to overwrite file
        ValueError
            Raised when a invalid file type is given
        '''
        self.data = data
        # if os.path.exists(path):
        #     self.path = path
        # else:
        #     raise FileNotFoundError("Specified directory not present")
            
        types = {1: '_csv', 2: "_tsv", 3: '_json', 4: '_excel', 5: '_syslog', 6: '_pcap'}
        if type not in types.keys():
            raise ValueError('Invalid type specified')
        
        self.type = types[type]


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
        _csv = lambda : read_csv(self.data)
        _tsv = lambda : read_csv(self.data, sep='\t')
        _json = lambda : read_json(self.data)
        _excel = lambda : read_excel(self.data)
        _syslog = lambda : _read_syslog()
        _pcap = lambda : _read_pcap()

        return eval('{}()'.format(self.type))

    def _read_syslog(self):
        # Implement syslog parsing 
        pass
    
    def _read_pcap(self):
        pass

class Writer():
    def __init__(self, path, type, df):
        '''
        Initialise writer to write data to file
        
        Parameters
        ----------
        path : str
            Path to write file to
        type : int
            type can be one of 4 values [1, 2 ,3, 4] to represent
            [csv, tsv, json, excel] file type respectively.
        df : pandas dataframe
            pandas dataframe containing data to be exported

        Raise
        -----
        FileExistsError
            Raised when file exists and user does not want to overwrite file
        ValueError
            Raised when a invalid file type is given
        '''
        if os.path.exists(path):
            valid = False
            while not valid:
                opt = input("File exists. Do you want to overwrite file? [Y/n]").strip()
                if opt not in ['Y', 'n']:
                    print('Invalid option')
                    continue

                valid = True
                
            if opt == 'Y':
                self.path = path
            elif opt == 'n':
                raise FileExistsError("File present")
        
        self.df = df

        types = {1: '_csv', 2: "_tsv", 3: '_json', 4: '_excel'}
        if type not in types.keys():
            raise ValueError('Invalid type specified')
        
        self.type = types[type]
    
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
        _csv = lambda : self.df.to_csv(index=False, path_or_buf=self.path)
        _tsv = lambda : self.df.to_csv(index=False, path_or_buf=self.path, sep='\t')
        _json = lambda : self.df.to_json(index=False, path_or_buf=self.path)
        _excel = lambda : self.df.to_excel(index=False, path_or_buf=self.path)

        eval('{}()'.format(self.type))
        return True