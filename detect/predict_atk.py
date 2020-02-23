import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # Suppress error
from tensorflow.keras.models import load_model
from tensorflow.keras.utils import to_categorical, normalize
import numpy as np
import pandas as pd
import socket


def run_predict_isAtk(df):
    '''
    Separate attacks traffic and normal traffic

    Parameters
    ----------
    df : DataFrame

    Return
    ------
    [Success]
        output : dict
            Normal traffic
        df2 : DataFrame
            Attack traffic to be analyse
    '''
    output = {}
    protocols = {num: name[8:] for name, num in vars(socket).items() if name.startswith("IPPROTO")}
    columnList = df.columns
    df1 = df.copy()
    logID = df.pop('ID')
    sourceIP = df.pop('SourceIP')
    DestIP = df.pop('DestIP')
    protocol = df['Protocol'].values
    port_num = df['Dst Port'].values
    time = df[['Timestamp']].values
    df_test = normalize(df.values)
    model = load_model("model/binary_class_classifier.h5")
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    predictions = model.predict_proba(df_test)

    df2 = pd.DataFrame(columns=columnList)
    for p, q, r, s, t, sip, dip in zip(predictions, logID, protocol, port_num, time, sourceIP, DestIP):
        if np.argmax(p) == 0:
            output[int(q)] = {
                "IsAtk": np.argmax(p),
                "Source IP": sip,
                "Dst IP": dip,
                "Protocol": protocols[r],
                "Dst Port": int(s),
                "Time": int(t[0])
            }


        else:
            row_index = df1.loc[df1["ID"] == q].index[0]
            df2.loc[df1.index[row_index]] = df1.iloc[row_index]

    return output, df2


def run_predict_Atks(df):
    '''
    Identify Possible Attacks

    Parameters
    ----------
    df : DataFrame

    Return
    ------
        output : dict
            Labels Attack Traffic
	'''

    output = {}
    protocols = {num: name[8:] for name, num in vars(socket).items() if name.startswith("IPPROTO")}
    atks = {
        0: 'Bot',
        1: 'Brute Force -Web',
        2: 'Brute Force -XSS',
        3: 'DDOS attack-HOIC',
        4: 'DDOS attack-LOIC-UDP',
        5: 'DoS attacks-GoldenEye',
        6: 'DoS attacks-Hulk',
        7: 'DoS attacks-SlowHTTPTest',
        8: 'DoS attacks-Slowloris',
        9: 'FTP-BruteForce',
        10: 'Infilteration',
        11: 'SQL Injection',
        12: 'SSH-Bruteforce'
    }

    logID = df.pop('ID')
    SourceIP = df.pop('SourceIP')
    DestIP = df.pop('DestIP')
    time = df[['Timestamp']].values
    protocol = df[['Protocol']].values
    port = df[['Dst Port']].values
    df_test = normalize(df.values)
    model = load_model("model/Atk_multiclass_categorical_50_ep_80_bs.h5")
    model.compile(optimizer='adam',
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])

    predictions = model.predict_proba(df_test)
    for l, sip, dip, p1, p2, p3, t in zip(logID, SourceIP, DestIP, predictions, protocol, port, time):
        output[int(l)] = {"IsAtk": 1,
                          "Source IP": sip,
                          "Dst IP": dip,
                          "Protocol": protocols[int(p2)],
                          "Dst Port": int(p3),
                          "Atk": atks[np.argmax(p1)],
                          "Time": int(t[0])
                          }
    return output


def run_predict_main(df):
    '''
    To identify attacks from log data

    Parameters
    ----------
    df : DataFrame

    Return
    ------
    [Success]
        output : dict
            Results of the logs

	'''
    (noAtk, Atk) = run_predict_isAtk(df)
    output = noAtk.copy()
    atk_output = run_predict_Atks(Atk)

    output.update(atk_output)
    return output