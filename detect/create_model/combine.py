import os
import pandas as pd
from sklearn.utils import shuffle

labels = {'Benign': 0, 'FTP-BruteForce': 1, 'SSH-Bruteforce': 1, 'DoS attacks-GoldenEye': 1, 'DoS attacks-Slowloris': 1,
     'DoS attacks-SlowHTTPTest': 1, 'DoS attacks-Hulk': 1, 'Brute Force -Web': 1, 'Brute Force -XSS': 1,
     'SQL Injection': 1, 'Infilteration': 1, 'Bot': 1,'DDOS attack-LOIC-UDP':1}


def merge_csv(fileNames, dataPath):
    '''
    Combines Dataset into one csv
    Parameters
    ----------
    fileNames : list(str)
    dataPath : Directory Location

    Return
    ------
    [Success]
        df : DataFrame
            Shuffled combine dataset
    '''
    df = pd.read_csv(os.path.join(dataPath, fileNames[0]))
    for name in fileNames[1:]:
        fname = os.path.join(dataPath, name)
        print('Appending', fname)
        df1 = pd.read_csv(fname)
        df = df.append(df1, ignore_index=True)

    return shuffle(df)
def combine_main(fileDir, LabelType):
    '''
    Main Function to run multi-class or binary labeling

    Parameters
    ----------
    fileDir : str
    LabelType : int
    '''

    dataPath = fileDir # Dataset folder in csv
    fileNames = os.listdir(dataPath)
    df = merge_csv(fileNames,dataPath)
    if str(LabelType).isdigit():
        if LabelType == 0:
            print('create combined attacks')
            outFile = os.path.join(dataPath, 'combined_attacks')
            df.to_csv(outFile + '.csv', index=False)
            print('Combine Dataset Completed')


        elif LabelType ==1:
            print('creating combine csv file')

            for k,v in labels.items():
                df.loc[df['Label']==k, 'Label'] = v

            outFile = os.path.join(dataPath, 'combine_atk_or_not_csv')
            df.to_csv(outFile, index=False)
            print('Combine Dataset Completed')

        else:
            print("Label_type: 1 for binary labels, 0 for keep labels")
    else:
        print("Label_type: 1 for binary labels, 0 for keep labels")

