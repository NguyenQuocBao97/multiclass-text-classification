# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in

import numpy as np
import pandas as pd
from keras.callbacks import EarlyStopping
from keras.layers import Dense, Embedding, SpatialDropout1D, LSTM, Dropout, K
from keras.models import Sequential
from keras.utils import np_utils
from matplotlib import pyplot
from sklearn import model_selection
from sklearn.preprocessing import LabelEncoder
from sklearn.utils import shuffle

if __name__ == '__main__':
    GROUP = '12'
    data = pd.read_excel('./output_mc_group_{}.xlsx'.format(GROUP))
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
    def recall_m(y_true, y_pred):
        true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
        possible_positives = K.sum(K.round(K.clip(y_true, 0, 1)))
        recall = true_positives / (possible_positives + K.epsilon())
        return recall

    def precision_m(y_true, y_pred):
        true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
        predicted_positives = K.sum(K.round(K.clip(y_pred, 0, 1)))
        precision = true_positives / (predicted_positives + K.epsilon())
        return precision

    def f1_m(y_true, y_pred):
        precision = precision_m(y_true, y_pred)
        recall = recall_m(y_true, y_pred)
        return 2 * ((precision * recall) / (precision + recall + K.epsilon()))

    train_x, test_x, train_y, test_y = model_selection.train_test_split(X, Y, test_size=0.1, random_state=0)
    # print(data.columns)
    input_dim = len(data.columns) - 1
    MAX_NB_WORDS = 50000
    EMBEDDING_DIM = 100
    model = Sequential()

    model.add(Embedding(1024, output_dim=256))
    model.add(LSTM(128))
    model.add(Dropout(0.5))
    model.add(Dense(3, activation='sigmoid'))
    model.compile(loss='categorical_crossentropy',
                  optimizer='adam',
                  metrics=[f1_m])
    history = model.fit(train_x, train_y, batch_size=16, epochs=10)
    f1_score = model.evaluate(test_x, test_y, batch_size=16)[1]
    model.save('./nn_model/{}.h5'.format(GROUP))
    print(f1_score)
    # print(history.history.keys())
    # pyplot.plot(history.history['acc'], label='train')
    # pyplot.plot(history.history['loss'], label='loss')
    # pyplot.legend()
    # pyplot.show()
