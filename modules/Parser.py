import os
from pandas import read_csv, read_excel, read_json
from pandas import DataFrame
from numpy import float64

class Reader():
    def __init__(self, path):
        '''
        Initialise reader to read log data

        Parameters
        ----------
        path : str
            Path to log file
        '''
        self.path = path

        supportedfiletypes = {'csv': '_csv', 'tsv': "_tsv",
                              'json': '_json', 'xlsx': '_excel', 'xls': '_excel'}

        filetype = path.split('.')[-1]
        if filetype not in supportedfiletypes.keys():
            self.importformat = supportedfiletypes['csv']
        else:
            self.importformat = supportedfiletypes[filetype]

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

        def _csv():
            return read_csv(self.path)

        def _tsv():
            return read_csv(self.path, sep='\t')

        def _json():
            return read_json(self.path, orient='split', convert_dates=False, convert_axes=False)

        def _excel():
            return read_excel(self.path)

        data = eval('{}()'.format(self.importformat))
        if self.importformat in ['_json', '_excel']:
            for field in data:
                if field != 'SourceIP':
                    data[field] = data[field].astype(float64)
        
        return data


def export_to_file(path, df):
    writer = Writer(path, df)
    return writer.write()


class Writer():
    def __init__(self, path, df):
        '''
        Initialise writer to write data to file

        Parameters
        ----------
        path : str
            Path to write file to
        df : pandas dataframe
            pandas dataframe containing data to be exported
        '''
        self.path = path

        self.df = df

        supportedfiletypes = {'csv': '_csv', 'tsv': "_tsv",
                              'json': '_json', 'xlsx': '_excel', 'xls': '_excel'}
        filetype = path.split('.')[-1]
        if filetype not in supportedfiletypes.keys():
            self.exporttype = supportedfiletypes['csv']
        else:
            self.exporttype = supportedfiletypes[filetype]

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
        def _csv():
            return self.df.to_csv(index=False, header=True, path_or_buf=self.path)

        def _tsv():
            return self.df.to_csv(index=False, header=True,  path_or_buf=self.path, sep='\t')

        def _json():
            return self.df.to_json(index=False, indent=2, path_or_buf=self.path, orient='table')

        def _excel():
            return self.df.to_excel(index=False, header=True, excel_writer=self.path)

        eval('{}()'.format(self.exporttype))
        return True
