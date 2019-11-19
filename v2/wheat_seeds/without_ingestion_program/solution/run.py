import os
import sys
from model import Model

import numpy as np

input_dir = '/app/input_data/'
output_dir = '/app/output/'
program_dir = '/app/program'
submission_dir = '/app/ingested_program'

sys.path.append(program_dir)
sys.path.append(submission_dir)


def get_training_data():
    X_train = np.genfromtxt(os.path.join(input_dir, 'training_data'))
    y_train = np.genfromtxt(os.path.join(input_dir, 'training_label'))
    return X_train, y_train


def get_prediction_data():
    return np.genfromtxt(os.path.join(input_dir, 'testing_data'))


def main():
    print('Reading Data')
    X_train, y_train = get_training_data()
    X_test = get_prediction_data()
    print('Starting')
    m = Model()
    print('Training Model')
    m.fit(X_train, y_train)
    print('Running Prediction')
    prediction = m.predict(X_test)
    np.savetxt(os.path.join(output_dir, 'prediction'), prediction)


if __name__ == '__main__':
    main()
