# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in

import numpy as np
import pandas as pd
from sklearn import model_selection
from sklearn import tree
from sklearn.metrics import f1_score
from sklearn.utils import shuffle
from sklearn import svm
from sklearn import ensemble
from sklearn import naive_bayes
from sklearn import externals
from sklearn import neighbors

import pickle
if __name__ == '__main__':
    print('\n\n\n')
    for num in [2, 1, 12]:
        print('===========================================GROUP {}==================='.format(num))
        xlsx_output_file = 'output_dt_group_{}'.format(num)
        group = '-'.join(xlsx_output_file.split('_')[-2:])
        data = pd.read_excel('./{}.xlsx'.format(xlsx_output_file))
        _LABEL = 'result'
        data = shuffle(data)

        i = 8
        data = data.drop(['file'], axis=1)

        data = data[i:].reset_index(drop=True)

        X = data.drop([_LABEL], axis=1)
        X = np.array(X)
        Y = data[_LABEL]

        # encoder = LabelEncoder()
        # encoder.fit(Y)
        # Y = encoder.transform(Y)
        # Y = np_utils.to_categorical(Y)
        # print(Y)
        train_x, test_x, train_y, test_y = model_selection.train_test_split(X, Y, test_size=0.1, random_state=10)
        # print(data.columns)

        models = [
            [svm.SVC(), 'svm'],
            [tree.DecisionTreeClassifier(), 'dt'],
            [ensemble.RandomForestClassifier(n_estimators=100), 'rf'],
            [naive_bayes.GaussianNB(), 'nb'],
            [neighbors.KNeighborsClassifier(), 'knn']

        ]
        for model_info in models:

            model = model_info[0]
            model_name = model_info[1]

            history = model.fit(train_x, train_y)
            # print(tree.plot_tree(model))
            with open('./saved_model/{}_model_{}.pkl'.format(model_name, group), 'wb') as file:
                pickle.dump(model, file)
            scores = model.score(test_x, test_y)
            f1_scores = f1_score(test_y, model.predict(test_x), average='weighted')


        # dot_data = StringIO()
        # export_graphviz(
        #     model,
        #     out_file=dot_data,
        #     class_names=list(set(Y)),
        #     filled=True,
        #     rounded=True,
        #     special_characters=True,
        #     feature_names=[col for col in data.columns if col != _LABEL]
        # )
        # graph = pydotplus.graph_from_dot_data(dot_data.getvalue())
        # image = Image(graph.create_png())
        # with open('dt_output.png', 'wb') as png:
        #     png.write(image.data)
            print('{} model with score: '.format(model_name), f1_scores)
