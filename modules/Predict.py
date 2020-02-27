import os
from tensorflow.keras.models import load_model
from tensorflow.keras.utils import to_categorical, normalize
from numpy import argmax
from pandas import DataFrame
import socket

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # Suppress error

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
    protocol = df['Protocol'].values
    port_num = df['Dst Port'].values
    time = df[['Timestamp']].values
    df_test = normalize(df.values)
    model = load_model("modules/model/binary_class_classifier.h5")
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    predictions = model.predict_proba(df_test)

    df2 = DataFrame(columns=columnList)
    for p, q, r, s, t, sip in zip(predictions, logID, protocol, port_num, time, sourceIP):
        if argmax(p) == 0:
            output[int(q)] = {
                "IsAtk": argmax(p),
                "IP": sip,
                "Protocol": protocols[r],
                "Port": int(s),
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
    columnList = df.columns
    df1 = df.copy()

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
        10: 'Infiltration',
        11: 'SQL Injection',
        12: 'SSH-Bruteforce'
    }

    logID = df.pop('ID')
    SourceIP = df.pop('SourceIP')
    time = df[['Timestamp']].values
    protocol = df[['Protocol']].values
    port = df[['Dst Port']].values
    df_test = normalize(df.values)
    model = load_model("modules/model/Atk_multiclass_categorical_50_ep_80_bs.h5")
    model.compile(optimizer='adam',
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])

    predictions = model.predict_proba(df_test)

    for l, sip, p1, p2, p3, t in zip(logID, SourceIP, predictions, protocol, port, time):
        output[int(l)] = {"IsAtk": 1,
                          "IP": sip,
                          "Protocol": protocols[int(p2)],
                          "Port": int(p3),
                          "Atk": atks[argmax(p1)],
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
    print(noAtk)
    output = noAtk.copy()
    atk_output = run_predict_Atks(Atk)

    output.update(atk_output)
    return output