"""
Baseline model.
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import os

import pandas as pd
from sklearn.externals import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split



def main(args):
    print('Loading dataset...')
    df = pd.read_csv(args.dataset)
    X, y = df['tweet'], df['class']
    x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    print('Vectorizing...')
    vectorizer = TfidfVectorizer()
    x_train = vectorizer.fit_transform(x_train)
    x_test = vectorizer.transform(x_test)

    print('Fitting...')
    clf = LogisticRegression(penalty='l1')
    clf.fit(x_train, y_train)

    print('Predicting...')
    y_pred = clf.predict(x_test)

    print(classification_report(y_test, y_pred))

    print('Saving...')
    joblib.dump(clf, args.model_file)
    joblib.dump(vectorizer, args.preprocessor)


if __name__ == '__main__':
    DATA_DIR = os.path.join(os.path.dirname(__file__), '../../data')
    parser = argparse.ArgumentParser(description='Training a classifier')
    parser.add_argument('--dataset', default=os.path.join(DATA_DIR, 'labeled_data.csv'), help='dataset')
    parser.add_argument('--model_file', default=os.path.join(DATA_DIR, 'model/model.pkl'), help='model file')
    parser.add_argument('--preprocessor', default=os.path.join(DATA_DIR, 'model/preprocess.pkl'), help='preprocessor')
    args = parser.parse_args()
    main(args)