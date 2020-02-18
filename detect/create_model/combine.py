import csv
import os
import sys
import numpy as np
import pandas as pd
from sklearn.utils import shuffle
import sys

labels = {'Benign': 0, 'FTP-BruteForce': 1, 'SSH-Bruteforce': 1, 'DoS attacks-GoldenEye': 1, 'DoS attacks-Slowloris': 1,
     'DoS attacks-SlowHTTPTest': 1, 'DoS attacks-Hulk': 1, 'Brute Force -Web': 1, 'Brute Force -XSS': 1,
     'SQL Injection': 1, 'Infilteration': 1, 'Bot': 1}


def merge_csv(fileNames):
    df = pd.read_csv(os.path.join(dataPath, fileNames[0]))
    for name in fileNames[1:]:
        fname = os.path.join(dataPath, name)
        print('Appending', fname)
        df1 = pd.read_csv(fname)
        df = df.append(df1, ignore_index=True)

    return shuffle(df)


if len(sys.argv) !=2:
	exit("Usage: python3 combine.py <Dataset Folder> <Label_type>\n\
		Label_type: 1 for binary labels, 0 for keep labels")
if not sys.argv[2].isdigit():
	exit("Label_type: 1 for binary labels, 0 for keep labels")

dataPath = sys.argv[1] # Dataset folder in csv
fileNames = os.listdir(dataPath)
df = merge_csv(fileNames)

if sys.argv[2] == 0:
    print('create combined attacks')
    outFile = os.path.join(dataPath, 'combined_attacks')
    df.to_csv(outFile + '.csv', index=False)

elif sys.argv[2] ==1:
    print('creating combine csv file')

    for k,v in labels.items():
        df.loc['Label'==k, 'Label'] = v

    outFile = os.path.join(dataPath, 'combine_atk_or_not_csv')
    df.to_csv(outFile + '.csv', index=False)
else:
	exit("Label_type: 1 for binary labels, 0 for keep labels")


print('Combine Dataset Completed')
