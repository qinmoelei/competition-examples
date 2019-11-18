import json
import os
import shutil
import time

import numpy as np
from sklearn.metrics import accuracy_score

reference_dir = os.path.join('/app/input/', 'ref')
prediction_dir = os.path.join('/app/input/', 'res')
score_dir = '/app/output/'
shared_dir = '/app/shared/'
prediction_path = os.path.join(shared_dir, 'prediction')

training_data = np.genfromtxt(os.path.join(reference_dir, 'training_data'))
training_label = np.genfromtxt(os.path.join(reference_dir, 'training_label'))
truth = np.genfromtxt(os.path.join(reference_dir, 'testing_label'))

accuracy = []

number_of_chunks = 5

data_chunks = iter(np.array_split(training_data, number_of_chunks))
label_chunks = iter(np.array_split(training_label, number_of_chunks))


def write_next_chunk():
    np.savetxt(os.path.join(shared_dir, 'training_data'), next(data_chunks))
    np.savetxt(os.path.join(shared_dir, 'training_label'), next(label_chunks))


def chunk_cycle():
    for _ in range(number_of_chunks):
        write_next_chunk()
        start = time.time()
        while not os.path.exists(prediction_path):
            if time.time() - start > 5 * 60:  # Don't wait longer than 5 minutes
                return 1, 'timeout'
            if os.path.exists(os.path.join(shared_dir, 'abort')):
                return 1, 'abort signal sent'
            # wait for first prediction
            time.sleep(0.01)
        prediction = np.genfromtxt(prediction_path)
        os.remove(prediction_path)
        acc = accuracy_score(truth, prediction)

        # shouldn't be accuracy, and should be json... fix later
        print(json.dumps({
            "type": "error_rate_update",
            "error_rate": acc,
        }))

        accuracy.append(acc)
    return 0, ''


def main():
    try:
        shutil.copy(
            os.path.join(reference_dir, 'testing_data'),
            os.path.join(shared_dir, 'testing_data')
        )
        return_code, message = chunk_cycle()
        if return_code != 0:
            print(f'ingestion program error message: {message}')
        # signal ingestion program that we are done
        np.savetxt(os.path.join(shared_dir, 'stop'), [])
        final_accuracy = accuracy[-1] if return_code == 0 else -1

        scores = {
            'accuracy': final_accuracy,
        }

        print(scores)

        with open(os.path.join(score_dir, 'scores.json'), 'w') as score_file:
            score_file.write(json.dumps(scores))
    except Exception as e:
        np.savetxt(os.path.join(shared_dir, 'stop'), [])
        raise e


if __name__ == '__main__':
    print('starting scoring program')
    main()
    print('scoring finished')
