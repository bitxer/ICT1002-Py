import csv
import os
import sys
import numpy as np
import pandas as pd
import operator

from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Dense, Activation
from sklearn.model_selection import train_test_split, StratifiedShuffleSplit
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.utils import to_categorical, normalize
from sklearn.utils import shuffle
from timeit import default_timer as timer
import time

dataPath = '../'
resultPath = '../model'
if not os.path.exists(resultPath):
    print('result path {} created.'.format(resultPath))
    os.mkdir(resultPath)
    
model_name = "init"



def loadData(fileName):
    dataFile = os.path.join(dataPath, fileName)
    pickleDump = '{}.pickle'.format(dataFile)
    if os.path.exists(pickleDump):
        df = pd.read_pickle(pickleDump)
    else:
        df = pd.read_csv(dataFile)
        df = df.dropna()
        df = shuffle(df)
        df.to_pickle(pickleDump)
    return df

def baseline_model(inputDim=-1, out_shape=(-1,)):
    global model_name
    model = Sequential()
    if inputDim > 0 and out_shape[1] > 0:
        model.add(Dense(79, activation='relu', input_shape=(inputDim,)))
        print(f"out_shape[1]:{out_shape[1]}")
        model.add(Dense(128, activation='relu'))
        
        model.add(Dense(out_shape[1], activation='softmax')) #This is the output layer
        print('Categorical Cross-Entropy Loss Function')
        model_name += "_categorical"
        model.compile(optimizer='adam',
                     loss='categorical_crossentropy',
                     metrics=['accuracy'])
    return model


def experiment(dataFile, optimizer='adam', epochs=1000, batch_size=70):
    
    #Creating data for analysis
    time_gen = int(time.time())
    global model_name
    model_name = f"Atk-multiclass_{time_gen}"
    
    seed = 7
    np.random.seed(seed)
    cvscores = []
    print('optimizer: {} epochs: {} batch_size: {}'.format(
        optimizer, epochs, batch_size))
    
    data = loadData(dataFile)
    data_y = data.pop('Label')
    
    #transform named labels into numerical values
    encoder = LabelEncoder()
    encoder.fit(data_y)
    data_y = encoder.transform(data_y)
    dummy_y = to_categorical(data_y)
    data_x = normalize(data.values)

    #define 5-fold cross validation test harness
    inputDim = len(data_x[0])
    print('inputdim = ', inputDim)
    

    num=0
    sss = StratifiedShuffleSplit(n_splits=1, test_size=0.2, random_state=10)
    start = timer()
    for train_index, test_index in sss.split(X=np.zeros(data_x.shape[0]), y=dummy_y):
        X_train, X_test = data_x[train_index], data_x[test_index]
        y_train, y_test = dummy_y[train_index], dummy_y[test_index]

        #create model
        model = baseline_model(inputDim, y_train.shape)
    
        #train
        print("Training " + dataFile + " on split " + str(num))
        model.fit(x=X_train, y=y_train, epochs=epochs, batch_size=batch_size, verbose=2, validation_data=(X_test, y_test))

        #save model
        model.save(f"{resultPath}/{model_name}_1000_ep_75_bs.h5")

        num+=1

    elapsed = timer() - start

    scores = model.evaluate(X_test, y_test, verbose=1)
    print(model.metrics_names)
    acc, loss = scores[1]*100, scores[0]*100
    print('Baseline: accuracy: {:.2f}%: loss: {:.2f}'.format(acc, loss))


    resultFile = os.path.join(resultPath, dataFile)
    with open('{}.result'.format(resultFile), 'a') as fout:
        fout.write('{} results...'.format(model_name))
        fout.write('\taccuracy: {:.2f} loss: {:.2f}'.format(acc, loss))
        fout.write('\telapsed time: {:.2f} sec\n'.format(elapsed))
        
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 tf_model.py inputFile.csv")
    else:
        experiment(sys.argv[1])
        

