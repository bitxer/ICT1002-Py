import os
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.utils import to_categorical, normalize
import numpy as np
import pandas as pd
from sklearn.utils import shuffle
import socket


output = {}
protocols = {num:name[8:] for name, num in vars(socket).items() if name.startswith("IPPROTO")}
def loadData(fileName):
    dataFile = fileName
    #pickleDump = '{}.pkl'.format(dataFile)
    #if os.path.exists(pickleDump):
    #    df = pd.read_pickle(pickleDump)
    #else:
    df = pd.read_csv(dataFile)

    df = df.dropna()
    #df.to_pickle(pickleDump)
    return df

def load_tensor_model():
    model = load_model("binary_class_classifier.model")
    return model

def run_predict(fileName):
    df = loadData(fileName)
    columnList = df.columns

    df1 = df.copy()
    logID = df.pop('ID')
    sourceIP = df.pop('SourceIP')
    DestIP = df.pop('DestIP')
    protocol = df['Protocol'].values
    port_num = df['Dst Port'].values
    time = df[['Timestamp']].values
    df_test = normalize(df.values)
    model = load_tensor_model()
    model.compile(optimizer = 'adam',loss = 'binary_crossentropy', metrics=['accuracy'])
    predictions = model.predict_proba(df_test)

    df2 = pd.DataFrame(columns = columnList) 
    for p,q,r,s,t,sip,dip in zip(predictions, logID,protocol,port_num, time, sourceIP,DestIP):
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
            #df2.loc[df1.index[q]] = df1.iloc[q]
            row_index = df1.loc[df1["ID"] == q].index[0]
            df2.loc[df1.index[row_index]] = df1.iloc[row_index]

        
    return output, df2

if __name__ == "__main__":
    output, df2 = run_predict("test3.csv")
    print(df2)
    print(output)