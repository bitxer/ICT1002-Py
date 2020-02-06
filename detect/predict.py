import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2' #Suppres error
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.utils import to_categorical, normalize
import numpy as np
import pandas as pd
from sklearn.utils import shuffle


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

def run_predict(fileName):
    df = loadData(fileName)

    #df1 =df.pop('Label')
    logID = df.pop('ID')
    df_test = normalize(df.values)

    model = load_model_csv()
    model.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['accuracy'])


    predictions = model.predict_proba(df_test)
    for p,q in zip(predictions, logID):
        output[q] = atks[np.argmax(p)]

    return output

if __name__=="__main__":
    output = run_predict("small_test_no_labels.csv")
    print(output)




