# Seed:
### metadata.yaml
```yaml
command: python3 run.py
```

### model.py
```python
class Model:
    def fit(self, X_train, y_train):
        """
        This should handle the logic of training your model
        :param X_train: 7 dimensional np.array of training data
        :param y_train: 1 dimensional np.array of the same length as X_train. Contains classifications of X_train
        """
        pass

    def predict(self, X_test):
        """
        This should handle making predictions with a trained model
        :param X_test: 7 dimensional np.array of testing data
        :return: 1 dimensional np.array of the same length as X_test containing predictions to each point in X_test
        """
        pass

```

### run.py
```python
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

```
