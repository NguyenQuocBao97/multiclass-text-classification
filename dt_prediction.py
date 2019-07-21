# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in

import numpy as np
import pandas as pd
from keras.callbacks import EarlyStopping
from keras.layers import Dense, Embedding, SpatialDropout1D, LSTM, Dropout
from keras.models import Sequential
from keras.utils import np_utils
from matplotlib import pyplot
from sklearn import model_selection
from sklearn.preprocessing import LabelEncoder
from sklearn.utils import shuffle
from sklearn import tree
if __name__ == '__main__':
    data = pd.read_excel('./output_dt.xlsx')
    _LABEL = 'result'
    data = shuffle(data)

    i = 8
    data = data.drop(['file'], axis=1)
    data_to_predict = data[:i].reset_index(drop=True)
    predict_species = data_to_predict.result
    predict_species = np.array(predict_species)
    prediction = np.array(data_to_predict.drop([_LABEL], axis=1))

    data = data[i:].reset_index(drop=True)

    X = data.drop([_LABEL], axis=1)
    X = np.array(X)
    Y = data[_LABEL]

    # Transform name species into numerical values
    encoder = LabelEncoder()
    encoder.fit(Y)
    Y = encoder.transform(Y)
    Y = np_utils.to_categorical(Y)
    # print(Y)

    # We have 3 classes : the output looks like :
    # 0,0,1 : Class 1
    # 0,1,0 : Class 2
    # 1,0,0 : Class 3

    train_x, test_x, train_y, test_y = model_selection.train_test_split(X, Y, test_size=0.1, random_state=10)
    # print(data.columns)
    input_dim = len(data.columns) - 1
    model = tree.DecisionTreeClassifier()
    history = model.fit(train_x, train_y)
    scores = model.score(test_x, test_y)
    print(scores)
    # print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1] * 100))
    # print(history.history.keys())
    # pyplot.plot(history.history['acc'], label='train')
    # pyplot.plot(history.history['loss'], label='loss')
    # pyplot.legend()
    # pyplot.show()
