import os
import numpy as np
import pandas as pd
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.utils import to_categorical, normalize
from sklearn.utils import shuffle
from timeit import default_timer as timer
import time


def loadData(fileName):
    '''
    Load data as pickle

    Parameter
    ---------
    fileName : str

    Return
    ------
    [Success]
        df : Dataframe
    '''
    pickleDump = '{}.pickle'.format(fileName)
    if os.path.exists(pickleDump):
        df = pd.read_pickle(pickleDump)
    else:
        df = pd.read_csv(fileName)
        df = df.dropna()
        df = shuffle(df)
        df.to_pickle(pickleDump)
    return df


def baseline_model(inputDim=-1, out_shape=(-1,)):
    '''
    Configure Model Settings

    Parameter
    ---------
    inputDim : int
    out_shape : tuple

    Return
    ------
    [Success]
        model : Sequential
        label_type : str
    '''
    label_type = ""
    model = Sequential()
    if inputDim > 0 and out_shape[1] > 0:
        model.add(Dense(79, activation='relu', input_shape=(inputDim,)))
        print(f"out_shape[1]:{out_shape[1]}")
        model.add(Dense(128, activation='relu'))

        model.add(Dense(out_shape[1], activation='softmax'))  # This is the output layer
        if out_shape[1] > 2:
            print('Categorical Cross-Entropy Loss Function')
            label_type += "_categorical"
            model.compile(optimizer='adam',
                          loss='categorical_crossentropy',
                          metrics=['accuracy'])
        else:
            label_type+="_binary"
            print('Binary Cross-Entrophy Loss Function')
            model.compile(optimizer='adam',
                          loss='binary_crossentropy',
                          metrics=['accuracy'])
    return model, label_type


def run_ML(fileName, optimizer='adam', epochs=100, batch_size=50):
    '''
    Train Attack Log Detection

    Parameters
    ----------
    fileName : str
    optimizer : str
    epochs : int
    batch_size : int
    '''
    time_gen = int(time.time())
    model_name = f"Atk-multiclass_{time_gen}"

    seed = 7
    np.random.seed(seed)
    print('optimizer: {} epochs: {} batch_size: {}'.format(
        optimizer, epochs, batch_size))

    data = loadData(fileName)
    data_y = data.pop('Label')

    # transform named labels into numerical values
    encoder = LabelEncoder()
    encoder.fit(data_y)
    data_y = encoder.transform(data_y)
    dummy_y = to_categorical(data_y)
    data_x = normalize(data.values)

    inputDim = len(data_x[0])
    num = 0
    sss = StratifiedShuffleSplit(n_splits=1, test_size=0.2, random_state=10)
    start = timer()
    for train_index, test_index in sss.split(X=np.zeros(data_x.shape[0]), y=dummy_y):
        X_train, X_test = data_x[train_index], data_x[test_index]
        y_train, y_test = dummy_y[train_index], dummy_y[test_index]

        # create model
        model, class_type = baseline_model(inputDim, y_train.shape)

        # train
        print("Training " + fileName + " on split " + str(num))
        model.fit(x=X_train, y=y_train, epochs=epochs, batch_size=batch_size, verbose=2,
                  validation_data=(X_test, y_test))

        # save model
        model.save("model/"+model_name+class_type+".h5")

        num += 1

    elapsed = timer() - start

    scores = model.evaluate(X_test, y_test, verbose=1)
    print(model.metrics_names)
    acc, loss = scores[1] * 100, scores[0] * 100
    print('Baseline: accuracy: {:.2f}%: loss: {:.2f}'.format(acc, loss))

    resultFile = os.path.join(model, fileName)
    with open('{}.result'.format(resultFile), 'a') as fout:
        fout.write('{} results...'.format(model_name))
        fout.write('\taccuracy: {:.2f} loss: {:.2f}'.format(acc, loss))
        fout.write('\telapsed time: {:.2f} sec\n'.format(elapsed))



