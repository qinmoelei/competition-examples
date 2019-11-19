import os
import sys
import time

import numpy as np

input_dir = '/app/input_data'
output_dir = '/app/output'
program_dir = '/app/program'
submission_dir = '/app/ingested_program'
shared_dir = '/app/shared'

sys.path.append(program_dir)
sys.path.append(output_dir)
sys.path.append(submission_dir)

training_data_path = os.path.join(shared_dir, 'training_data')
training_label_path = os.path.join(shared_dir, 'training_label')


def get_training_data():
    print('New Training Data')
    X_train = np.genfromtxt(training_data_path)
    y_train = np.genfromtxt(training_label_path)
    return X_train, y_train


def train_test_cycle(m, X_train, y_train, X_test):
    m.partial_fit(X_train, y_train)
    prediction = m.predict(X_test)
    print('updating prediction')
    np.savetxt(os.path.join(shared_dir, 'prediction'), prediction)


def main():
    try:
        from model import Model
        m = Model()

        start = time.time()
        while not os.path.exists(os.path.join(shared_dir, 'stop')):
            while not os.path.exists(training_data_path):
                if os.path.exists(os.path.join(shared_dir, 'stop')):
                    print('Stop signal received from scoring program')
                    return
                if time.time() - start > 5 * 60:  # Don't wait longer than 5 minutes
                    print('Sending abort signal due to timeout')
                    np.savetxt(os.path.join(shared_dir, 'abort'), [])
                    return
                time.sleep(.01)
            X_test = np.genfromtxt(os.path.join(shared_dir, 'testing_data'))
            X_train, y_train = get_training_data()
            os.remove(training_data_path)
            os.remove(training_label_path)
            train_test_cycle(m, X_train, y_train, X_test)
    except Exception as e:
        np.savetxt(os.path.join(shared_dir, 'abort'), [])
        raise e


if __name__ == '__main__':
    print('starting ingestion program')
    main()
    print('ingestion Finished')
