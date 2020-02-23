import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2' #Suppres error
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.utils import to_categorical, normalize
import numpy as np
import pandas as pd
from sklearn.utils import shuffle
import socket
#lazy to add back ip
import random
import struct
ip_l = []
for i in range(20):
    ip_l.append(socket.inet_ntoa(struct.pack('>I', random.randint(1, 0xffffffff))))

output = {}
atks = {
 0:'Bot',
 1:'Brute Force -Web',
 2:'Brute Force -XSS', 
 3:'DDOS attack-HOIC',
 4:'DDOS attack-LOIC-UDP',
 5:'DoS attacks-GoldenEye',
 6:'DoS attacks-Hulk', 
 7:'DoS attacks-SlowHTTPTest', 
 8:'DoS attacks-Slowloris',
 9:'FTP-BruteForce',
 10:'Infilteration',
 11:'SQL Injection',
 12:'SSH-Bruteforce'
}
protocols = {num:name[8:] for name,num in vars(socket).items() if name.startswith("IPPROTO")}



def loadData(fileName):
    dataFile = fileName
    pickleDump = '{}.pickle'.format(dataFile)
    if os.path.exists(pickleDump):
        df = pd.read_pickle(pickleDump)
    else:
        df = pd.read_csv(dataFile)
        df = df.dropna()
        df.to_pickle(pickleDump)
    return df

def load_model_csv():
    model = load_model("Atk_multiclass_categorical_50_ep_80_bs.h5")
    return model

def run_predict(df):
    #df = loadData(fileName)



    logID = df.pop('ID')
    SourceIP = df.pop('SourceIP')
    DestIP = df.pop('DestIP')
    time = df[['Timestamp']].values
    protocol = df[['Protocol']].values
    port = df[['Dst Port']].values
    df_test = normalize(df.values)

    model = load_model_csv()
    model.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['accuracy'])


    predictions = model.predict_proba(df_test)
    i=0
    proto = dict()
    for l,sip,dip,p1,p2,p3,t in zip(logID,SourceIP,DestIP,predictions,protocol,port,time):#ID
        output[int(l)] = {"IsAtk": 1,
                     "Source IP":sip,
                     "Dst IP": dip,
                     "Protocol":protocols[int(p2)],
                     "Dst Port":int(p3),
                     "Atk": atks[np.argmax(p1)],
                     "Time":int(t[0])
                     }

        i+=1

    return output

if __name__=="__main__":
    output = run_predict("big_test_3.csv")#small_test_no_labels.csv")
    print(output)
